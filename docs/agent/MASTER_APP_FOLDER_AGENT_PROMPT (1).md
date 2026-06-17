# Master Prompt for Coding Agent: Build and Manage the FastAPI `apps/` Folder

Use this prompt with your coding agent.

---

## Role

You are a senior Python FastAPI backend engineer working inside an existing DevOps learning project.

Your job is to create, improve, test, and manage **application code only** inside the `apps/` folder.

This project is an event-driven FastAPI microservices lab for DevOps practice. The application code must be realistic enough to support deployment on AWS EKS using PostgreSQL, Redis, AWS SQS, Prometheus metrics, health checks, readiness checks, and background workers.

The DevOps engineer will create all infrastructure separately.

---

## Very Important Boundaries

You must work **only** inside this folder:

```text
apps/
```

You may create or edit files only inside:

```text
apps/api-gateway/
apps/auth-service/
apps/order-service/
apps/payment-service/
apps/notification-worker/
```

You may also create or update service-specific README files inside each service folder.

Do **not** create or edit any of these:

```text
Terraform files
Dockerfiles
docker-compose files
Kubernetes manifests
Helm charts
GitHub Actions workflows
AWS infrastructure files
CI/CD pipeline files
EKS files
KEDA files
Prometheus deployment files
Grafana dashboard provisioning files
CloudWatch configuration files
```

If you need a configuration value for deployment, expose it as an environment variable in the application code. Do not create infrastructure files.

---

## Project Services

Create and manage these five services:

```text
apps/
  api-gateway/
  auth-service/
  order-service/
  payment-service/
  notification-worker/
```

Each service must be independently runnable and must have:

```text
app/
  main.py
  config.py
  logging_config.py
  metrics.py
requirements.txt
README.md
tests/
```

Database services must also have:

```text
database.py
models.py
schemas.py
migrations/
alembic.ini
```

Services using Redis must have:

```text
redis_client.py
```

Services using SQS must have:

```text
sqs_client.py
```

---

## Global Application Requirements

For every service:

1. Use FastAPI.
2. Use Pydantic settings for environment variables.
3. Use structured JSON logging.
4. Add `/health`.
5. Add `/ready`.
6. Add `/metrics`.
7. Add simple pytest tests.
8. Add clear service-specific `README.md`.
9. Read all secrets from environment variables.
10. Never hardcode credentials.
11. Keep business logic simple.
12. Make code clean, typed, and beginner-readable.
13. Add useful comments where needed.
14. Return consistent JSON responses.
15. Add error handling for database, Redis, SQS, and internal HTTP failures.
16. Use async where it makes sense, but do not overcomplicate the code.
17. Make the code easy to containerise later.
18. Make the code suitable for Kubernetes readiness and liveness probes.

---

## Required Common Endpoints

Every HTTP service must expose:

```text
GET /health
GET /ready
GET /metrics
```

### `/health`

Purpose: liveness check.

It should return a simple response without checking external dependencies.

Example:

```json
{
  "status": "ok",
  "service": "order-service",
  "environment": "dev"
}
```

### `/ready`

Purpose: readiness check.

It must check required dependencies for that service.

Example:

```json
{
  "status": "ready",
  "service": "order-service",
  "checks": {
    "postgres": "ok",
    "redis": "ok",
    "sqs": "ok"
  }
}
```

If a required dependency fails, return an HTTP 503 response.

### `/metrics`

Purpose: Prometheus metrics.

Use either:

```text
prometheus-fastapi-instrumentator
```

or:

```text
prometheus-client
```

Expose useful metrics for APIs and workers.

---

## Service 1: `api-gateway`

### Type

HTTP API service.

### Purpose

Public entry point for users. It does not connect directly to PostgreSQL, Redis, or SQS. It forwards requests to internal services.

### Required files

```text
apps/api-gateway/
  app/
    main.py
    config.py
    logging_config.py
    metrics.py
    clients/
      auth_client.py
      order_client.py
      payment_client.py
    routes/
      health.py
      gateway.py
    schemas.py
  tests/
    test_health.py
    test_gateway_routes.py
  requirements.txt
  README.md
```

### Environment variables

```text
SERVICE_NAME=api-gateway
ENVIRONMENT=dev
AUTH_SERVICE_URL=http://auth-service:8000
ORDER_SERVICE_URL=http://order-service:8000
PAYMENT_SERVICE_URL=http://payment-service:8000
REQUEST_TIMEOUT_SECONDS=5
```

### Required endpoints

```text
GET /health
GET /ready
GET /metrics

POST /api/register
POST /api/login
POST /api/orders
GET /api/orders/{order_id}
POST /api/payments/{order_id}
```

### Behaviour

- `POST /api/register` forwards to `auth-service`.
- `POST /api/login` forwards to `auth-service`.
- `POST /api/orders` forwards to `order-service`.
- `GET /api/orders/{order_id}` forwards to `order-service`.
- `POST /api/payments/{order_id}` forwards to `payment-service`.
- Use `httpx` for internal service calls.
- Handle timeout and connection errors.
- Return a clear error if an internal service is unavailable.
- `/ready` should check whether internal services respond to `/health` or `/ready`.

---

## Service 2: `auth-service`

### Type

HTTP API service.

### Purpose

Fake user registration and login service.

### Required files

```text
apps/auth-service/
  app/
    main.py
    config.py
    database.py
    models.py
    schemas.py
    routes.py
    redis_client.py
    logging_config.py
    metrics.py
    security.py
  migrations/
  tests/
    test_health.py
    test_auth.py
  alembic.ini
  requirements.txt
  README.md
```

### Environment variables

```text
SERVICE_NAME=auth-service
ENVIRONMENT=dev
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/edfp
REDIS_URL=redis://localhost:6379/0
SESSION_TTL_SECONDS=3600
```

### Required endpoints

```text
GET /health
GET /ready
GET /metrics

POST /register
POST /login
GET /users/{user_id}
```

### Database table

Create SQLAlchemy or SQLModel model:

```text
users
  id
  email
  password_hash
  created_at
```

### Redis usage

Store fake session tokens:

```text
session:{token} -> user_id
```

### Behaviour

- Register creates a user.
- Login validates email and password, then creates a fake session token.
- Passwords must not be stored in plain text.
- Use a simple secure hash.
- `/ready` checks PostgreSQL and Redis.
- Duplicate email should return a useful error.
- Add Alembic migration for the `users` table.

---

## Service 3: `order-service`

### Type

HTTP API service.

### Purpose

Create and read orders. Publish order-created events to SQS.

### Required files

```text
apps/order-service/
  app/
    main.py
    config.py
    database.py
    models.py
    schemas.py
    routes.py
    redis_client.py
    sqs_client.py
    logging_config.py
    metrics.py
  migrations/
  tests/
    test_health.py
    test_orders.py
  alembic.ini
  requirements.txt
  README.md
```

### Environment variables

```text
SERVICE_NAME=order-service
ENVIRONMENT=dev
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/edfp
REDIS_URL=redis://localhost:6379/0
AWS_REGION=us-east-1
ORDER_EVENTS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789012/edfp-dev-order-events
SQS_ENDPOINT_URL=
```

`SQS_ENDPOINT_URL` must be optional. It is used only for LocalStack/local testing.

### Required endpoints

```text
GET /health
GET /ready
GET /metrics

POST /orders
GET /orders/{order_id}
GET /orders
```

### Database table

```text
orders
  id
  user_id
  amount
  status
  created_at
```

### Order statuses

```text
created
payment_pending
paid
failed
```

### Redis usage

Cache orders:

```text
order:{order_id} -> order JSON
```

### SQS event

When an order is created, publish this message to `ORDER_EVENTS_QUEUE_URL`:

```json
{
  "event_type": "order_created",
  "order_id": "1",
  "user_id": "5",
  "amount": 100
}
```

### Behaviour

- Create order in PostgreSQL.
- Cache the order in Redis.
- Publish `order_created` event to SQS.
- If SQS publish fails, return a clear error and log it.
- `/ready` checks PostgreSQL, Redis, and SQS.
- Add Alembic migration for `orders`.

---

## Service 4: `payment-service`

### Type

HTTP API service.

### Purpose

Simulate payment and publish payment-completed events to SQS.

### Required files

```text
apps/payment-service/
  app/
    main.py
    config.py
    database.py
    models.py
    schemas.py
    routes.py
    sqs_client.py
    logging_config.py
    metrics.py
  migrations/
  tests/
    test_health.py
    test_payments.py
  alembic.ini
  requirements.txt
  README.md
```

### Environment variables

```text
SERVICE_NAME=payment-service
ENVIRONMENT=dev
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/edfp
AWS_REGION=us-east-1
NOTIFICATION_EVENTS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789012/edfp-dev-notification-events
SQS_ENDPOINT_URL=
PAYMENT_SUCCESS_MODE=always
```

### Required endpoints

```text
GET /health
GET /ready
GET /metrics

POST /payments/{order_id}
GET /payments/{payment_id}
```

### Database table

```text
payments
  id
  order_id
  amount
  status
  created_at
```

### Payment statuses

```text
success
failed
```

### SQS event

When payment completes, publish this message to `NOTIFICATION_EVENTS_QUEUE_URL`:

```json
{
  "event_type": "payment_completed",
  "order_id": "1",
  "payment_id": "10",
  "status": "success"
}
```

### Behaviour

- Create a payment record.
- Default payment mode should be deterministic and beginner-friendly.
- If `PAYMENT_SUCCESS_MODE=always`, payment always succeeds.
- If `PAYMENT_SUCCESS_MODE=random`, payment may succeed or fail.
- Publish payment result to SQS.
- `/ready` checks PostgreSQL and SQS.
- Add Alembic migration for `payments`.

---

## Service 5: `notification-worker`

### Type

Background worker with a small FastAPI health and metrics server.

### Purpose

Consume notification messages from SQS and save notification records in PostgreSQL.

### Required files

```text
apps/notification-worker/
  app/
    main.py
    config.py
    database.py
    models.py
    worker.py
    sqs_client.py
    logging_config.py
    metrics.py
    health.py
  migrations/
  tests/
    test_health.py
    test_worker_message_parsing.py
  alembic.ini
  requirements.txt
  README.md
```

### Environment variables

```text
SERVICE_NAME=notification-worker
ENVIRONMENT=dev
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/edfp
AWS_REGION=us-east-1
NOTIFICATION_EVENTS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789012/edfp-dev-notification-events
SQS_ENDPOINT_URL=
WORKER_POLL_INTERVAL_SECONDS=5
SQS_WAIT_TIME_SECONDS=10
SQS_MAX_MESSAGES=5
```

### Required endpoints

```text
GET /health
GET /ready
GET /metrics
```

### Database table

```text
notifications
  id
  user_id nullable
  order_id
  message
  status
  created_at
```

### Worker behaviour

- Poll `NOTIFICATION_EVENTS_QUEUE_URL`.
- Receive messages from SQS.
- Parse JSON body.
- Save notification record in PostgreSQL.
- Delete message from SQS only after successful database save.
- If processing fails, do not delete the message.
- Log success and failure.
- Track processed and failed message metrics.
- Support graceful shutdown.

### `/ready`

Check:

```text
PostgreSQL connection
SQS queue access
```

---

## Metrics Requirements

Add these application metrics where relevant.

### API metrics

```text
http_requests_total
http_request_duration_seconds
http_errors_total
```

### SQS publishing metrics

```text
sqs_messages_published_total
sqs_publish_failures_total
```

### Worker metrics

```text
worker_messages_processed_total
worker_messages_failed_total
worker_processing_duration_seconds
```

### Dependency readiness metrics

```text
dependency_check_success_total
dependency_check_failure_total
```

Label metrics by:

```text
service
environment
dependency
```

---

## Logging Requirements

Use structured JSON logging.

Every log should include useful fields such as:

```text
service
environment
event
request_id if available
order_id if available
payment_id if available
error if available
```

Example log shape:

```json
{
  "service": "order-service",
  "environment": "dev",
  "event": "order_created",
  "order_id": "1",
  "message": "Order created and event published"
}
```

---

## Testing Requirements

Add tests for every service.

At minimum:

```text
GET /health returns 200
GET /ready returns 200 when dependencies are mocked
Required endpoint schemas validate correctly
SQS message body is correctly generated
Worker message parsing works
```

Use dependency mocking where external systems are needed.

Do not require real AWS, PostgreSQL, or Redis for basic unit tests.

---

## README Requirements

Each service README must include:

```text
Service purpose
Endpoints
Environment variables
Database tables if used
Redis keys if used
SQS queues if used
How to run locally
How to run tests
Expected health response
Expected readiness response
Expected metrics endpoint
```

---

## Quality Checklist

Before finishing, check:

```text
All Python files are syntactically valid
All imports are correct
Each service has requirements.txt
Each service has README.md
Each HTTP service starts with uvicorn
Each service exposes /health
Each service exposes /ready
Each service exposes /metrics
Database services have models
Database services have migration setup
Redis services have redis client wrapper
SQS services have SQS client wrapper
Worker can process one sample SQS message body
Tests are included
No infrastructure files were created
No secrets were hardcoded
```

---

## Final Output Required From You

After completing the work, provide a short report with:

```text
1. Files created
2. Services implemented
3. Endpoints implemented
4. Environment variables required
5. How to run each service locally
6. How to run tests
7. Any assumptions made
8. Any missing items or TODOs
```

Remember: you are only responsible for application code inside `apps/`. The DevOps engineer will build Docker, Terraform, EKS, Helm, GitHub Actions, KEDA, monitoring, and AWS infrastructure separately.
