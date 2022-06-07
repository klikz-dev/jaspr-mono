locals {
  enabled                                         = module.this.enabled
  enable_default_security_group_with_custom_rules = var.enable_default_security_group_with_custom_rules && local.enabled ? 1 : 0
  enable_internet_gateway                         = var.enable_internet_gateway && local.enabled ? 1 : 0
  vpc_id                                          = aws_vpc.default[0].id #join("", aws_vpc.default.*.id)
}


module "label" {
  source = "../null-label"

  context = module.this.context
}

resource "aws_vpc" "default" {
  count                            = local.enabled ? 1 : 0
  cidr_block                       = var.cidr_block
  instance_tenancy                 = var.instance_tenancy
  enable_dns_hostnames             = var.enable_dns_hostnames
  enable_dns_support               = var.enable_dns_support
  enable_classiclink               = var.enable_classiclink
  enable_classiclink_dns_support   = var.enable_classiclink_dns_support
  assign_generated_ipv6_cidr_block = true
  tags                             = var.vpc_tags != null ? merge(module.label.tags, var.vpc_tags) : module.label.tags
}

# If `aws_default_security_group` is not defined, it would be created implicitly with access `0.0.0.0/0`
resource "aws_default_security_group" "default" {
  count  = local.enable_default_security_group_with_custom_rules
  vpc_id = local.vpc_id

  tags = merge(module.label.tags, { Name = "Default Security Group" })
}

resource "aws_internet_gateway" "default" {
  count  = local.enable_internet_gateway
  vpc_id = local.vpc_id
  tags   = module.label.tags
}
