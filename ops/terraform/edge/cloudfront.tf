resource "aws_cloudfront_origin_access_identity" "edge_access_identity" {
  comment = "Identity restricts EDGE access through cloudfront only"
}

resource "aws_cloudfront_distribution" "edge-dev" {
  count = var.environment == local.DEVELOPMENT ? 1 : 0
  #checkov:skip=CKV_AWS_86:Access logging is not required
  #checkov:skip=CKV_AWS_68:Web Application Firewall is not currently required for static media
  origin {
    domain_name = aws_s3_bucket.edge.bucket_regional_domain_name
    origin_id   = local.S3_EDGE_ORIGIN_ID[var.environment]

    custom_header {
      name  = "x-env-jaspr-cdn"
      value = "media.${local.ROOT_DOMAIN[var.environment]} release-media.${local.ROOT_DOMAIN[var.environment]}"
    }

    custom_header {
      name  = "x-env-api-root"
      value = "*.api.${local.ROOT_DOMAIN[var.environment]}"
    }

    custom_header {
      name  = "x-env-sentry-root"
      value = local.SENTRY_ROOT[var.environment]
    }

    custom_header {
      name  = "x-env-sentry-report"
      value = local.SENTRY_REPORT[var.environment]
    }

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.edge_access_identity.cloudfront_access_identity_path
    }
  }

  enabled         = true
  is_ipv6_enabled = true
  http_version    = "http2"
  comment         = "Frontend CDN"
  price_class     = "PriceClass_100" # North America and Europe

  default_root_object = "index.html"

  tags = {
    Environment = var.environment
    Branch      = var.git_branch
  }

  aliases = ["${local.EDGE_SUBDOMAIN[var.environment]}.${local.ROOT_DOMAIN[var.environment]}", "epic.${local.ROOT_DOMAIN[var.environment]}"]

  custom_error_response {
    error_code            = 403
    response_code         = 200
    error_caching_min_ttl = 3600
    response_page_path    = "/index.html"
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    error_caching_min_ttl = 3600
    response_page_path    = "/index.html"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.S3_EDGE_ORIGIN_ID[var.environment]

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"

    # min_ttl and max_ttl will squeeze any cache headers from the S3 origin.
    # If no cache headers are set at the origin, the default will apply
    min_ttl     = 0
    default_ttl = 3600
    max_ttl     = 31556952 # 1 Year
    compress    = true

    lambda_function_association {
      event_type   = "origin-response"
      lambda_arn   = aws_lambda_function.security_headers.qualified_arn
      include_body = false

    }

    lambda_function_association {
      event_type   = "viewer-request"
      lambda_arn   = aws_lambda_function.dev_redirect[0].qualified_arn
      include_body = false
    }

  }

  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = aws_acm_certificate_validation.edge.certificate_arn
    minimum_protocol_version       = "TLSv1.2_2019"
    ssl_support_method             = "sni-only"
  }
}


resource "aws_cloudfront_distribution" "edge-prod" {
  count = var.environment == local.DEVELOPMENT ? 0 : 1
  #checkov:skip=CKV_AWS_86:Access logging is not required
  #checkov:skip=CKV_AWS_68:Web Application Firewall is not currently required for static media
  origin {
    domain_name = aws_s3_bucket.edge.bucket_regional_domain_name
    origin_id   = local.S3_EDGE_ORIGIN_ID[var.environment]

    custom_header {
      name  = "x-env-jaspr-cdn"
      value = "media.${local.ROOT_DOMAIN[var.environment]}"
    }

    custom_header {
      name  = "x-env-api-root"
      value = "api.${local.ROOT_DOMAIN[var.environment]}"
    }

    custom_header {
      name  = "x-env-sentry-root"
      value = local.SENTRY_ROOT[var.environment]
    }

    custom_header {
      name  = "x-env-sentry-report"
      value = local.SENTRY_REPORT[var.environment]
    }

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.edge_access_identity.cloudfront_access_identity_path
    }
  }

  enabled         = true
  is_ipv6_enabled = true
  http_version    = "http2"
  comment         = "Frontend CDN"
  price_class     = "PriceClass_100" # North America and Europe

  default_root_object = "index.html"

  tags = {
    Environment = var.environment
    Branch      = var.git_branch
  }

  aliases = ["${local.EDGE_SUBDOMAIN[var.environment]}.${local.ROOT_DOMAIN[var.environment]}", "epic.${local.ROOT_DOMAIN[var.environment]}"]

  custom_error_response {
    error_code            = 403
    response_code         = 200
    error_caching_min_ttl = 3600
    response_page_path    = "/index.html"
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    error_caching_min_ttl = 3600
    response_page_path    = "/index.html"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.S3_EDGE_ORIGIN_ID[var.environment]

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"

    # min_ttl and max_ttl will squeeze any cache headers from the S3 origin.
    # If no cache headers are set at the origin, the default will apply
    min_ttl     = 0
    default_ttl = 3600
    max_ttl     = 31556952 # 1 Year
    compress    = true

    lambda_function_association {
      event_type   = "origin-response"
      lambda_arn   = aws_lambda_function.security_headers.qualified_arn
      include_body = false

    }

  }

  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = aws_acm_certificate_validation.edge.certificate_arn
    minimum_protocol_version       = "TLSv1.2_2019"
    ssl_support_method             = "sni-only"
  }
}