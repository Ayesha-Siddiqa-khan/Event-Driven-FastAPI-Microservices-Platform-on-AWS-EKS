# Your DevOps Checklists

Use this file while building the infrastructure and deployment side.

---

# Checklist 1: Before Docker

```text
[ ] I understand what each service does.
[ ] I can run at least one service locally.
[ ] I know required environment variables for every service.
[ ] I know which services need PostgreSQL.
[ ] I know which services need Redis.
[ ] I know which services need SQS.
[ ] I know which service is a background worker.
```

---

# Checklist 2: Docker

```text
[ ] Dockerfile created for api-gateway.
[ ] Dockerfile created for auth-service.
[ ] Dockerfile created for order-service.
[ ] Dockerfile created for payment-service.
[ ] Dockerfile created for notification-worker.
[ ] All images build successfully.
[ ] All images start using environment variables.
[ ] /health works from each running container.
```

---

# Checklist 3: AWS infrastructure

```text
[ ] S3 Terraform state bucket created.
[ ] DynamoDB Terraform lock table created.
[ ] VPC created.
[ ] Public and private subnets created.
[ ] EKS cluster created.
[ ] ECR repositories created.
[ ] RDS PostgreSQL created.
[ ] ElastiCache Redis created.
[ ] SQS queues created.
[ ] SQS DLQs created.
[ ] Secrets Manager secrets created.
[ ] IAM roles created.
[ ] OIDC/IRSA or Pod Identity configured.
```

---

# Checklist 4: Kubernetes and Helm

```text
[ ] Namespace created.
[ ] Helm chart created for api-gateway.
[ ] Helm chart created for auth-service.
[ ] Helm chart created for order-service.
[ ] Helm chart created for payment-service.
[ ] Helm chart created for notification-worker.
[ ] Readiness probe uses /ready.
[ ] Liveness probe uses /health.
[ ] Resource requests and limits are configured.
[ ] Only api-gateway is public.
[ ] Worker has no public ingress.
```

---

# Checklist 5: CI/CD

```text
[ ] Pull request workflow runs tests.
[ ] Build workflow builds all service images.
[ ] Images are pushed to ECR with Git SHA tags.
[ ] Migration step runs before deployment.
[ ] Helm deployment runs after migration.
[ ] Smoke test runs after deployment.
[ ] Failed smoke test triggers rollback.
[ ] Production requires manual approval.
```

---

# Checklist 6: Monitoring

```text
[ ] Prometheus scrapes /metrics.
[ ] Grafana dashboard shows API latency.
[ ] Grafana dashboard shows HTTP error rate.
[ ] Grafana dashboard shows worker processed messages.
[ ] Grafana dashboard shows worker failed messages.
[ ] SQS queue depth is visible.
[ ] PostgreSQL connection metric is visible.
[ ] Redis connection metric is visible.
[ ] CloudWatch logs collect pod logs.
[ ] At least one CloudWatch alarm is configured.
```

---

# Checklist 7: Autoscaling and failure labs

```text
[ ] HPA scales API services under load.
[ ] KEDA scales notification-worker from SQS queue depth.
[ ] Bad image rollback is tested.
[ ] Wrong database password failure is tested.
[ ] Redis unavailable failure is tested.
[ ] High queue depth failure is tested.
[ ] Pod crash recovery is tested.
[ ] Results are documented with screenshots.
```
