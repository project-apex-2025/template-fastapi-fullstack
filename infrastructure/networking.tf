# Networking — reference the APEX shared VPC and subnets in the 090 account

data "aws_vpc" "main" {
  id = var.vpc_id
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
  filter {
    name   = "tag:Name"
    values = ["apex-shared-private-*"]
  }
}

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
  filter {
    name   = "tag:Name"
    values = ["apex-shared-public-*"]
  }
}

data "aws_route53_zone" "parent" {
  name = var.parent_zone_name
}
