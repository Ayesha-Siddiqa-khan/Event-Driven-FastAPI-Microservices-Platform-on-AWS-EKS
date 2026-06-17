variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "repositories" {
  type        = list(string)
  description = "Service repository suffixes, for example api-gateway."
}

variable "tags" {
  type    = map(string)
  default = {}
}
