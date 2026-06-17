# order-service

FastAPI service for creating and reading orders in the DevOps learning lab. It stores orders in PostgreSQL, caches individual orders in Redis, and publishes `order_created` events to AWS SQS.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check for the service process. |
| `GET` | `/ready` | Readiness check for PostgreSQL, Redis, and SQS queue access. |
| `GET` | `/metrics` | Prometheus metrics endpoint. |
| `POST` | `/orders` | Create an order, cache it, and publish an SQS event. |
| `GET` | `/orders/{order_id}` | Read an order from Redis first, then PostgreSQL on cache miss. |
| `GET` | `/orders` | Return recent orders. |

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SERVICE_NAME` | No | `order-service` | Service name used in health responses and logs. |
| `ENVIRONMENT` | No | `dev` | Runtime environment name used in health responses and logs. |
| `DATABASE_URL` | Yes | `postgresql://postgres:postgres@localhost:5432/devops_lab` | SQLAlchemy PostgreSQL URL. |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` | Redis connection URL. |
| `AWS_REGION` | Yes | `us-east-1` | AWS region for the SQS client. |
| `ORDER_EVENTS_QUEUE_URL` | Yes | empty | SQS queue URL for order events. |
| `SQS_ENDPOINT_URL` | No | empty | Optional custom SQS endpoint, useful for LocalStack. |
| `LOG_LEVEL` | No | `INFO` | Root log level for structured JSON logs. |

## Database Table

`orders`

- `id`
- `user_id`
- `amount`
- `status`
- `created_at`

Allowed statuses:

- `created`
- `payment_pending`
- `paid`
- `failed`

## Redis

Individual orders are cached as JSON with this key format:

```text
order:{order_id}
```

## SQS Message

`POST /orders` publishes this JSON payload to `ORDER_EVENTS_QUEUE_URL`:

```json
{
  "event_type": "order_created",
  "order_id": "1",
  "user_id": "5",
  "amount": 100
}
```

## Run Locally

From this directory:

```bash
cd apps/order-service
python -m pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

## Run Tests

The unit tests use SQLite plus fake Redis and SQS clients. They do not require real AWS, PostgreSQL, or Redis.

```bash
cd apps/order-service
python -m pytest -q
```

## Integration Testing Note

Real PostgreSQL, Redis, and SQS-compatible integration testing is intentionally left for later container and Kubernetes environments.

## TODO

- Add an outbox pattern if SQS publish failures should be retried after an order is committed.
- Add pagination parameters for `GET /orders` when the lab needs larger datasets.
