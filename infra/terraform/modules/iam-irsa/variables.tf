variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "namespace" {
  type = string
}

variable "oidc_provider_arn" {
  type = string
}

variable "oidc_provider_url" {
  type = string
}

variable "order_events_queue_arn" {
  type = string
}

variable "notification_events_queue_arn" {
  type = string
}

variable "keda_namespace" {
  type    = string
  default = "keda"
}

variable "external_secrets_namespace" {
  type    = string
  default = "external-secrets"
}

variable "secret_arns" {
  type        = list(string)
  description = "Secrets Manager ARNs readable by External Secrets Operator."
  default     = []
}

variable "tags" {
  type    = map(string)
  default = {}
}
