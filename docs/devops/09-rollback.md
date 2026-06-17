# Rollback

Deploy workflows run smoke tests after Helm deployment.

If smoke tests fail:

1. The workflow runs `helm rollback` for affected releases.
2. The workflow prints rollout status.
3. The workflow exits with failure.

Manual rollback:

```bash
helm history edfp-dev-api-gateway -n edfp-dev
helm rollback edfp-dev-api-gateway <revision> -n edfp-dev
kubectl rollout status deployment/edfp-dev-api-gateway -n edfp-dev
```

Use immutable Git SHA image tags to make rollbacks predictable.
