locals {
  issuer_host = replace(var.oidc_provider_url, "https://", "")
  tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
  service_accounts = {
    order-service = {
      namespace = var.namespace
      actions   = ["sqs:SendMessage", "sqs:GetQueueAttributes", "sqs:GetQueueUrl"]
      resources = [var.order_events_queue_arn]
    }
    payment-service = {
      namespace = var.namespace
      actions   = ["sqs:SendMessage", "sqs:GetQueueAttributes", "sqs:GetQueueUrl"]
      resources = [var.notification_events_queue_arn]
    }
    notification-worker = {
      namespace = var.namespace
      actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:ChangeMessageVisibility", "sqs:GetQueueAttributes", "sqs:GetQueueUrl"]
      resources = [var.notification_events_queue_arn]
    }
    keda-operator = {
      namespace = var.keda_namespace
      actions   = ["sqs:GetQueueAttributes", "sqs:GetQueueUrl", "sqs:ListQueues"]
      resources = [var.notification_events_queue_arn]
    }
    external-secrets = {
      namespace = var.external_secrets_namespace
      actions   = ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"]
      resources = var.secret_arns
    }
  }
}

data "aws_iam_policy_document" "trust" {
  for_each = local.service_accounts

  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${local.issuer_host}:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "${local.issuer_host}:sub"
      values   = ["system:serviceaccount:${each.value.namespace}:${each.key}"]
    }
  }
}

resource "aws_iam_role" "this" {
  for_each = local.service_accounts

  name               = "${var.project_name}-${var.environment}-${each.key}-irsa"
  assume_role_policy = data.aws_iam_policy_document.trust[each.key].json

  tags = merge(local.tags, { Name = "${var.project_name}-${var.environment}-${each.key}-irsa" })
}

resource "aws_iam_role_policy" "this" {
  for_each = local.service_accounts

  name = "${var.project_name}-${var.environment}-${each.key}-sqs"
  role = aws_iam_role.this[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = each.value.actions
      Resource = each.value.resources
    }]
  })
}
