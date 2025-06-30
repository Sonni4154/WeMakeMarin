# FastAPI Integration Dashboard

## 🔧 Features
- Unified web dashboard for QuickBooks, Google, Gmail, Jibble, and Jotform
- Editable UI forms for Customers, Invoices, and Estimates
- Logging of all user actions
- Google OAuth-ready
- Manual command-line interface
- Responsive, mobile-friendly layout
- Scheduled sync jobs (cron-style)

## 🚀 Deployment Guide (Step-by-Step)

### 1. Requirements
- Linux VPS
- Python 3.10+
- Git, nginx, openssh-server
- (Optional) domain name and HTTPS setup

### 2. Setup
```bash
# Clone and deploy
chmod +x deploy.sh
./deploy.sh
```

### 3. Configuration
Create a `.env` file with credentials:
```env
QB_CLIENT_ID=xxx
GOOGLE_API_KEY=xxx
DATABASE_URL=sqlite:///./test.db
```

### 4. Accessing
- Open `http://your-server-ip:8000` for UI
- Open `http://your-server-ip/ssh_keys/` for public SSH key

### 5. Sync
```bash
./start_cron.sh
```

### 6. Manual Control
```bash
python3 cli.py
```

## 📦 Modules
- `main.py` - App entrypoint
- `routers/` - All FastAPI routers
- `templates/` - HTML UI pages
- `cron_jobs/` - Scheduled sync jobs
- `cli.py` - Command-line CRUD shell
- `log_actions.py` - Action logger
