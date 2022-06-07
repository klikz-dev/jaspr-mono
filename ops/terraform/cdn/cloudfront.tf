resource "aws_cloudfront_origin_access_identity" "cdn_access_identity" {
  comment = "Identity restricts CDN access through cloudfront only"
}

data "aws_cloudfront_origin_request_policy" "cdn_origin_request_policy" {
  name = "Managed-CORS-S3Origin"
}
data "aws_cloudfront_cache_policy" "cdn_cache_policy" {
  name = "Managed-CachingOptimizedForUncompressedObjects"
}
data "aws_cloudfront_response_headers_policy" "cdn_response_headers_policy" {
  name = "Managed-CORS-With-Preflight"
}


resource "aws_cloudfront_distribution" "media" {
  #checkov:skip=CKV_AWS_86:Access logging is not required
  #checkov:skip=CKV_AWS_68:Web Application Firewall is not currently required for static media
  origin {
    domain_name = aws_s3_bucket.media.bucket_regional_domain_name
    origin_id   = local.S3_MEDIA_CDN_ORIGIN_ID[var.environment]

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.cdn_access_identity.cloudfront_access_identity_path
    }
  }

  enabled         = true
  is_ipv6_enabled = true
  http_version    = "http2"
  comment         = var.git_branch == "release" ? "Release Media CDN" : "Media CDN"
  price_class     = "PriceClass_100" # North America and Europe

  tags = {
    Environment = var.environment
    Branch      = var.git_branch
  }

  aliases = ["${local.MEDIA_CDN_SUBDOMAIN[var.environment]}.${local.ROOT_DOMAIN[var.environment]}"]

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  default_cache_behavior {
    allowed_methods            = ["GET", "HEAD", "OPTIONS"]
    cached_methods             = ["GET", "HEAD", "OPTIONS"]
    target_origin_id           = local.S3_MEDIA_CDN_ORIGIN_ID[var.environment]
    origin_request_policy_id   = data.aws_cloudfront_origin_request_policy.cdn_origin_request_policy.id
    cache_policy_id            = data.aws_cloudfront_cache_policy.cdn_cache_policy.id
    response_headers_policy_id = data.aws_cloudfront_response_headers_policy.cdn_response_headers_policy.id

    viewer_protocol_policy = "redirect-to-https"
  }

  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = aws_acm_certificate_validation.media.certificate_arn
    minimum_protocol_version       = "TLSv1.2_2019"
    ssl_support_method             = "sni-only"
  }
}
