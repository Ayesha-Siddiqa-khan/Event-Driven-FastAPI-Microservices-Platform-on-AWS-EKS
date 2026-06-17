# 13 - Deployment Order

Follow this order to avoid confusion.

## Infrastructure deployment order

```text
1. S3 bucket and DynamoDB table for Terraform state
2. VPC, subnets, route tables, NAT Gateway, security groups
3. ECR repositories
4. EKS cluster and node group
5. EKS add-ons and controllers
6. RDS PostgreSQL
7. ElastiCache Redis
8. SQS queues and DLQs
9. Secrets Manager secrets
10. IAM roles for GitHub Actions and service accounts
11. Prometheus and Grafana
12. AWS Load Balancer Controller ingress
13. KEDA
```

## Application deployment order

```text
1. auth-service
2. order-service
3. payment-service
4. notification-worker
5. api-gateway
```

## Why this order?

`auth-service` is simplest and teaches database + Redis.

`order-service` adds database + Redis + SQS publishing.

`payment-service` adds database + SQS publishing.

`notification-worker` adds background worker and SQS consuming.

`api-gateway` connects all internal services and becomes the public entry point.

## Per-service deployment flow

For each service:

```text
1. build image
2. push image to ECR
3. run database migration if needed
4. deploy or upgrade Helm release
5. wait for rollout
6. call /health
7. call /ready
8. run smoke test
9. rollback if smoke test fails
```

## Smoke tests

Auth service:

```text
POST /register
POST /login
```

Order service:

```text
POST /orders
GET /orders/{order_id}
```

Payment service:

```text
POST /payments/{order_id}
GET /payments/{payment_id}
```

Notification worker:

```text
send test message to SQS
confirm notification row is created
confirm message is deleted from queue
```

API gateway:

```text
POST /api/register
POST /api/orders
POST /api/payments/{order_id}
```

## Rollback logic

If smoke test fails:

```text
helm rollback <release-name>
```

Then verify:

```text
kubectl rollout status deployment/<deployment-name>
curl /health
curl /ready
```

Document this with screenshots for your portfolio.
