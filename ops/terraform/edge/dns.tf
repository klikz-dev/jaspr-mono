resource "aws_acm_certificate" "edge" {
  domain_name               = "${local.EDGE_SUBDOMAIN[var.environment]}.${local.ROOT_DOMAIN[var.environment]}"
  subject_alternative_names = ["epic.${local.ROOT_DOMAIN[var.environment]}"]
  validation_method         = "DNS"

  tags = {
    Environment = var.environment
    Branch      = var.git_branch
  }

  lifecycle {
    create_before_destroy = true
  }

}

resource "aws_route53_record" "cert_validation" {
  # Requires AWS Provider > 3
  for_each = {
    for dvo in aws_acm_certificate.edge.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.edge.zone_id

  depends_on = [aws_acm_certificate.edge]
}

resource "aws_route53_record" "edge-dev" {
  count = var.environment == local.DEVELOPMENT ? 1: 0
  name    = "${local.EDGE_SUBDOMAIN[var.environment]}.${local.ROOT_DOMAIN[var.environment]}"
  zone_id = data.aws_route53_zone.edge.zone_id
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.edge-dev[0].domain_name
    zone_id                = aws_cloudfront_distribution.edge-dev[0].hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "epic-dev" {
  count = var.environment == local.DEVELOPMENT ? 1: 0
  name    = "epic.${local.ROOT_DOMAIN[var.environment]}"
  zone_id = data.aws_route53_zone.edge.zone_id
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.edge-dev[0].domain_name
    zone_id                = aws_cloudfront_distribution.edge-dev[0].hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "edge-prod" {
  count = var.environment == local.DEVELOPMENT ? 0: 1
  name    = "${local.EDGE_SUBDOMAIN[var.environment]}.${local.ROOT_DOMAIN[var.environment]}"
  zone_id = data.aws_route53_zone.edge.zone_id
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.edge-prod[0].domain_name
    zone_id                = aws_cloudfront_distribution.edge-prod[0].hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "epic-prod" {
  count = var.environment == local.DEVELOPMENT ? 0: 1
  name    = "epic.${local.ROOT_DOMAIN[var.environment]}"
  zone_id = data.aws_route53_zone.edge.zone_id
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.edge-prod[0].domain_name
    zone_id                = aws_cloudfront_distribution.edge-prod[0].hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_acm_certificate_validation" "edge" {
  certificate_arn         = aws_acm_certificate.edge.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
