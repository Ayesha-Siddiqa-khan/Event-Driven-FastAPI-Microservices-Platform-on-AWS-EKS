variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "cluster_version" {
  type    = string
  default = "1.31"
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "public_endpoint" {
  type    = bool
  default = true
}

variable "node_instance_types" {
  type    = list(string)
  default = ["t3.medium"]
}

variable "node_desired_size" {
  type    = number
  default = 2
}

variable "node_min_size" {
  type    = number
  default = 1
}

variable "node_max_size" {
  type    = number
  default = 3
}

variable "tags" {
  type    = map(string)
  default = {}
}
