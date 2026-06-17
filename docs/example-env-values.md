# Example Environment Values

These are examples only. Do not commit real secrets.

## api-gateway

```text
AUTH_SERVICE_URL=http://auth-service:8001
ORDER_SERVICE_URL=http://order-service:8002
PAYMENT_SERVICE_URL=http://payment-service:8003
SERVICE_NAME=api-gateway
ENVIRONMENT=dev
```

## auth-service

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/devops_lab
REDIS_URL=redis://HOST:6379/0
SERVICE_NAME=auth-service
ENVIRONMENT=dev
SESSION_TTL_SECONDS=3600
```

## order-service

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/devops_lab
REDIS_URL=redis://HOST:6379/0
ORDER_EVENTS_QUEUE_URL=https://sqs.REGION.amazonaws.com/ACCOUNT/order-events-queue
AWS_REGION=us-east-1
SQS_ENDPOINT_URL=
SERVICE_NAME=order-service
ENVIRONMENT=dev
```

## payment-service

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/devops_lab
NOTIFICATION_EVENTS_QUEUE_URL=https://sqs.REGION.amazonaws.com/ACCOUNT/notification-events-queue
AWS_REGION=us-east-1
SQS_ENDPOINT_URL=
SERVICE_NAME=payment-service
ENVIRONMENT=dev
PAYMENT_FAILURE_RATE=0.0
```

## notification-worker

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/devops_lab
NOTIFICATION_EVENTS_QUEUE_URL=https://sqs.REGION.amazonaws.com/ACCOUNT/notification-events-queue
AWS_REGION=us-east-1
SQS_ENDPOINT_URL=
WORKER_POLL_INTERVAL_SECONDS=2
SERVICE_NAME=notification-worker
ENVIRONMENT=dev
```
