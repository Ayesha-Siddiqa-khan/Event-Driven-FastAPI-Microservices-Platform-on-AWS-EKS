# Service-by-Service Prompts for Your Coding Agent

Use these prompts one by one. Do not send all prompts at once.

---

## Prompt 1: `auth-service`

```text
Improve only apps/auth-service. Do not create Dockerfiles, docker-compose, Terraform, Kubernetes YAML, Helm charts, GitHub Actions, or cloud infrastructure files.

Implement a production-style FastAPI auth-service for a DevOps lab.

Required features:
- GET /health
- GET /ready
- GET /metrics
- POST /register
- POST /login
- GET /users/{user_id}
- PostgreSQL users table using SQLAlchemy or SQLModel
- Alembic migration for users table
- Redis fake session storage using key session:{token}
- Pydantic settings from environment variables
- structured JSON logging
- basic error handling
- pytest tests for /health and basic validation

Environment variables:
- DATABASE_URL
- REDIS_URL
- SERVICE_NAME
- ENVIRONMENT

Readiness must check PostgreSQL and Redis.
```

---

## Prompt 2: `order-service`

```text
Improve only apps/order-service. Do not create Dockerfiles, docker-compose, Terraform, Kubernetes YAML, Helm charts, GitHub Actions, or cloud infrastructure files.

Implement a production-style FastAPI order-service for a DevOps lab.

Required features:
- GET /health
- GET /ready
- GET /metrics
- POST /orders
- GET /orders/{order_id}
- GET /orders
- PostgreSQL orders table
- Alembic migration for orders table
- Redis cache using key order:{order_id}
- boto3 SQS client
- SQS_ENDPOINT_URL support for LocalStack
- Publish order_created message to ORDER_EVENTS_QUEUE_URL after order creation
- structured JSON logging
- metrics for orders created, SQS publish success, and SQS publish failure
- pytest tests with SQS mocked

Environment variables:
- DATABASE_URL
- REDIS_URL
- ORDER_EVENTS_QUEUE_URL
- AWS_REGION
- SQS_ENDPOINT_URL optional
- SERVICE_NAME
- ENVIRONMENT

Readiness must check PostgreSQL, Redis, and SQS queue access.
```

---

## Prompt 3: `payment-service`

```text
Improve only apps/payment-service. Do not create Dockerfiles, docker-compose, Terraform, Kubernetes YAML, Helm charts, GitHub Actions, or cloud infrastructure files.

Implement a production-style FastAPI payment-service for a DevOps lab.

Required features:
- GET /health
- GET /ready
- GET /metrics
- POST /payments/{order_id}
- GET /payments/{payment_id}
- PostgreSQL payments table
- Alembic migration for payments table
- boto3 SQS client
- SQS_ENDPOINT_URL support for LocalStack
- Publish payment_completed message to NOTIFICATION_EVENTS_QUEUE_URL
- structured JSON logging
- metrics for payments created, SQS publish success, and SQS publish failure
- pytest tests with SQS mocked

Environment variables:
- DATABASE_URL
- NOTIFICATION_EVENTS_QUEUE_URL
- AWS_REGION
- SQS_ENDPOINT_URL optional
- SERVICE_NAME
- ENVIRONMENT

Readiness must check PostgreSQL and SQS queue access.
```

---

## Prompt 4: `notification-worker`

```text
Improve only apps/notification-worker. Do not create Dockerfiles, docker-compose, Terraform, Kubernetes YAML, Helm charts, GitHub Actions, or cloud infrastructure files.

Implement a production-style background notification worker for a DevOps lab.

Required features:
- Background SQS polling loop
- GET /health
- GET /ready
- GET /metrics
- PostgreSQL notifications table
- Alembic migration for notifications table
- boto3 SQS client
- SQS_ENDPOINT_URL support for LocalStack
- Receive messages from NOTIFICATION_EVENTS_QUEUE_URL
- Save notification record in PostgreSQL
- Delete SQS message only after successful processing
- Do not delete failed messages
- graceful shutdown
- metrics for processed messages, failed messages, and processing duration
- pytest tests with SQS mocked

Environment variables:
- DATABASE_URL
- NOTIFICATION_EVENTS_QUEUE_URL
- AWS_REGION
- SQS_ENDPOINT_URL optional
- WORKER_POLL_INTERVAL_SECONDS
- SERVICE_NAME
- ENVIRONMENT

Readiness must check PostgreSQL and SQS queue access.
```

---

## Prompt 5: `api-gateway`

```text
Improve only apps/api-gateway. Do not create Dockerfiles, docker-compose, Terraform, Kubernetes YAML, Helm charts, GitHub Actions, or cloud infrastructure files.

Implement a production-style FastAPI api-gateway for a DevOps lab.

Required features:
- GET /health
- GET /ready
- GET /metrics
- POST /api/register forwards to AUTH_SERVICE_URL/register
- POST /api/login forwards to AUTH_SERVICE_URL/login
- POST /api/orders forwards to ORDER_SERVICE_URL/orders
- GET /api/orders/{order_id} forwards to ORDER_SERVICE_URL/orders/{order_id}
- POST /api/payments/{order_id} forwards to PAYMENT_SERVICE_URL/payments/{order_id}
- httpx internal service client
- timeout handling
- useful error response when internal service is down
- structured JSON logging
- metrics for request count, latency, and upstream errors
- pytest tests with internal services mocked

Environment variables:
- AUTH_SERVICE_URL
- ORDER_SERVICE_URL
- PAYMENT_SERVICE_URL
- SERVICE_NAME
- ENVIRONMENT

Readiness must check auth-service, order-service, and payment-service reachability.
```
