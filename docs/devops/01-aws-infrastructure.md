# AWS Infrastructure

Terraform creates one environment at a time using the naming pattern:

```text
edfp-<env>-<resource-name>
```

Core AWS resources:

- VPC: network boundary for EKS, RDS, Redis, and load balancers
- EKS: Kubernetes control plane and private worker nodes
- ECR: Docker image registry for each service
- RDS PostgreSQL: relational storage for auth, orders, payments, and notifications
- ElastiCache Redis: cache/session storage for auth and orders
- SQS: event queues with DLQs
- Secrets Manager: application runtime secrets
- IAM: GitHub OIDC and workload IRSA roles

Dev uses small resources. Prod enables stronger defaults such as Multi-AZ RDS and larger node capacity.
