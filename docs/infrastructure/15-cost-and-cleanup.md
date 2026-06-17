# 15 - Cost and Cleanup

AWS resources can cost money. Build carefully and destroy dev resources when not needed.

## Highest cost resources in this project

Usually expensive:

```text
NAT Gateway
EKS worker nodes
RDS instance
ElastiCache Redis
ALB
CloudWatch logs and metrics
```

## Cost-saving beginner choices

For dev:

```text
single NAT Gateway
small EKS node group
small RDS instance
small Redis instance
short CloudWatch log retention
no Multi-AZ for dev database
turn off staging/prod when not needed
```

## Do not delete these accidentally

Be careful with:

```text
S3 Terraform state bucket
DynamoDB Terraform lock table
RDS database backups
ECR images you still need for rollback
```

## Cleanup order

When destroying dev:

```text
1. delete app Helm releases
2. delete ingress so ALB is removed
3. delete KEDA scaled objects
4. delete monitoring stack if needed
5. delete EKS workloads
6. destroy app-support resources
7. destroy data layer if safe
8. destroy EKS
9. destroy network
10. keep or separately delete Terraform state backend
```

## Common cleanup problems

| Problem | Cause | Fix |
|---|---|---|
| VPC will not delete | ENI still exists | check EKS, ALB, VPC endpoints |
| subnet will not delete | load balancer still attached | delete ingress/ALB first |
| security group will not delete | another resource references it | inspect dependencies |
| ECR repository will not delete | images still inside | delete images or force delete |
| S3 bucket will not delete | objects still inside | empty bucket first |

## Portfolio note

Include a cost section in your README:

```text
This project uses paid AWS resources. For learning, I used dev-sized infrastructure and destroyed non-essential resources after testing.
```
