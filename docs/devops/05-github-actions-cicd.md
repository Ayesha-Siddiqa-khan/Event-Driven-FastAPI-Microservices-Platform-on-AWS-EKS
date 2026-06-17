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

Required GitHub repository variables or secrets:

- `AWS_ROLE_ARN`: GitHub Actions OIDC role ARN. This may be a repository secret or variable. For this lab dev account use `arn:aws:iam::257536659737:role/edfp-dev-github-actions`
- `AWS_REGION`: AWS region, normally `us-east-1`
- `AWS_ACCOUNT_ID`: AWS account ID, normally `257536659737`
- `EKS_CLUSTER_NAME`: dev EKS cluster name, normally `edfp-dev-eks`
- `NAMESPACE`: dev Kubernetes namespace, normally `edfp-dev`

The dev workflows include defaults for these values and read `AWS_ROLE_ARN`
from either a variable or secret, so a missing repository variable does not cause
`configure-aws-credentials` to fail with
`Could not load credentials from any providers`. Still add the variables in
GitHub so the configuration is explicit and easy to change later.

The first infrastructure apply must be bootstrapped outside GitHub Actions because the OIDC role does not exist until Terraform creates it.

Use GitHub Environments for staging and prod approvals.

## Manual workflow checks

If workflows appear in the left sidebar but show no runs, confirm these items in
GitHub:

1. The workflow files are committed to the default branch, `main`.
2. Repository Actions are enabled under Settings -> Actions -> General.
3. Workflow permissions allow GitHub Actions to run. OIDC does not require AWS access keys.
4. The repository variables above exist under Settings -> Secrets and variables -> Actions -> Variables, or `AWS_ROLE_ARN` exists under Secrets.

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
- install External Secrets Operator and KEDA
- create namespace `edfp-dev` if missing
- deploy services with Helm
- check pods and services

The deploy workflows invoke repository scripts with `bash ./scripts/name.sh`.
This avoids Linux runner permission errors when scripts are committed from a
Windows working tree without the executable bit.

The application Helm charts create `ExternalSecret`, `TriggerAuthentication`,
and `ScaledObject` resources. Deploy workflows install External Secrets
Operator and KEDA first, then wait for their CRDs before deploying the service
charts. Without this step, Helm fails with errors such as `no matches for kind
"ExternalSecret"`.

Migration Jobs run as `post-install,post-upgrade` Helm hooks. They need the
release ConfigMaps and ExternalSecret-backed Kubernetes Secrets to exist before
`alembic upgrade head` can start.

Deploy workflows delete stale migration Jobs before applying service charts.
This cleans up failed historical hook Jobs, such as older `pre-install` jobs
that could not start because the service account did not exist yet.
