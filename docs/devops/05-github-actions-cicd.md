# GitHub Actions CI/CD

Workflows:

- `ci.yml`: runs pytest on pull requests and pushes to `main`
- `terraform-plan.yml`: validates and plans Terraform changes on pull requests, pushes to `main`, and manual runs
- `terraform-apply-dev.yml`: manually applies dev infrastructure
- `deploy-dev.yml`: manually deploys dev, and also deploys on pushes to `main`
- `deploy-staging.yml`: manual staging deployment
- `deploy-prod.yml`: manual prod deployment

GitHub Actions uses OIDC:

- No AWS access keys in GitHub secrets
- `id-token: write` is enabled in workflows
- AWS IAM trusts only the configured repository

Required GitHub repository variables:

- `AWS_ROLE_ARN`: GitHub Actions OIDC role ARN. For this lab dev account use `arn:aws:iam::257536659737:role/edfp-dev-github-actions`
- `AWS_REGION`: AWS region, normally `us-east-1`
- `AWS_ACCOUNT_ID`: AWS account ID, normally `257536659737`
- `EKS_CLUSTER_NAME`: dev EKS cluster name, normally `edfp-dev-eks`
- `NAMESPACE`: dev Kubernetes namespace, normally `edfp-dev`

The first infrastructure apply must be bootstrapped outside GitHub Actions because the OIDC role does not exist until Terraform creates it.

Use GitHub Environments for staging and prod approvals.

## Manual workflow checks

If workflows appear in the left sidebar but show no runs, confirm these items in
GitHub:

1. The workflow files are committed to the default branch, `main`.
2. Repository Actions are enabled under Settings -> Actions -> General.
3. Workflow permissions allow GitHub Actions to run. OIDC does not require AWS access keys.
4. The repository variables above exist under Settings -> Secrets and variables -> Actions -> Variables.

To manually run dev deployment:

1. Open the repository on GitHub.
2. Go to Actions.
3. Select `Deploy Dev`.
4. Click `Run workflow`.
5. Select branch `main`.
6. Click the green `Run workflow` button.

To confirm it is running, stay on the `Deploy Dev` workflow page and watch for a
new run at the top of the list. Open the run and verify these steps appear:

- configure AWS credentials with OIDC
- login to Amazon ECR
- build and push Docker images
- update kubeconfig for EKS
- create namespace `edfp-dev` if missing
- deploy services with Helm
- check pods and services
