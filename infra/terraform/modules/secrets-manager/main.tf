locals {
  tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

resource "aws_secretsmanager_secret" "this" {
  for_each = nonsensitive(var.secret_values)

  name                    = each.key
  kms_key_id              = var.kms_key_id
  recovery_window_in_days = var.environment == "prod" ? 30 : 0

  tags = merge(local.tags, { Name = each.key })
}

resource "aws_secretsmanager_secret_version" "this" {
  for_each = nonsensitive(var.secret_values)

  secret_id     = aws_secretsmanager_secret.this[each.key].id
  secret_string = var.secret_values[each.key]
}
