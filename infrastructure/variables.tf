variable "project_name" {
  default = "__APP_HOSTNAME__"
}

variable "app_name" {
  default = "__APP_NAME__"
}

variable "aws_region" {
  default = "__AWS_REGION__"
}

variable "aws_account_id" {
  default = "__AWS_ACCOUNT_ID__"
}

variable "domain_name" {
  default = "__APP_HOSTNAME__"
}

variable "parent_zone_name" {
  default = "demo.apex.hcls.aws.dev"
}

variable "cognito_user_pool_id" {
  default = "__COGNITO_POOL_ID__"
}

variable "cognito_domain" {
  default = "__COGNITO_DOMAIN__"
}

variable "vpc_id" {
  description = "APEX shared VPC"
  default     = "vpc-0c8f1f0293c0d1d97"
}

variable "backend_image" {
  description = "Backend Docker image URI (set by CI/CD)"
  default     = ""
}

locals {
  environment = "prod"
}
