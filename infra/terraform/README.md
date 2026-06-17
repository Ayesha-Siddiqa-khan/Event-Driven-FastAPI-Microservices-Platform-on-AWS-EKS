# Terraform

Terraform creates the AWS foundation for the EDFP lab:

- VPC with public and private subnets
- EKS cluster and private managed node group
- ECR repositories
- RDS PostgreSQL
- ElastiCache Redis
- SQS queues and DLQs
- Secrets Manager secrets
- GitHub Actions OIDC role
- IRSA roles for SQS workloads

For local learning, start from this directory. The root configuration uses a local
Terraform state file at `state/dev/terraform.tfstate`, so you can initialize
without creating an S3 backend bucket first.

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

The `envs/dev`, `envs/staging`, and `envs/prod` directories are still available
for later CI/CD and remote-state workflows.
