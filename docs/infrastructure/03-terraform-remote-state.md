# 03 - Terraform Remote State: S3 and DynamoDB

Before creating the main infrastructure, create remote state storage.

## Why you need this

Terraform state records what infrastructure exists. If you keep state only on your laptop, it is easy to lose or corrupt it. Remote state makes your infrastructure easier to manage and safer for CI/CD.

## Resources to create manually first

Create these before your main Terraform code:

| Resource | Name |
|---|---|
| S3 bucket | `edfp-dev-tfstate-<account-id>-us-east-1` |
| DynamoDB table | `edfp-dev-tflock` |

## S3 bucket purpose

Stores Terraform state files.

Example object keys:

```text
edfp/dev/network/terraform.tfstate
edfp/dev/eks/terraform.tfstate
edfp/dev/data/terraform.tfstate
edfp/dev/app-support/terraform.tfstate
```

## S3 bucket settings

Recommended settings:

```text
versioning: enabled
server-side encryption: enabled
public access: blocked
object ownership: bucket owner enforced
lifecycle: keep recent versions, expire old non-current versions later
```

## DynamoDB table purpose

Used for Terraform state locking.

Table name:

```text
edfp-dev-tflock
```

Partition key:

```text
LockID
```

Type:

```text
String
```

## Recommended Terraform state separation

Do not put the whole project into one state file. Split by layer:

```text
network
security
ecr
eks
data
observability
app-support
```

Beginner version:

```text
network.tfstate
eks.tfstate
data.tfstate
```

Advanced version:

```text
network/terraform.tfstate
ecr/terraform.tfstate
eks/terraform.tfstate
rds/terraform.tfstate
redis/terraform.tfstate
sqs/terraform.tfstate
secrets/terraform.tfstate
observability/terraform.tfstate
```

## Verification checklist

- S3 bucket exists
- bucket versioning is enabled
- public access is blocked
- DynamoDB table exists
- Terraform backend can initialise successfully
- state file appears in S3 after `terraform apply`
- lock appears temporarily during Terraform operation
