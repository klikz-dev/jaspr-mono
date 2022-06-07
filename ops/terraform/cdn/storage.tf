resource "aws_s3_bucket" "media" {
  #checkov:skip=CKV_AWS_19:Encryption of public media content is not required
  #checkov:skip=CKV_AWS_145:Encryption of public media content is not required
  #checkov:skip=CKV_AWS_52:MFA delete is not required
  #checkov:skip=CKV_AWS_144:Cross-Region replication is not required
  #checkov:skip=CKV_AWS_18:Access logging is not required for static media
  #checkov:skip=CKV_AWS_21:Versioning is not required for static media

  bucket = local.MEDIA_BUCKET_NAME[var.environment]

  tags = {
    Name        = "Media"
    Environment = var.environment
    Branch      = var.git_branch
  }
}

resource "aws_s3_bucket_acl" "media" {
  bucket = aws_s3_bucket.media.id
  acl    = "private" # Access allowed only via Cloudfront
}

resource "aws_s3_bucket_cors_configuration" "media" {
  bucket = aws_s3_bucket.media.bucket
  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["content-length"] # Do we still need this?
    max_age_seconds = 86400
  }
}

resource "aws_s3_bucket_public_access_block" "media" {
  #checkov:skip=CKV_AWS_54:Bucket media is public
  #checkov:skip=CKV_AWS_55:Bucket media is public
  #checkov:skip=CKV_AWS_56:Bucket media is public
  bucket            = aws_s3_bucket.media.id
  block_public_acls = true
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.media.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.cdn_access_identity.iam_arn]
    }
  }
}

resource "aws_s3_bucket_policy" "media_policy" {
  bucket = aws_s3_bucket.media.id
  policy = data.aws_iam_policy_document.s3_policy.json
}
