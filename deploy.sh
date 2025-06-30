#!/bin/bash
set -e

APP_NAME="quickbooks_sync_app"
DEPLOY_DIR="/opt/$APP_NAME"

echo "Updating system and installing dependencies..."
apt-get update
apt-get install -y python3 python3-pip python3-venv nginx git openssh-server

echo "Setting up SSH key access..."
useradd -m deployuser || true
mkdir -p /home/deployuser/.ssh
ssh-keygen -b 4096 -t rsa -f /home/deployuser/.ssh/id_rsa -q -N ""
chmod 700 /home/deployuser/.ssh
chmod 600 /home/deployuser/.ssh/id_rsa
chmod 644 /home/deployuser/.ssh/id_rsa.pub
chown -R deployuser:deployuser /home/deployuser/.ssh

echo "Making SSH key available via Nginx..."
mkdir -p /var/www/html/ssh_keys
cp /home/deployuser/.ssh/id_rsa.pub /var/www/html/ssh_keys/
systemctl restart nginx

echo "Deploying app to $DEPLOY_DIR..."
mkdir -p $DEPLOY_DIR
cp -r . $DEPLOY_DIR
cd $DEPLOY_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cat <<EOF > /etc/systemd/system/$APP_NAME.service
[Unit]
Description=FastAPI Uvicorn App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$DEPLOY_DIR
ExecStart=$DEPLOY_DIR/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable $APP_NAME
systemctl start $APP_NAME

echo "Deployment complete. Access your app at http://<your-server-ip>:8000"
echo "SSH public key available at http://<your-server-ip>/ssh_keys/id_rsa.pub"
