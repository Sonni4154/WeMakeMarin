# Dockerfile for FastAPI Integration App
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential libpq-dev curl  && pip install --upgrade pip  && pip install -r requirements.txt  && chmod +x generate_env.sh

EXPOSE 8000

CMD ["bash", "-c", "source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000"]
