# AWS Infrastructure Guide

This guide explains the AWS infrastructure you should build for the Event-Driven FastAPI Microservices Platform.

The repository intentionally does not include Terraform, Helm, Kubernetes YAML, Dockerfiles, or GitHub Actions workflows. You should create those yourself as hands-on DevOps practice. These documents tell you what to create, why each resource is needed, how to name it, and how the services should connect.

## Recommended beginner-friendly AWS stack

| Layer | AWS service / tool | Purpose |
|---|---|---|
| Remote Terraform state | S3 + DynamoDB | Store Terraform state and prevent concurrent state changes |
| Container registry | ECR | Store Docker images for each FastAPI service |
| Compute | EKS | Run API services and background worker on Kubernetes |
| Networking | VPC, subnets, route tables, NAT, security groups | Isolate public and private infrastructure |
| Public entry | AWS Load Balancer Controller + ALB | Expose only `api-gateway` publicly |
| Database | RDS PostgreSQL | Store users, orders, payments, notifications |
| Cache | ElastiCache Redis | Store sessions and order cache |
| Queue | SQS | Decouple order/payment/notification flow |
| Secrets | AWS Secrets Manager | Store database URL, Redis URL, JWT secret, app secrets |
| App AWS permissions | IRSA / EKS Pod Identity | Let pods access SQS and Secrets Manager safely |
| Observability | Prometheus + Grafana, then CloudWatch | Monitor app and infrastructure |
| DNS | Route 53 | Optional friendly domain name for the API |

## Start here

Read these files in order:

1. [`docs/infrastructure/00-naming-conventions.md`](docs/infrastructure/00-naming-conventions.md)
2. [`docs/infrastructure/01-environments-and-resource-inventory.md`](docs/infrastructure/01-environments-and-resource-inventory.md)
3. [`docs/infrastructure/02-networking-vpc.md`](docs/infrastructure/02-networking-vpc.md)
4. [`docs/infrastructure/03-terraform-remote-state.md`](docs/infrastructure/03-terraform-remote-state.md)
5. [`docs/infrastructure/04-ecr-container-registry.md`](docs/infrastructure/04-ecr-container-registry.md)
6. [`docs/infrastructure/05-eks-cluster.md`](docs/infrastructure/05-eks-cluster.md)
7. [`docs/infrastructure/06-rds-postgresql.md`](docs/infrastructure/06-rds-postgresql.md)
8. [`docs/infrastructure/07-elasticache-redis.md`](docs/infrastructure/07-elasticache-redis.md)
9. [`docs/infrastructure/08-sqs-queues.md`](docs/infrastructure/08-sqs-queues.md)
10. [`docs/infrastructure/09-secrets-manager.md`](docs/infrastructure/09-secrets-manager.md)
11. [`docs/infrastructure/10-iam-oidc-irsa.md`](docs/infrastructure/10-iam-oidc-irsa.md)
12. [`docs/infrastructure/11-load-balancer-dns-tls.md`](docs/infrastructure/11-load-balancer-dns-tls.md)
13. [`docs/infrastructure/12-observability.md`](docs/infrastructure/12-observability.md)
14. [`docs/infrastructure/13-deployment-order.md`](docs/infrastructure/13-deployment-order.md)
15. [`docs/infrastructure/14-dev-staging-prod-values.md`](docs/infrastructure/14-dev-staging-prod-values.md)
16. [`docs/infrastructure/15-cost-and-cleanup.md`](docs/infrastructure/15-cost-and-cleanup.md)
17. [`docs/infrastructure/16-recruiter-evidence-checklist.md`](docs/infrastructure/16-recruiter-evidence-checklist.md)

## Important rule

Do not create everything at once.

Build infrastructure in this sequence:

```text
S3 + DynamoDB for Terraform state
VPC
ECR
EKS
RDS PostgreSQL
ElastiCache Redis
SQS
Secrets Manager
IAM roles for service accounts
AWS Load Balancer Controller
Monitoring
Application deployments
KEDA autoscaling
Failure labs
```

This order helps you debug one layer at a time.
