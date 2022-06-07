resource "aws_s3_bucket" "edge" {
  #checkov:skip=CKV_AWS_19:Encryption of public media content is not required
  #checkov:skip=CKV_AWS_145:Encryption of public media content is not required
  #checkov:skip=CKV_AWS_52:MFA delete is not required
  #checkov:skip=CKV_AWS_144:Cross-Region replication is not required
  #checkov:skip=CKV_AWS_18:Access logging is not required for static media
  #checkov:skip=CKV_AWS_21:Versioning is not required for static media
  #checkov:skip=CKV2_AWS_6:Bucket media is public
  bucket = local.BUCKET_NAME[var.environment]
  acl    = "private" # Access allowed only via Cloudfront

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["content-length"] # Do we still need this?
    max_age_seconds = 86400
  }

  tags = {
    Name        = "Frontend CDN"
    Environment = var.environment
    Branch      = var.git_branch
  }
}

resource "aws_s3_bucket_public_access_block" "edge" {
  #checkov:skip=CKV_AWS_54:Bucket media is public
  #checkov:skip=CKV_AWS_55:Bucket media is public
  #checkov:skip=CKV_AWS_56:Bucket media is public
  bucket            = aws_s3_bucket.edge.id
  block_public_acls = true
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.edge.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.edge_access_identity.iam_arn]
    }
  }
}

resource "aws_s3_bucket_policy" "edge_policy" {
  bucket = aws_s3_bucket.edge.id
  policy = data.aws_iam_policy_document.s3_policy.json
}
