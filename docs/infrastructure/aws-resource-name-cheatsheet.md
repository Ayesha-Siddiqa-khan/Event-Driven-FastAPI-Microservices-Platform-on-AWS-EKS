# AWS Resource Name Cheatsheet

Use this file when you are creating Terraform variables, AWS resources, Helm values, and README tables.

Replace:

```text
<account-id> with your AWS account ID
<region> with your AWS region, for example us-east-1
```

## Global variables

```text
PROJECT=edfp
ENV=dev
REGION=us-east-1
ACCOUNT_ID=<account-id>
```

## Terraform backend

```text
S3 bucket:      edfp-dev-tfstate-<account-id>-us-east-1
DynamoDB lock: edfp-dev-tflock
```

## Network

```text
VPC:                 edfp-dev-vpc-main
Internet Gateway:    edfp-dev-igw-main
NAT Gateway:         edfp-dev-nat-a
Public subnet A:     edfp-dev-public-a
Public subnet B:     edfp-dev-public-b
Private app subnet A: edfp-dev-private-app-a
Private app subnet B: edfp-dev-private-app-b
Private db subnet A:  edfp-dev-private-db-a
Private db subnet B:  edfp-dev-private-db-b
```

## ECR

```text
edfp-dev-api-gateway
edfp-dev-auth-service
edfp-dev-order-service
edfp-dev-payment-service
edfp-dev-notification-worker
```

## EKS

```text
Cluster:        edfp-dev-eks-main
Node group:     edfp-dev-ng-apps
Namespace:      edfp-dev
```

## Service accounts

```text
api-gateway-sa
auth-service-sa
order-service-sa
payment-service-sa
notification-worker-sa
```

## IAM roles

```text
edfp-dev-github-actions-deployer
edfp-dev-irsa-auth-service
edfp-dev-irsa-order-service
edfp-dev-irsa-payment-service
edfp-dev-irsa-notification-worker
edfp-dev-irsa-aws-load-balancer-controller
edfp-dev-irsa-external-secrets
edfp-dev-irsa-keda
```

## Security groups

```text
edfp-dev-sg-alb
edfp-dev-sg-eks-apps
edfp-dev-sg-rds-postgres
edfp-dev-sg-redis
```

## RDS

```text
DB instance: edfp-dev-rds-postgres
DB name:     edfp_dev
DB user:     edfp_app
```

## Redis

```text
Redis: edfp-dev-redis-main
```

## SQS

```text
Order queue:             edfp-dev-order-events
Order DLQ:               edfp-dev-order-events-dlq
Notification queue:      edfp-dev-notification-events
Notification DLQ:        edfp-dev-notification-events-dlq
```

## Secrets Manager

```text
/edfp/dev/auth-service/database-url
/edfp/dev/auth-service/redis-url
/edfp/dev/auth-service/jwt-secret
/edfp/dev/order-service/database-url
/edfp/dev/order-service/redis-url
/edfp/dev/order-service/order-events-queue-url
/edfp/dev/payment-service/database-url
/edfp/dev/payment-service/notification-events-queue-url
/edfp/dev/notification-worker/database-url
/edfp/dev/notification-worker/notification-events-queue-url
```

## Public URL

```text
api-dev.yourdomain.com
```

If you do not own a domain, use the ALB DNS name.
