# 16 - Recruiter Evidence Checklist

Recruiters and hiring teams need proof. Capture screenshots and write short explanations.

## Infrastructure evidence

Take screenshots of:

```text
EKS cluster nodes ready
ECR repositories with image tags
RDS private database
Redis private endpoint
SQS queues and DLQs
Secrets Manager secret names without exposing values
GitHub Actions successful deployment
ALB target group healthy
Grafana dashboard
CloudWatch logs
KEDA scaling worker replicas
```

## README sections to include

```text
Architecture overview
AWS services used
Deployment flow
CI/CD flow
Database migration strategy
Secrets management strategy
Queue processing strategy
Autoscaling strategy
Monitoring and alerting
Failure labs
Rollback demo
Cost notes
Lessons learnt
```

## Failure lab evidence

Show these tests:

| Test | Evidence |
|---|---|
| Bad deployment rollback | GitHub Actions log + Helm revision |
| Queue backlog scaling | SQS depth + worker replicas |
| Redis failure | `/ready` fails for dependent services |
| DB connection problem | migration fails or readiness fails |
| API load test | k6 output + Grafana latency dashboard |
| Worker failure | failed message metric + DLQ message |

## Strong portfolio wording

Use wording like:

```text
This project demonstrates production-style deployment of event-driven FastAPI microservices on AWS EKS using Terraform-managed infrastructure, GitHub Actions OIDC, ECR, RDS PostgreSQL, ElastiCache Redis, SQS, Secrets Manager, Helm, KEDA autoscaling, Prometheus/Grafana monitoring, CloudWatch logs, and rollback testing.
```
