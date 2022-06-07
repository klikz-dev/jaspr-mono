
resource "aws_wafv2_web_acl_association" "alb-waf" {
  resource_arn = aws_lb.api-server-lb.arn
  web_acl_arn  = aws_wafv2_web_acl.alb-waf.arn
}

resource "aws_wafv2_web_acl" "alb-waf" {
  name        = "alb-waf-${local.deployment_name}"
  description = "API Server WAF ACL"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "rate-limits"
    priority = 1

    action {
      count {}
    }

    statement {
      rate_based_statement {
        limit              = 1000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "exceed-rate-limit-requests"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "api-lb-requests"
    sampled_requests_enabled   = true
  }

  tags = local.STANDARD_TAGS
}