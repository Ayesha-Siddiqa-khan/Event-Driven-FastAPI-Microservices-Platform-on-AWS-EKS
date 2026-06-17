# payment-service

FastAPI service for simulating payment attempts for orders in the DevOps learning lab. It stores payment records in PostgreSQL and publishes `payment_completed` events to an AWS SQS notification queue.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check for the service process. |
| `GET` | `/ready` | Readiness check for PostgreSQL and SQS queue access. |
| `GET` | `/metrics` | Prometheus metrics endpoint. |
| `POST` | `/payments/{order_id}` | Create a simulated payment for an order and publish an SQS event. |
| `GET` | `/payments/{payment_id}` | Return payment information from PostgreSQL. |

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SERVICE_NAME` | No | `payment-service` | Service name used in health responses and logs. |
| `ENVIRONMENT` | No | `dev` | Runtime environment name used in health responses and logs. |
| `DATABASE_URL` | Yes | `postgresql://postgres:postgres@localhost:5432/devops_lab` | SQLAlchemy PostgreSQL URL. |
| `AWS_REGION` | Yes | `us-east-1` | AWS region for the SQS client. |
| `NOTIFICATION_EVENTS_QUEUE_URL` | Yes | empty | SQS queue URL for payment notification events. |
| `SQS_ENDPOINT_URL` | No | empty | Optional custom SQS endpoint, useful for LocalStack. |
| `PAYMENT_SUCCESS_MODE` | No | `always` | Use `always` for deterministic success or `random` for simulated success/failure. |
| `LOG_LEVEL` | No | `INFO` | Root log level for structured JSON logs. |

## Database Table

`payments`

- `id`
- `order_id`
- `amount`
- `status`
- `created_at`

Allowed statuses:

- `success`
- `failed`

## SQS Queue Usage

`POST /payments/{order_id}` publishes a `payment_completed` event to `NOTIFICATION_EVENTS_QUEUE_URL` after the payment record is created.

## SQS Message

```json
{
  "event_type": "payment_completed",
  "order_id": "1",
  "payment_id": "10",
  "status": "success"
}
```

## Run Locally

From this directory:

```bash
cd apps/payment-service
python -m pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

## Run Tests

The unit tests use SQLite and a fake SQS client. They do not require real AWS or PostgreSQL.

```bash
cd apps/payment-service
python -m pytest -q
```

## Integration Testing Note

Real PostgreSQL and SQS integration testing is intentionally left for later container, Kubernetes, and AWS environments.

## TODO

- Add an outbox/retry pattern if SQS publish failures should be retried after a payment is committed.
- Add idempotency for repeated payment requests for the same order.
