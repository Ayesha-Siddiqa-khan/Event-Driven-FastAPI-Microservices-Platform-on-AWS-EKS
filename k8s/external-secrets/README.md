# External Secrets

Install External Secrets Operator before deploying the application charts:

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm repo update
helm upgrade --install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace
```

Apply `cluster-secret-store.yaml` after annotating the `external-secrets` service account with the Terraform-created `external-secrets` IRSA role. The role can read the `/edfp/<env>/*` secrets from AWS Secrets Manager.

```bash
kubectl annotate serviceaccount external-secrets \
  -n external-secrets \
  eks.amazonaws.com/role-arn=REPLACE_WITH_EXTERNAL_SECRETS_IRSA_ROLE_ARN
```

Application Helm charts create `ExternalSecret` resources. They do not store secret values in Git.
The manifests use `external-secrets.io/v1`, matching the current External
Secrets Operator CRDs installed by the Helm chart.
