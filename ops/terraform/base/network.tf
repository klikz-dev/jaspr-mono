
# Declare the data source
data "aws_availability_zones" "available" {
  state = "available"
}

module "vpc" {
  source     = "../modules/aws_vpc"
  namespace  = "jaspr"
  stage      = var.environment
  name       = "app"
  cidr_block = "10.0.0.0/22"
  # Connectria tag was put in place by their Ops team
  # Need to mimic it so we don't remove the tag with terraform deployments
  vpc_tags   = var.environment == local.PRODUCTION ? { ConnectriaManaged = "True" } : null
}

module "subnets" {
  source              = "../modules/aws-dynamic-subnets"
  namespace           = "jaspr"
  stage               = var.environment
  name                = "app"
  vpc_id              = module.vpc.vpc_id
  igw_id              = module.vpc.igw_id
  cidr_block          = module.vpc.vpc_cidr_block
  nat_gateway_enabled = true
  availability_zones  = [
    data.aws_availability_zones.available.names[0],
    data.aws_availability_zones.available.names[1]
  ]
  private_subnets_additional_tags = {
    tier = "private"
  }
  public_subnets_additional_tags = {
    tier = "public"
  }
}
