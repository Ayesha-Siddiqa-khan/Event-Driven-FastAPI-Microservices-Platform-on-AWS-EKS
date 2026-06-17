# App Summary and Expected Output

This document explains, in simple words, what this application does, what each service is responsible for, and what output you should expect when the system is working.

## One-line project summary

This project is an **event-driven FastAPI microservices platform** designed for DevOps practice. It uses HTTP APIs, PostgreSQL, Redis, AWS SQS, and a background worker so you can practise real deployment patterns on AWS EKS using Terraform, Helm, GitHub Actions, monitoring, autoscaling, and rollback.

## What problem this app solves

The app simulates a small order and payment system.

A user can:

1. Register.
2. Log in.
3. Create an order.
4. Trigger a payment.
5. Generate a notification after payment.

The business logic is intentionally simple. The real purpose is to give you a realistic system to deploy and operate.

## Main learning goal

This application helps you practise deployment of different workload types:

| Workload type | Example in this project | What you learn |
|---|---|---|
| Public HTTP API | `api-gateway` | Ingress, routing, public access, smoke testing |
| Internal HTTP APIs | `auth-service`, `order-service`, `payment-service` | Internal Kubernetes services, readiness probes, service-to-service communication |
| Database-backed service | `auth-service`, `order-service`, `payment-service`, `notification-worker` | PostgreSQL, migrations, secrets, database readiness checks |
| Cache-backed service | `auth-service`, `order-service` | Redis configuration, session/cache checks |
| Queue publisher | `order-service`, `payment-service` | AWS SQS integration and IAM permissions |
| Background worker | `notification-worker` | Queue consumption, worker deployment, KEDA autoscaling, no public ingress |
| Observable service | All services | `/health`, `/ready`, `/metrics`, logs, dashboards |

## Services included

| Service | What it does | Main output |
|---|---|---|
| `api-gateway` | Public entry point that forwards requests to internal services | Unified `/api/...` endpoints |
| `auth-service` | Registers users and creates login sessions | User records in PostgreSQL and session keys in Redis |
| `order-service` | Creates and reads orders | Order records in PostgreSQL, order cache in Redis, order event in SQS |
| `payment-service` | Simulates payment for an order | Payment record in PostgreSQL and payment event in SQS |
| `notification-worker` | Reads payment events from SQS and saves notifications | Notification records in PostgreSQL and worker metrics |

## Simple application flow

```text
Client
  ↓
api-gateway
  ↓
auth-service creates user and login token
  ↓
api-gateway sends order request
  ↓
order-service saves order in PostgreSQL
  ↓
order-service caches order in Redis
  ↓
order-service publishes order_created event to SQS
  ↓
api-gateway sends payment request
  ↓
payment-service saves payment in PostgreSQL
  ↓
payment-service publishes payment_completed event to SQS
  ↓
notification-worker consumes payment_completed event
  ↓
notification-worker saves notification in PostgreSQL
```

## Expected output from each service

### 1. Health endpoint

Every service has a `/health` endpoint.

Example request:

```bash
curl http://localhost:8002/health
```

Example output:

```json
{
  "status": "ok",
  "service": "order-service",
  "environment": "dev"
}
```

Meaning:

- The process is running.
- The service can respond to HTTP requests.
- This is suitable for Kubernetes liveness probes.

### 2. Readiness endpoint

Every service has a `/ready` endpoint.

Example request for `order-service`:

```bash
curl http://localhost:8002/ready
```

Successful output:

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

Failed output example:

```json
{
  "status": "not_ready",
  "checks": {
    "postgres": "ok",
    "redis": "failed",
    "sqs": "ok"
  }
}
```

Meaning:

- `/health` checks whether the process is alive.
- `/ready` checks whether the service can safely receive traffic.
- In Kubernetes, a pod should not receive traffic when `/ready` fails.

### 3. Metrics endpoint

Every service exposes `/metrics` for Prometheus.

Example request:

```bash
curl http://localhost:8002/metrics
```

Example output format:

```text
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{handler="/orders",method="POST",status="201"} 10
```

You should use this output later in Prometheus and Grafana.

## Expected business API outputs

### Register user

Through `api-gateway`:

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"password123"}'
```

Expected output:

```json
{
  "id": 1,
  "email": "demo@example.com",
  "created_at": "2026-06-17T10:00:00Z"
}
```

What happens internally:

- `api-gateway` forwards the request to `auth-service`.
- `auth-service` saves the user in PostgreSQL.

Expected PostgreSQL table output:

```text
users
+----+------------------+---------------+----------------------+
| id | email            | password_hash | created_at           |
+----+------------------+---------------+----------------------+
| 1  | demo@example.com | ********      | 2026-06-17 10:00:00  |
+----+------------------+---------------+----------------------+
```

### Login user

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"password123"}'
```

Expected output:

```json
{
  "token": "2c761af2-2c3e-4d34-8a02-111111111111",
  "user_id": 1
}
```

What happens internally:

- `auth-service` checks PostgreSQL for the user.
- `auth-service` creates a fake session token.
- The token is stored in Redis.

Expected Redis key:

```text
session:2c761af2-2c3e-4d34-8a02-111111111111 -> 1
```

### Create order

```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":100.50}'
```

Expected output:

```json
{
  "id": 1,
  "user_id": 1,
  "amount": 100.50,
  "status": "created",
  "created_at": "2026-06-17T10:05:00Z"
}
```

What happens internally:

- `api-gateway` forwards the request to `order-service`.
- `order-service` saves the order in PostgreSQL.
- `order-service` caches the order in Redis.
- `order-service` publishes an `order_created` message to SQS.

Expected PostgreSQL table output:

```text
orders
+----+---------+--------+---------+----------------------+
| id | user_id | amount | status  | created_at           |
+----+---------+--------+---------+----------------------+
| 1  | 1       | 100.50 | created | 2026-06-17 10:05:00  |
+----+---------+--------+---------+----------------------+
```

Expected Redis key:

```text
order:1 -> {"id":1,"user_id":1,"amount":"100.50","status":"created"}
```

Expected SQS message in `order-events-queue`:

```json
{
  "event_type": "order_created",
  "order_id": "1",
  "user_id": "1",
  "amount": "100.50"
}
```

### Get order

```bash
curl http://localhost:8000/api/orders/1
```

Expected output:

```json
{
  "id": 1,
  "user_id": 1,
  "amount": "100.50",
  "status": "created",
  "created_at": "2026-06-17T10:05:00Z"
}
```

What happens internally:

- `order-service` first checks Redis cache.
- If Redis has the order, it returns quickly from cache.
- If Redis does not have the order, it reads from PostgreSQL and stores it again in Redis.

This is useful for monitoring cache hit and miss behaviour.

### Create payment

```bash
curl -X POST http://localhost:8000/api/payments/1 \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":100.50}'
```

Expected output:

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

The status can be either:

```text
success
failed
```

What happens internally:

- `payment-service` creates a payment record in PostgreSQL.
- `payment-service` publishes a `payment_completed` event to SQS.

Expected PostgreSQL table output:

```text
payments
+----+----------+---------+--------+---------+----------------------+
| id | order_id | user_id | amount | status  | created_at           |
+----+----------+---------+--------+---------+----------------------+
| 1  | 1        | 1       | 100.50 | success | 2026-06-17 10:06:00  |
+----+----------+---------+--------+---------+----------------------+
```

Expected SQS message in `notification-events-queue`:

```json
{
  "event_type": "payment_completed",
  "order_id": "1",
  "payment_id": "1",
  "status": "success",
  "user_id": "1"
}
```

### Notification worker output

The `notification-worker` continuously polls the `notification-events-queue`.

When it receives the payment event, it saves a notification record.

Expected PostgreSQL table output:

```text
notifications
+----+---------+----------+-------------------------------------+---------+----------------------+
| id | user_id | order_id | message                             | status  | created_at           |
+----+---------+----------+-------------------------------------+---------+----------------------+
| 1  | 1       | 1        | Payment status for order 1: success | created | 2026-06-17 10:06:10  |
+----+---------+----------+-------------------------------------+---------+----------------------+
```

Expected worker logs:

```json
{"level":"INFO","message":"notification-worker started"}
{"level":"INFO","message":"processed notification event","order_id":1}
```

If processing fails, the message is not deleted from SQS. This allows retry behaviour and is useful for failure testing.

## Expected deployment output on Kubernetes

After you create Dockerfiles, Helm charts, and Terraform yourself, the deployed system should show this kind of output.

### Expected pods

```text
api-gateway-xxxxx                 Running
auth-service-xxxxx                Running
order-service-xxxxx               Running
payment-service-xxxxx             Running
notification-worker-xxxxx         Running
```

### Expected Kubernetes services

```text
api-gateway        LoadBalancer or ClusterIP behind Ingress
auth-service       ClusterIP
order-service      ClusterIP
payment-service    ClusterIP
```

The `notification-worker` should not have public ingress. It may have an internal service only if you need to scrape `/metrics`.

### Expected ingress behaviour

Only `api-gateway` should be public.

Example public paths:

```text
/api/register
/api/login
/api/orders
/api/orders/{order_id}
/api/payments/{order_id}
```

Internal services should not be directly public.

## Expected AWS output

When your infrastructure is deployed correctly, you should see resources similar to these:

```text
ECR repositories:
- edfp-dev-api-gateway
- edfp-dev-auth-service
- edfp-dev-order-service
- edfp-dev-payment-service
- edfp-dev-notification-worker

SQS queues:
- edfp-dev-order-events
- edfp-dev-notification-events
- edfp-dev-order-events-dlq
- edfp-dev-notification-events-dlq

RDS:
- edfp-dev-rds-postgres

ElastiCache:
- edfp-dev-redis-main

Secrets Manager:
- /edfp/dev/auth-service/database-url
- /edfp/dev/order-service/database-url
- /edfp/dev/order-service/redis-url
- /edfp/dev/payment-service/database-url
- /edfp/dev/notification-worker/database-url
```

## Expected monitoring output

In Grafana, you should aim to show these panels:

| Dashboard panel | Expected result |
|---|---|
| Request rate by service | Increases when you call APIs |
| p95 latency | Shows API response time |
| HTTP error rate | Increases when you simulate bad releases |
| Pod CPU and memory | Changes during load testing |
| Queue depth | Increases when many events are published |
| Worker processed messages | Increases when worker consumes SQS messages |
| Worker failed messages | Increases during failure lab |
| PostgreSQL readiness failures | Increases when DB connection is broken |
| Redis readiness failures | Increases when Redis connection is broken |

## Expected autoscaling output

When you add KEDA and send many messages to `notification-events-queue`, you should see:

```text
Queue depth increases
↓
KEDA detects queue depth
↓
notification-worker replicas increase
↓
worker processes messages
↓
queue depth decreases
↓
worker replicas scale down
```

Example expected result:

```text
Before load:
notification-worker replicas: 1
queue messages: 0

During load:
notification-worker replicas: 3-5
queue messages: 100+

After processing:
notification-worker replicas: 1
queue messages: 0
```

## Expected rollback output

When you deploy a bad version, your pipeline should show:

```text
1. New image deployed
2. Smoke test started
3. /ready or business endpoint failed
4. Helm rollback triggered
5. Previous working version restored
6. Smoke test passed after rollback
```

This is one of the most important outputs for your portfolio.

## Final output of the complete project

When the project is complete, you should be able to demonstrate:

1. A public API endpoint through `api-gateway`.
2. Internal microservices communicating inside Kubernetes.
3. PostgreSQL storing users, orders, payments, and notifications.
4. Redis storing sessions and cached orders.
5. SQS carrying events between services.
6. A background worker consuming queue messages.
7. KEDA scaling the worker from queue depth.
8. Prometheus scraping `/metrics` from services.
9. Grafana dashboards showing API, worker, queue, and database behaviour.
10. GitHub Actions building images, running migrations, deploying services, and rolling back failed releases.
11. AWS infrastructure created by Terraform.
12. Proper documentation with screenshots and failure labs.

## Recruiter-friendly explanation

You can describe this project like this:

> I built and deployed an event-driven FastAPI microservices platform on AWS EKS. The system includes public and internal HTTP services, PostgreSQL-backed services, Redis caching, AWS SQS event queues, a background notification worker, Prometheus/Grafana monitoring, queue-based autoscaling with KEDA, database migrations, environment-based Helm values, and rollback testing through GitHub Actions.

