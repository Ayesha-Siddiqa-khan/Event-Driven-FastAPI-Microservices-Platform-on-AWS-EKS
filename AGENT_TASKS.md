# AGENT_TASKS.md

# Tasks for the FastAPI Coding Agent

This file is for the coding agent only. The agent should work on **application code** and should not create infrastructure or deployment files.

## Main rule

The agent is responsible for building and improving the FastAPI microservices application.

The agent must not create these files:

```text
Dockerfile
docker-compose.yml
Terraform files
Kubernetes YAML files
Helm charts
GitHub Actions workflows
AWS infrastructure scripts
Argo CD applications
KEDA ScaledObject files
Prometheus/Grafana deployment files
```

You, the DevOps engineer, will create those separately.

---

## Agent output boundary

The agent may create or modify only these areas:

```text
apps/api-gateway/
apps/auth-service/
apps/order-service/
apps/payment-service/
apps/notification-worker/
docs/agent/
```

The agent may create:

```text
Python source files
FastAPI routes
Pydantic schemas
SQLAlchemy or SQLModel models
Alembic migration files
pytest tests
requirements.txt files
service README.md files
example .env documentation files
```

---

# Agent task order

## Task 1: Improve common service standards

Apply these standards to all services:

- structured JSON logging
- `/health` endpoint
- `/ready` endpoint
- `/metrics` endpoint
- environment-based configuration
- no hardcoded credentials
- clear exception handling
- consistent response format
- pytest health tests

Acceptance criteria:

```text
Every service starts independently.
Every service has /health.
Every service has /ready.
Every HTTP service has /metrics.
All configuration comes from environment variables.
No cloud credentials are hardcoded.
```

---

## Task 2: Build `auth-service`

Purpose: user registration and fake login.

Agent should implement:

```text
POST /register
POST /login
GET /users/{user_id}
GET /health
GET /ready
GET /metrics
```

Database:

```text
users
- id
- email
- password_hash
- created_at
```

Redis:

```text
session:{token} -> user_id
```

Readiness checks:

```text
PostgreSQL connection
Redis ping
```

Acceptance criteria:

```text
/register creates a user in PostgreSQL.
/login creates a fake session token in Redis.
/users/{user_id} returns a user.
/ready fails if PostgreSQL or Redis is unavailable.
```

---

## Task 3: Build `order-service`

Purpose: create and read orders.

Agent should implement:

```text
POST /orders
GET /orders/{order_id}
GET /orders
GET /health
GET /ready
GET /metrics
```

Database:

```text
orders
- id
- user_id
- amount
- status
- created_at
```

Redis:

```text
order:{order_id} -> order JSON
```

SQS:

Publish message to `ORDER_EVENTS_QUEUE_URL` after order creation.

Message format:

```json
{
  "event_type": "order_created",
  "order_id": "1",
  "user_id": "5",
  "amount": 100
}
```

Readiness checks:

```text
PostgreSQL connection
Redis ping
SQS queue access
```

Acceptance criteria:

```text
POST /orders stores an order in PostgreSQL.
POST /orders stores/retrieves order cache in Redis.
POST /orders publishes an order_created message to SQS.
/ready fails if database, Redis, or SQS is unavailable.
```

---

## Task 4: Build `payment-service`

Purpose: simulate order payment and publish payment notification events.

Agent should implement:

```text
POST /payments/{order_id}
GET /payments/{payment_id}
GET /health
GET /ready
GET /metrics
```

Database:

```text
payments
- id
- order_id
- amount
- status
- created_at
```

SQS:

Publish message to `NOTIFICATION_EVENTS_QUEUE_URL`.

Message format:

```json
{
  "event_type": "payment_completed",
  "order_id": "1",
  "payment_id": "10",
  "status": "success"
}
```

Readiness checks:

```text
PostgreSQL connection
SQS queue access
```

Acceptance criteria:

```text
POST /payments/{order_id} creates a payment record.
The service publishes a payment_completed message to SQS.
/ready fails if PostgreSQL or SQS is unavailable.
```

---

## Task 5: Build `notification-worker`

Purpose: consume SQS notification messages and store notifications.

Agent should implement:

```text
Background SQS polling loop
GET /health
GET /ready
GET /metrics
```

Database:

```text
notifications
- id
- user_id nullable
- order_id
- message
- status
- created_at
```

Worker behaviour:

```text
Poll NOTIFICATION_EVENTS_QUEUE_URL.
Receive messages.
Parse message JSON.
Save notification to PostgreSQL.
Delete the SQS message only after successful processing.
If processing fails, do not delete the message.
Expose processed and failed message metrics.
Support graceful shutdown.
```

Acceptance criteria:

```text
Worker consumes SQS messages.
Worker saves notification records.
Worker deletes messages only after success.
Worker exposes metrics for processed and failed messages.
/ready fails if PostgreSQL or SQS is unavailable.
```

---

## Task 6: Build `api-gateway`

Purpose: one public HTTP entry point that forwards traffic to internal services.

Agent should implement:

```text
POST /api/register -> auth-service /register
POST /api/login -> auth-service /login
POST /api/orders -> order-service /orders
GET /api/orders/{order_id} -> order-service /orders/{order_id}
POST /api/payments/{order_id} -> payment-service /payments/{order_id}
GET /health
GET /ready
GET /metrics
```

Readiness checks:

```text
auth-service reachable
order-service reachable
payment-service reachable
```

Acceptance criteria:

```text
Gateway forwards requests correctly.
Gateway returns useful errors if an internal service is unavailable.
/ready fails if required internal services are unavailable.
```

---

## Task 7: Tests the agent should add

The agent should add tests for:

```text
/health returns 200
/ready returns expected status when dependencies are mocked
register endpoint validates input
order endpoint validates input
SQS publish function can be mocked
worker processing function can be tested without real AWS
```

The agent should not require real AWS services for unit tests.

---

## Task 8: Documentation the agent should maintain

Each service README should explain:

```text
What the service does
Endpoints
Environment variables
Database tables
Redis keys if used
SQS messages if used
How to run locally
How to run tests
Expected health/readiness output
```

---

# Agent completion checklist

Before the agent says the application code is ready, it must satisfy this checklist:

```text
[ ] All services have requirements.txt.
[ ] All services have README.md.
[ ] All services have /health.
[ ] All services have /ready.
[ ] HTTP services have /metrics.
[ ] Database services have Alembic migrations.
[ ] SQS code supports SQS_ENDPOINT_URL for LocalStack.
[ ] No secret is hardcoded.
[ ] Tests exist for basic health and key logic.
[ ] Code can be containerised by the DevOps engineer without changing app logic.
```
