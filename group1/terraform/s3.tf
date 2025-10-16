resource "aws_s3_bucket" "poudlard_backups" {
  bucket = "poudlard-backups-${random_id.bucket_id.hex}"
  acl    = "private"
}

resource "random_id" "bucket_id" {
  byte_length = 4
}

resource "aws_iam_user" "es_snapshot_user" {
  name = "es-snapshot-user"
}

resource "aws_iam_access_key" "es_snapshot_key" {
  user = aws_iam_user.es_snapshot_user.name
}

resource "aws_iam_policy" "es_s3_policy" {
  name = "es-s3-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        Effect = "Allow",
        Resource = ["${aws_s3_bucket.poudlard_backups.arn}/*","${aws_s3_bucket.poudlard_backups.arn}" ]
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "attach" {
  user       = aws_iam_user.es_snapshot_user.name
  policy_arn = aws_iam_policy.es_s3_policy.arn
}
*** End Patch
