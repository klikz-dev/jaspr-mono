data "aws_route53_zone" "media" {
  name         = local.ROOT_DOMAIN[var.environment]
  private_zone = false
}
