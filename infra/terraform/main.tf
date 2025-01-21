provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "django_model_api_static" {
  bucket = "django-model-api-static"

  tags = {
    Name        = "django-model-api-static"
    Environment = "Dev"
    Client      = "DjangoModelAPI"
  }
}

resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for django-model-api-static"
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.django_model_api_static.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.oai.iam_arn]
    }
  }
}

resource "aws_s3_bucket_policy" "django_model_api_static_policy" {
  bucket = aws_s3_bucket.django_model_api_static.bucket
  policy = data.aws_iam_policy_document.s3_policy.json
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = aws_s3_bucket.django_model_api_static.bucket_regional_domain_name
    origin_id   = "S3-django-model-api-static"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  default_root_object = "index.html"  # Set this according to your needs

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-django-model-api-static"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"  # Enforce HTTPS
  }

  price_class = "PriceClass_100"  # Choose the appropriate price class

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

resource "aws_iam_policy" "s3_upload_policy" {
  name        = "S3UploadDjangoModelAPIStatic"
  description = "Policy for uploading to S3 bucket django-model-api-static"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "VisualEditor0",
        Effect = "Allow",
        Action = "s3:ListBucket",
        Resource = "${aws_s3_bucket.django_model_api_static.arn}"
      },
      {
        Sid    = "VisualEditor1",
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:GetObject"
        ],
        Resource = [
          "${aws_s3_bucket.django_model_api_static.arn}",
          "${aws_s3_bucket.django_model_api_static.arn}/*"
        ]
      }
    ]
  })
}


resource "aws_iam_user" "s3_uploader_user" {
  name = "s3-uploader-django-model-api-static"
}

resource "aws_iam_user_policy_attachment" "s3_upload_user_policy_attachment" {
  user       = aws_iam_user.s3_uploader_user.name
  policy_arn = aws_iam_policy.s3_upload_policy.arn
}

resource "aws_iam_access_key" "s3_uploader_user_key" {
  user = aws_iam_user.s3_uploader_user.name
}

output "access_key_id" {
  value = aws_iam_access_key.s3_uploader_user_key.id
}

output "secret_access_key" {
  value = aws_iam_access_key.s3_uploader_user_key.secret
  sensitive = true
}
