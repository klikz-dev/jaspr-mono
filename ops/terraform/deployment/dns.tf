
data "aws_route53_zone" "default" {
  name = local.ROOT_DOMAIN[var.environment]
}

resource "aws_route53_record" "api" {
  zone_id = data.aws_route53_zone.default.zone_id
  name    = local.API_DOMAIN[var.environment]
  type    = "A"

  alias {
    name                   = aws_lb.api-server-lb.dns_name
    zone_id                = aws_lb.api-server-lb.zone_id
    evaluate_target_health = false
  }
}
