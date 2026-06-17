# 09 - Portfolio Checklist

Use this checklist before publishing the project on GitHub.

## Repository quality

- [ ] Clean root README
- [ ] Architecture diagram
- [ ] Service contracts documented
- [ ] Environment variables documented
- [ ] Local run instructions documented
- [ ] Deployment strategy documented
- [ ] Rollback strategy documented
- [ ] Failure labs documented
- [ ] Screenshots added

## DevOps proof

- [ ] Docker images built successfully
- [ ] Images pushed to ECR
- [ ] Terraform creates AWS resources
- [ ] Helm deploys services
- [ ] GitHub Actions deploys to dev
- [ ] GitHub Actions deploys to staging
- [ ] Production requires manual approval
- [ ] Alembic migrations run before deployment
- [ ] Smoke tests run after deployment
- [ ] Failed deployment triggers rollback
- [ ] KEDA scales worker from queue depth
- [ ] Grafana dashboard shows app metrics
- [ ] CloudWatch shows AWS metrics

## Screenshots to include

- [ ] GitHub Actions successful pipeline
- [ ] GitHub Actions failed pipeline with rollback
- [ ] EKS workloads
- [ ] Helm releases
- [ ] SQS queue depth
- [ ] KEDA worker scaling
- [ ] Grafana dashboard
- [ ] CloudWatch metrics
- [ ] RDS metrics
- [ ] Redis metrics
