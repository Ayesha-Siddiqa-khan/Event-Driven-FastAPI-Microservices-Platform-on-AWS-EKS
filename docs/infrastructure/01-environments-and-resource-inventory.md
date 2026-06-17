# 01 - Environments and Resource Inventory

Build the project in three environments, but do not create all three at the beginning.

## Environment plan

| Environment | Purpose | When to create |
|---|---|---|
| `dev` | learning, testing, frequent destroy/recreate | first |
| `staging` | production-like testing | after dev works |
| `prod` | final recruiter demo environment | last |

## Recommended AWS region

Use one region for the first project:

```text
us-east-1
```

You may choose another region closer to you, but keep everything in the same region at first.

## Complete resource inventory for `dev`

| Layer | Resource | Recommended name |
|---|---|---|
| Terraform state | S3 bucket | `edfp-dev-tfstate-<account-id>-us-east-1` |
| Terraform lock | DynamoDB table | `edfp-dev-tflock` |
| Network | VPC | `edfp-dev-vpc-main` |
| Network | Public subnets | `edfp-dev-public-a`, `edfp-dev-public-b` |
| Network | Private app subnets | `edfp-dev-private-app-a`, `edfp-dev-private-app-b` |
| Network | Private DB subnets | `edfp-dev-private-db-a`, `edfp-dev-private-db-b` |
| Network | NAT Gateway | `edfp-dev-nat-a` |
| Registry | ECR repositories | one repository per service |
| Compute | EKS cluster | `edfp-dev-eks-main` |
| Compute | Node group | `edfp-dev-ng-apps` |
| Database | RDS PostgreSQL | `edfp-dev-rds-postgres` |
| Cache | ElastiCache Redis | `edfp-dev-redis-main` |
| Queue | SQS order queue | `edfp-dev-order-events` |
| Queue | SQS notification queue | `edfp-dev-notification-events` |
| Secrets | Secrets Manager paths | `/edfp/dev/...` |
| Ingress | ALB | created by AWS Load Balancer Controller |
| DNS | Route 53 record | optional, for example `api-dev.example.com` |
| Monitoring | CloudWatch log groups | `/aws/eks/edfp-dev/...` |
| Monitoring | Prometheus/Grafana | installed inside EKS |

## Service-to-resource mapping

| Service | Database | Redis | SQS send | SQS receive | Internet access |
|---|---|---|---|---|---|
| api-gateway | no | no | no | no | public through ALB |
| auth-service | yes | yes | no | no | internal only |
| order-service | yes | yes | order-events | no | internal only |
| payment-service | yes | no | notification-events | optional later | internal only |
| notification-worker | yes | no | no | notification-events | no ingress |

## Beginner simplification

Use one PostgreSQL database instance and separate tables for each service.

Later, as an advanced improvement, split into separate databases:

```text
auth_db
orders_db
payments_db
notifications_db
```

For the first version, one database is enough.
