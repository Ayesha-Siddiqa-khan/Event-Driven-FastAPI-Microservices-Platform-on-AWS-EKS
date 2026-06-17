# GitHub Actions CI/CD

Workflows:

- `ci.yml`: runs pytest for changed services on pull requests
- `terraform-plan.yml`: validates and plans Terraform changes
- `terraform-apply-dev.yml`: applies dev infrastructure
- `deploy-dev.yml`: builds, pushes, deploys, and smoke-tests dev
- `deploy-staging.yml`: manual staging deployment
- `deploy-prod.yml`: manual prod deployment

GitHub Actions uses OIDC:

- No AWS access keys in GitHub secrets
- `id-token: write` is enabled in workflows
- AWS IAM trusts only the configured repository

Required GitHub repository variables:

- `AWS_ROLE_ARN`: Terraform-created GitHub Actions IAM role ARN
- `AWS_REGION`: optional, defaults to `us-east-1`

The first infrastructure apply must be bootstrapped outside GitHub Actions because the OIDC role does not exist until Terraform creates it.

Use GitHub Environments for staging and prod approvals.
