resource "aws_route53_record" "cert_validation" {
  # Requires targeted apply.  See terraform issue:
  # https://github.com/hashicorp/terraform-provider-aws/issues/14447
  for_each = {
    for dvo in aws_acm_certificate.media.domain_validation_options : dvo.domain_name => {
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
  zone_id         = data.aws_route53_zone.media.zone_id
}

resource "aws_route53_record" "media" {
  name    = "${local.MEDIA_CDN_SUBDOMAIN[var.environment]}.${local.ROOT_DOMAIN[var.environment]}"
  zone_id = data.aws_route53_zone.media.zone_id
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.media.domain_name
    zone_id                = aws_cloudfront_distribution.media.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_acm_certificate" "media" {
  domain_name       = "${local.MEDIA_CDN_SUBDOMAIN[var.environment]}.${local.ROOT_DOMAIN[var.environment]}"
  validation_method = "DNS"

  tags = {
    Environment = var.environment
    Branch      = var.git_branch
  }

  lifecycle {
    create_before_destroy = true
  }

}

resource "aws_acm_certificate_validation" "media" {
  certificate_arn         = aws_acm_certificate.media.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
