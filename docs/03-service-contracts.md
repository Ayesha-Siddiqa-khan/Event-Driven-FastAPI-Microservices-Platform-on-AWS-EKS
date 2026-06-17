# 03 - Service Contracts

## Common endpoints

Every HTTP service exposes:

```text
GET /health
GET /ready
GET /metrics
```

### /health

Checks whether the process is alive. Use this for liveness probes.

### /ready

Checks whether the service can receive traffic. This should check dependencies such as PostgreSQL, Redis and SQS.

### /metrics

Prometheus metrics endpoint.

## api-gateway

Public endpoints:

```text
POST /api/register
POST /api/login
POST /api/orders
GET /api/orders/{order_id}
POST /api/payments/{order_id}
```

Environment variables:

```text
AUTH_SERVICE_URL
ORDER_SERVICE_URL
PAYMENT_SERVICE_URL
SERVICE_NAME
ENVIRONMENT
```

## auth-service

Endpoints:

```text
POST /register
POST /login
GET /users/{user_id}
```

Uses:

```text
PostgreSQL
Redis
```

Environment variables:

```text
DATABASE_URL
REDIS_URL
SERVICE_NAME
ENVIRONMENT
```

## order-service

Endpoints:

```text
POST /orders
GET /orders/{order_id}
GET /orders
```

Uses:

```text
PostgreSQL
Redis
SQS
```

Environment variables:

```text
DATABASE_URL
REDIS_URL
ORDER_EVENTS_QUEUE_URL
AWS_REGION
SQS_ENDPOINT_URL optional
SERVICE_NAME
ENVIRONMENT
```

## payment-service

Endpoints:

```text
POST /payments/{order_id}
GET /payments/{payment_id}
```

Uses:

```text
PostgreSQL
SQS
```

Environment variables:

```text
DATABASE_URL
NOTIFICATION_EVENTS_QUEUE_URL
AWS_REGION
SQS_ENDPOINT_URL optional
SERVICE_NAME
ENVIRONMENT
```

## notification-worker

Worker behaviour:

```text
Poll SQS
Parse JSON message
Save notification to PostgreSQL
Delete message after successful processing
Do not delete message after failed processing
Expose health and metrics server
```

Environment variables:

```text
DATABASE_URL
NOTIFICATION_EVENTS_QUEUE_URL
AWS_REGION
SQS_ENDPOINT_URL optional
WORKER_POLL_INTERVAL_SECONDS
SERVICE_NAME
ENVIRONMENT
```
