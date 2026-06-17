variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "secret_values" {
  type        = map(string)
  description = "Map of Secrets Manager secret names to string values."
  sensitive   = true
}

variable "kms_key_id" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}
