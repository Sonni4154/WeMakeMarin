#!/bin/bash
# Exit on errors, unset variables, and failed pipes
set -euo pipefail

# Enable debug tracing with --debug
if [[ "${1:-}" == "--debug" ]]; then
    set -x
fi

# Basic error message
trap 'echo "Error on line $LINENO" >&2' ERR

retry() {
    local n=0
    local try=3
    until [ $n -ge $try ]; do
        "$@" && break
        n=$((n+1))
        echo "Command failed: $* (attempt $n/$try)" >&2
        sleep 1
    done
    if [ $n -ge $try ]; then
        echo "Command failed after $try attempts: $*" >&2
        exit 1
    fi
}

echo "🛠️ FastAPI App: Full Deployment Script for Debian 12 (Enhanced)"

# Collect Inputs
read -p "👤 Deployment username [deployuser]: " USERNAME
USERNAME=${USERNAME:-deployuser}
read -p "🌍 Domain name for HTTPS (blank to skip HTTPS): " DOMAIN
read -p "🔐 Use PostgreSQL? (yes/no) [yes]: " USE_PG
USE_PG=${USE_PG:-yes}

# Step 1: Update system and install base packages (with retries)
retry apt update && retry apt upgrade -y
retry apt install -y python3 python3-pip python3-venv build-essential libssl-dev libffi-dev python3-dev \
    nginx git curl ufw openssh-server software-properties-common

# Step 2: Create deploy user and SSH keys
if ! id "$USERNAME" >/dev/null 2>&1; then
    adduser --disabled-password --gecos "" $USERNAME
fi
mkdir -p /home/$USERNAME/.ssh
if [ ! -f /home/$USERNAME/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -f /home/$USERNAME/.ssh/id_rsa -q -N ""
    chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh
fi
mkdir -p /var/www/html/ssh_keys
cp /home/$USERNAME/.ssh/id_rsa.pub /var/www/html/ssh_keys/$USERNAME.pub
chmod 644 /var/www/html/ssh_keys/*
systemctl restart nginx

# Step 3: Configure firewall
ufw allow OpenSSH
ufw allow 80
ufw allow 8000
[ -n "$DOMAIN" ] && ufw allow 443
ufw --force enable

# Step 4: Optional PostgreSQL setup
if [[ "$USE_PG" == "yes" ]]; then
    echo "Installing PostgreSQL..."
    retry apt install -y postgresql postgresql-client libpq-dev
    sudo -u postgres psql -c "CREATE USER $USERNAME WITH PASSWORD 'changeme';" || true
    sudo -u postgres psql -c "CREATE DATABASE fastapi_app OWNER $USERNAME;" || true
    echo "✅ PostgreSQL database 'fastapi_app' created with user '$USERNAME'"
fi

# Step 5: Copy files and install Python dependencies
APP_DIR="/opt/fastapi_integration_app"
mkdir -p $APP_DIR
cp -r . $APP_DIR
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
retry pip install --upgrade pip setuptools wheel
retry pip install -r requirements.txt

# Step 6: Generate .env config
echo "Generating .env from user input..."
./generate_env.sh

# Step 7: Setup systemd
cat <<EOF > /etc/systemd/system/fastapi_app.service
[Unit]
Description=FastAPI Integration App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable fastapi_app
systemctl restart fastapi_app

# Step 8: Setup HTTPS with Certbot
if [ -n "$DOMAIN" ]; then
    echo "🔐 Setting up HTTPS with Certbot..."
    retry apt install -y certbot python3-certbot-nginx
    certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m admin@$DOMAIN || echo "⚠️ Certbot failed, continuing..."
    systemctl reload nginx
fi

# Step 9: Cron sync
(crontab -l 2>/dev/null; echo "*/15 * * * * cd $APP_DIR && $APP_DIR/venv/bin/python cron_jobs/sync.py >> $APP_DIR/sync.log 2>&1") | crontab -

# Step 10: Output
IP=$(curl -s ifconfig.me)
echo ""
echo "✅ Deployment Complete!"
echo "🌐 App: http://${DOMAIN:-$IP}:8000"
echo "🔑 SSH Key: http://${DOMAIN:-$IP}/ssh_keys/$USERNAME.pub"
echo "📁 App Directory: $APP_DIR"
echo "🗃️ DB: ${USE_PG:-sqlite} — check .env for config"
echo "📜 Logs: actions.log, sync.log"
