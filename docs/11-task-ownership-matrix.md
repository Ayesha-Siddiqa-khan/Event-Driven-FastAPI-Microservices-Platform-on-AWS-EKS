# Task Ownership Matrix

This file shows who should do each part of the project.

| Area | Coding agent | You, DevOps engineer |
|---|---:|---:|
| FastAPI route code | Yes | Review only |
| Pydantic schemas | Yes | Review only |
| SQLAlchemy/SQLModel models | Yes | Review only |
| Alembic migrations | Yes | Run in pipeline |
| PostgreSQL connection code | Yes | Provide RDS and secrets |
| Redis connection code | Yes | Provide ElastiCache and secrets |
| SQS client code | Yes | Create SQS queues and IAM permissions |
| Background worker code | Yes | Deploy and autoscale with KEDA |
| Unit tests | Yes | Run in CI |
| Service README files | Yes | Add deployment notes if needed |
| Dockerfiles | No | Yes |
| Docker build and image tagging | No | Yes |
| ECR repositories | No | Yes |
| Terraform modules | No | Yes |
| S3 remote state | No | Yes |
| DynamoDB lock table | No | Yes |
| VPC, subnets, NAT, routing | No | Yes |
| EKS cluster | No | Yes |
| RDS PostgreSQL | No | Yes |
| ElastiCache Redis | No | Yes |
| SQS queues and DLQs | No | Yes |
| Secrets Manager | No | Yes |
| IAM, OIDC, IRSA | No | Yes |
| Helm charts | No | Yes |
| Kubernetes probes/resources | No | Yes, using app endpoints |
| KEDA ScaledObject | No | Yes |
| Prometheus/Grafana install | No | Yes |
| App metrics endpoint | Yes | Scrape and dashboard |
| CloudWatch logs and alarms | No | Yes |
| GitHub Actions workflows | No | Yes |
| Deployment rollback | No | Yes |
| Load testing | Optional script help only | Yes |
| Failure labs | No | Yes |
| Portfolio screenshots | No | Yes |

---

## Simple rule

The coding agent builds **what runs inside the container**.

You build **everything around the container**.

```text
Agent = application behaviour
You = infrastructure, deployment, automation, scaling, monitoring, reliability
```
