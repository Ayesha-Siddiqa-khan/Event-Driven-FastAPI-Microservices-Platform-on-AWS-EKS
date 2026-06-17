variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "github_org" {
  type = string
}

variable "github_repo" {
  type = string
}

variable "github_branch" {
  type    = string
  default = "main"
}

variable "create_github_oidc_provider" {
  type        = bool
  description = "Whether to create the account-level GitHub Actions OIDC provider."
  default     = false
}

variable "existing_github_oidc_provider_arn" {
  type        = string
  description = "Existing GitHub Actions OIDC provider ARN. If null, the module builds it from the current AWS account ID."
  default     = null
}

variable "tags" {
  type    = map(string)
  default = {}
}
