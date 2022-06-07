data "aws_route53_zone" "edge" {
  name         = local.ROOT_DOMAIN[var.environment]
  private_zone = false
}
