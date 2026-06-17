# Terraform Usage

Create the S3 backend bucket first:

```bash
aws s3api create-bucket --bucket REPLACE_WITH_EDFP_TERRAFORM_STATE_BUCKET --region us-east-1
aws s3api put-bucket-versioning --bucket REPLACE_WITH_EDFP_TERRAFORM_STATE_BUCKET --versioning-configuration Status=Enabled
```

The backend uses native S3 locking:

```hcl
use_lockfile = true
```

DynamoDB locking is not used because modern Terraform supports S3 lock files.

Run dev:

```bash
cd infra/terraform/envs/dev
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

Bootstrap note: the GitHub Actions OIDC role is created by Terraform. The first `terraform apply` must be run locally with an AWS administrator/deployment identity, or from a temporary pre-existing bootstrap role. After that, store the Terraform-created role ARN in the GitHub repository variable `AWS_ROLE_ARN`.

Repeat from `envs/staging` or `envs/prod` for higher environments.
