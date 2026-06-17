# Scripts

Operational helper scripts:

- `build-all-images.sh`: builds all service Docker images
- `push-all-images.sh`: pushes all service images to ECR
- `smoke-test.sh`: checks gateway and internal service health after deployment
- `migrate.sh`: runs Alembic migrations locally for database services

CI/CD primarily uses Helm migration Jobs, but `migrate.sh` is useful for controlled local runs.
