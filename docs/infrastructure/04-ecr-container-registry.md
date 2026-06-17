# 04 - ECR Container Registry

Amazon ECR stores Docker images for your services.

## Why you need ECR

Your GitHub Actions pipeline will:

```text
build Docker image
push image to ECR
update Helm image tag
Kubernetes pulls image from ECR
```

## Repositories to create

Create one private ECR repository per service:

```text
edfp-dev-api-gateway
edfp-dev-auth-service
edfp-dev-order-service
edfp-dev-payment-service
edfp-dev-notification-worker
```

## Recommended image tag format

Use Git SHA tags:

```text
<short-git-sha>
```

Example:

```text
a1b2c3d
```

For environment-specific tags:

```text
dev-a1b2c3d
staging-a1b2c3d
prod-a1b2c3d
```

## ECR lifecycle policy

Add a lifecycle policy to avoid storing too many old images.

Recommended beginner rule:

```text
keep last 20 images
expire untagged images after 7 days
```

## ECR image scanning

Enable image scanning if available in your setup.

Learning goal:

```text
push image
scan image
review vulnerabilities
fix package versions if needed
```

## Which GitHub Actions permissions are needed

Your GitHub Actions deploy role needs permissions to:

```text
ecr:GetAuthorizationToken
ecr:BatchCheckLayerAvailability
ecr:InitiateLayerUpload
ecr:UploadLayerPart
ecr:CompleteLayerUpload
ecr:PutImage
ecr:DescribeRepositories
ecr:DescribeImages
```

## Kubernetes image references

Your Helm values should later reference images like:

```text
<account-id>.dkr.ecr.us-east-1.amazonaws.com/edfp-dev-order-service:a1b2c3d
```

## Verification checklist

- all five ECR repositories exist
- GitHub Actions can authenticate to ECR
- Docker image can be pushed
- image tag is visible in ECR
- EKS pods can pull image
- no deployment uses only `latest`
