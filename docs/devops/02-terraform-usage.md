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

Dev EKS node group note: the dev managed node group uses
`c7i-flex.large` and keeps capacity at desired/min/max `1/1/2`. AWS returned
this type as Free Tier eligible in `us-east-1` for this account, and the small
capacity keeps the learning environment controlled.

GitHub OIDC note: the IAM OIDC provider for
`https://token.actions.githubusercontent.com` is account-level. If it already
exists, Terraform must reuse it instead of trying to create another provider.
The dev configuration sets `create_github_oidc_provider = false` and references
the existing provider ARN format:

```text
arn:aws:iam::<account-id>:oidc-provider/token.actions.githubusercontent.com
```

After this patch, rerun:

```bash
cd infra/terraform/envs/dev
terraform plan -var="github_org=Ayesha-Siddiqa-khan" -var="github_repo=Event-Driven-FastAPI-Microservices-Platform-on-AWS-EKS"
terraform apply -var="github_org=Ayesha-Siddiqa-khan" -var="github_repo=Event-Driven-FastAPI-Microservices-Platform-on-AWS-EKS"
```

If GitHub Actions cannot assume `arn:aws:iam::257536659737:role/edfp-dev-github-actions`
with `sts:AssumeRoleWithWebIdentity`, update only the GitHub OIDC IAM role
trust policy from a local authenticated terminal:

```bash
cd infra/terraform/envs/dev
terraform apply \
  -target=module.github_oidc.aws_iam_role.github_actions \
  -var="github_org=Ayesha-Siddiqa-khan" \
  -var="github_repo=Event-Driven-FastAPI-Microservices-Platform-on-AWS-EKS"
```

The dev OIDC trust policy is for branch `main` and also allows GitHub
environment subjects such as
`repo:Ayesha-Siddiqa-khan/Event-Driven-FastAPI-Microservices-Platform-on-AWS-EKS:environment:dev`.

Bootstrap note: the GitHub Actions IAM role is created by Terraform. The first
`terraform apply` must be run locally with an AWS administrator/deployment
identity, or from a temporary pre-existing bootstrap role. After that, store the
Terraform-created role ARN in the GitHub repository variable `AWS_ROLE_ARN`.

Repeat from `envs/staging` or `envs/prod` for higher environments.
