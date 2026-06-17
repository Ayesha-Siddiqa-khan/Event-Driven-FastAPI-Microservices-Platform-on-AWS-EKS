# Expected App Output

This document gives a quick view of what output you should see when the app is working.

For the full explanation, read [`../APP_SUMMARY.md`](../APP_SUMMARY.md).

## Main user journey

```text
register user
↓
login user
↓
create order
↓
order is saved in PostgreSQL
↓
order is cached in Redis
↓
order event is published to SQS
↓
create payment
↓
payment is saved in PostgreSQL
↓
payment event is published to SQS
↓
notification-worker consumes event
↓
notification is saved in PostgreSQL
```

## Expected endpoint outputs

### `/health`

```json
{
  "status": "ok",
  "service": "order-service",
  "environment": "dev"
}
```

### `/ready`

```json
{
  "status": "ready",
  "checks": {
    "postgres": "ok",
    "redis": "ok",
    "sqs": "ok"
  }
}
```

### Register user

```json
{
  "id": 1,
  "email": "demo@example.com",
  "created_at": "2026-06-17T10:00:00Z"
}
```

### Login user

```json
{
  "token": "example-session-token",
  "user_id": 1
}
```

### Create order

```json
{
  "id": 1,
  "user_id": 1,
  "amount": 100.50,
  "status": "created",
  "created_at": "2026-06-17T10:05:00Z"
}
```

### Create payment

```json
{
  "id": 1,
  "order_id": 1,
  "user_id": 1,
  "amount": 100.50,
  "status": "success",
  "created_at": "2026-06-17T10:06:00Z"
}
```

## Expected storage output

### PostgreSQL tables

```text
users
orders
payments
notifications
```

### Redis keys

```text
session:<token> -> user_id
order:<order_id> -> order JSON
```

### SQS messages

```json
{
  "event_type": "order_created",
  "order_id": "1",
  "user_id": "1",
  "amount": "100.50"
}
```

```json
{
  "event_type": "payment_completed",
  "order_id": "1",
  "payment_id": "1",
  "status": "success",
  "user_id": "1"
}
```

## Expected DevOps output

When your deployment is complete, you should be able to show:

- running Kubernetes pods for all services
- only `api-gateway` exposed publicly
- internal services exposed as `ClusterIP`
- PostgreSQL and Redis readiness checks passing
- SQS queues receiving messages
- `notification-worker` consuming queue messages
- Prometheus scraping `/metrics`
- Grafana dashboard showing request rate, latency, errors, queue depth, and worker metrics
- KEDA scaling the worker when queue depth increases
- GitHub Actions rollback when a smoke test fails

