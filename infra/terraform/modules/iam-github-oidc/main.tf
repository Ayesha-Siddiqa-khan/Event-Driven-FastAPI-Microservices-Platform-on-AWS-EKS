locals {
  github_oidc_url                   = "https://token.actions.githubusercontent.com"
  github_oidc_provider_path         = "token.actions.githubusercontent.com"
  existing_github_oidc_provider_arn = coalesce(var.existing_github_oidc_provider_arn, "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${local.github_oidc_provider_path}")
  github_oidc_provider_arn          = var.create_github_oidc_provider ? aws_iam_openid_connect_provider.github[0].arn : data.aws_iam_openid_connect_provider.github[0].arn
  role_name                         = "${var.project_name}-${var.environment}-github-actions"
  repo_sub                          = "repo:${var.github_org}/${var.github_repo}:ref:refs/heads/${var.github_branch}"
  tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

data "aws_caller_identity" "current" {}

data "tls_certificate" "github" {
  count = var.create_github_oidc_provider ? 1 : 0
  url   = local.github_oidc_url
}

resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_github_oidc_provider ? 1 : 0

  url             = local.github_oidc_url
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.github[0].certificates[0].sha1_fingerprint]

  tags = merge(local.tags, { Name = "${local.role_name}-oidc" })
}

data "aws_iam_openid_connect_provider" "github" {
  count = var.create_github_oidc_provider ? 0 : 1
  arn   = local.existing_github_oidc_provider_arn
}

data "aws_iam_policy_document" "trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.github_oidc_provider_arn]
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
