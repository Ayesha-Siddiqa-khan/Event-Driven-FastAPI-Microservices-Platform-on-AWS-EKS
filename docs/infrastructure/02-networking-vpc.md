# 02 - Networking: VPC, Subnets, Routing, and Security Groups

The VPC is the foundation of your AWS infrastructure.

## Goal

Create a private, production-style network where:

- only the load balancer is public
- Kubernetes worker nodes run in private subnets
- RDS PostgreSQL runs in private database subnets
- Redis runs in private subnets
- services access AWS APIs through NAT Gateway or VPC endpoints

## Recommended CIDR

```text
VPC CIDR: 10.20.0.0/16
```

## Subnet plan

Use two Availability Zones for beginner-friendly high availability.

| Subnet | CIDR | AZ | Purpose |
|---|---|---|---|
| public-a | `10.20.1.0/24` | `us-east-1a` | ALB, NAT Gateway |
| public-b | `10.20.2.0/24` | `us-east-1b` | ALB |
| private-app-a | `10.20.11.0/24` | `us-east-1a` | EKS nodes/pods |
| private-app-b | `10.20.12.0/24` | `us-east-1b` | EKS nodes/pods |
| private-db-a | `10.20.21.0/24` | `us-east-1a` | RDS/Redis |
| private-db-b | `10.20.22.0/24` | `us-east-1b` | RDS/Redis |

## Internet Gateway

Attach one Internet Gateway to the VPC.

Name:

```text
edfp-dev-igw-main
```

Used by:

```text
public subnets
Application Load Balancer
NAT Gateway
```

## NAT Gateway

For cost saving, use one NAT Gateway in `dev`.

Name:

```text
edfp-dev-nat-a
```

Production improvement:

```text
one NAT Gateway per Availability Zone
```

## Route tables

| Route table | Associated subnets | Default route |
|---|---|---|
| public | public-a, public-b | Internet Gateway |
| private-app | private-app-a, private-app-b | NAT Gateway |
| private-db | private-db-a, private-db-b | no direct internet route if possible |

## Security groups

### ALB security group

Name:

```text
edfp-dev-sg-alb
```

Inbound:

```text
80 from 0.0.0.0/0
443 from 0.0.0.0/0
```

Outbound:

```text
to EKS node/pod security group on app ports
```

### EKS node/app security group

Name:

```text
edfp-dev-sg-eks-apps
```

Inbound:

```text
from ALB security group to api-gateway port
internal cluster communication
```

Outbound:

```text
RDS PostgreSQL 5432
Redis 6379
SQS API through NAT or VPC endpoint
Secrets Manager API through NAT or VPC endpoint
```

### RDS security group

Name:

```text
edfp-dev-sg-rds-postgres
```

Inbound:

```text
5432 from EKS node/app security group only
```

Do not allow `0.0.0.0/0` to PostgreSQL.

### Redis security group

Name:

```text
edfp-dev-sg-redis
```

Inbound:

```text
6379 from EKS node/app security group only
```

## Optional VPC endpoints

For a stronger project, add VPC endpoints later:

```text
S3 gateway endpoint
ECR API endpoint
ECR Docker endpoint
CloudWatch Logs endpoint
Secrets Manager endpoint
SQS endpoint
STS endpoint
```

This reduces dependency on public internet/NAT for AWS service access.

## Verification checklist

After networking is created, verify:

- VPC exists
- public subnets have route to Internet Gateway
- private app subnets have route to NAT Gateway
- DB subnets are private
- RDS security group allows only EKS app security group
- Redis security group allows only EKS app security group
- public access to database is disabled
