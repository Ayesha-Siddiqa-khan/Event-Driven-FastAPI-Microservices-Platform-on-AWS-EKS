# Agent and DevOps Workflow

This file explains how to use the coding agent without losing the DevOps learning value.

## Recommended workflow

Use this loop for each service.

```text
1. Give the agent one service task.
2. Agent creates or improves the FastAPI code only.
3. You run the service locally.
4. You write or update the Dockerfile.
5. You build the image.
6. You push the image to ECR.
7. You create or update the Helm chart.
8. You deploy to EKS.
9. You test /health and /ready.
10. You add monitoring and screenshot evidence.
```

Do not ask the agent to do all services and infrastructure at the same time. That will make the project difficult to debug.

---

# Best service-by-service sequence

## Round 1: `auth-service`

Agent does:

```text
FastAPI endpoints
PostgreSQL users table
Redis fake session
health/readiness/metrics
tests
```

You do:

```text
Dockerfile
ECR repository
RDS secret
Redis secret
Helm chart
migration job
EKS deployment
readiness probe
Grafana panel
```

Do not move to `order-service` until `auth-service` is deployed and healthy.

---

## Round 2: `order-service`

Agent does:

```text
order endpoints
PostgreSQL orders table
Redis order cache
SQS publish to order-events queue
metrics
tests
```

You do:

```text
Dockerfile
ECR repository
SQS order-events queue
IAM permission to send SQS message
Helm chart
migration job
EKS deployment
readiness probe checking DB, Redis and SQS
Grafana panels for latency and SQS publish failures
```

---

## Round 3: `payment-service`

Agent does:

```text
payment endpoints
PostgreSQL payments table
SQS publish to notification-events queue
metrics
tests
```

You do:

```text
Dockerfile
ECR repository
SQS notification-events queue
IAM permission to send SQS message
Helm chart
migration job
EKS deployment
readiness probe
rollback test with bad image
```

---

## Round 4: `notification-worker`

Agent does:

```text
background polling loop
SQS receive/delete logic
PostgreSQL notifications table
metrics server
processed/failed message metrics
graceful shutdown
tests with mocked SQS
```

You do:

```text
Dockerfile
ECR repository
IAM permission to receive/delete SQS messages
Helm chart without public ingress
KEDA ScaledObject
worker autoscaling test
Grafana worker dashboard
```

---

## Round 5: `api-gateway`

Agent does:

```text
public API routes
internal HTTP forwarding
error handling when internal services fail
health/readiness/metrics
tests
```

You do:

```text
Dockerfile
ECR repository
Ingress or AWS Load Balancer route
TLS later
Helm chart
public endpoint smoke tests
load test with k6
production-style README screenshots
```

---

# What to ask the agent each time

Use small prompts, for example:

```text
Improve only auth-service. Do not create Docker, Terraform, Helm, Kubernetes, or GitHub Actions files. Implement PostgreSQL users, Redis sessions, /health, /ready, /metrics, Alembic migration, and basic tests.
```

After that is working:

```text
Improve only order-service. Do not create infrastructure files. Implement PostgreSQL orders, Redis order cache, SQS order_created publishing with SQS_ENDPOINT_URL support, readiness checks, metrics, Alembic migration, and tests.
```

This method helps you learn each DevOps dependency one at a time.
