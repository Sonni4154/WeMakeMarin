# 🐳 Docker Deployment for FastAPI Integration App

## Requirements

- Docker
- Docker Compose

## Setup

1. Clone the repo and enter the directory:

```bash
git clone https://your.repo.here
cd fastapi-integration-app
```

2. Create your `.env` file:

```bash
./generate_env.sh
```

3. Start the application:

```bash
docker-compose up --build
```

4. Visit:

- App: http://localhost:8000
- PostgreSQL: available internally as `db`

## Services

- `web`: FastAPI application (port 8000)
- `db`: PostgreSQL 15

## Data Volumes

- `pgdata`: PostgreSQL persistent storage
