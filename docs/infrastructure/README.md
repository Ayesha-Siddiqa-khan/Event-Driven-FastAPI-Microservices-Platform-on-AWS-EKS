# Infrastructure Documentation Index

This folder explains the complete AWS infrastructure plan for the project.

It is written as a practical lab guide. Each file answers:

- What should I create?
- Why do I need it?
- What should I name it?
- Which service uses it?
- Which environment variables should it provide?
- What should I verify after creating it?

## Project code name

Use a short code name for AWS resources:

```text
edfp
```

Meaning:

```text
event-driven-fastapi-platform
```

Short names are useful because some AWS resources have length limits.

## Environment names

Use three environments:

```text
dev
staging
prod
```

Start with `dev` only. Add `staging` after the app works. Add `prod` last.

## Naming pattern

Use this pattern:

```text
<project>-<environment>-<component>-<purpose>
```

Example:

```text
edfp-dev-ecr-api-gateway
edfp-dev-sqs-order-events
edfp-dev-rds-postgres
edfp-dev-eks-main
```

For S3 buckets, add account ID and region because bucket names must be globally unique:

```text
edfp-dev-tfstate-123456789012-us-east-1
```

## Recommended first environment

Create only `dev` first:

```text
AWS_REGION=us-east-1
PROJECT=edfp
ENVIRONMENT=dev
CLUSTER_NAME=edfp-dev-eks-main
```

After everything works in `dev`, duplicate the same pattern for `staging` and `prod`.
