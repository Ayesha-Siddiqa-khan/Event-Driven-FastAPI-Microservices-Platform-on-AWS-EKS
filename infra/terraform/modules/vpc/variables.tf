variable "project_name" {
  type        = string
  description = "Short project name used in AWS resource names."
}

variable "environment" {
  type        = string
  description = "Deployment environment name."
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC."
}

variable "azs" {
  type        = list(string)
  description = "Availability zones to use."
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for public subnets."
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for private subnets."
}

variable "single_nat_gateway" {
  type        = bool
  description = "Use one NAT gateway for cost-saving dev environments."
  default     = true
}

variable "tags" {
  type        = map(string)
  description = "Additional tags."
  default     = {}
}
