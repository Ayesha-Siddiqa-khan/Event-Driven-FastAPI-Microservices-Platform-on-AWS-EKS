# notification-worker

Background worker that consumes notification events from SQS and saves notifications in PostgreSQL.

## Uses

- PostgreSQL for notifications
- AWS SQS for consuming notification events
- Small FastAPI server for health and metrics

## Environment variables

```text
DATABASE_URL=postgresql://user:password@localhost:5432/devops_lab
NOTIFICATION_EVENTS_QUEUE_URL=https://sqs.REGION.amazonaws.com/ACCOUNT/notification-events-queue
AWS_REGION=us-east-1
SQS_ENDPOINT_URL=optional-for-localstack
WORKER_POLL_INTERVAL_SECONDS=2
SERVICE_NAME=notification-worker
ENVIRONMENT=dev
```

## Run locally

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```
