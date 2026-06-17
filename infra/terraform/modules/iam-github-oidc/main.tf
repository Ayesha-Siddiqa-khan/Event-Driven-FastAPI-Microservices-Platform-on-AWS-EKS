locals {
  role_name = "${var.project_name}-${var.environment}-github-actions"
  repo_sub  = "repo:${var.github_org}/${var.github_repo}:ref:refs/heads/${var.github_branch}"
  tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

data "tls_certificate" "github" {
  url = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.github.certificates[0].sha1_fingerprint]

  tags = merge(local.tags, { Name = "${local.role_name}-oidc" })
}

data "aws_iam_policy_document" "trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = [local.repo_sub, "repo:${var.github_org}/${var.github_repo}:environment:*"]
    }
  }
}

resource "aws_iam_role" "github_actions" {
  name               = local.role_name
  assume_role_policy = data.aws_iam_policy_document.trust.json

  tags = local.tags
}

# TODO: Narrow this policy after the learning project stabilizes.
resource "aws_iam_role_policy" "learning_platform" {
  name = "${local.role_name}-learning-platform"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "cloudformation:*",
          "cloudwatch:*",
          "ec2:*",
          "ecr:*",
          "eks:*",
          "elasticache:*",
          "iam:*",
          "logs:*",
          "rds:*",
          "secretsmanager:*",
          "sqs:*",
          "ssm:*",
          "sts:GetCallerIdentity"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = "*"
      }
    ]
  })
}
