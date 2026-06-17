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

For the dev EKS managed node group, the default instance type is
`c7i-flex.large` with desired/min/max capacity set to `1/1/2`. This matches the
Free Tier eligible choices returned by AWS in `us-east-1` for this account while
keeping the lab cluster small.

The GitHub Actions OIDC provider for `token.actions.githubusercontent.com` is an
account-level IAM provider. Because many AWS accounts already have it, Terraform
defaults to reusing the existing provider instead of creating a duplicate.

After patching an interrupted or failed dev apply, run:

```bash
cd infra/terraform/envs/dev
terraform plan -var="github_org=Ayesha-Siddiqa-khan" -var="github_repo=Event-Driven-FastAPI-Microservices-Platform-on-AWS-EKS"
terraform apply -var="github_org=Ayesha-Siddiqa-khan" -var="github_repo=Event-Driven-FastAPI-Microservices-Platform-on-AWS-EKS"
```

The `envs/dev`, `envs/staging`, and `envs/prod` directories are still available
for later CI/CD and remote-state workflows.
