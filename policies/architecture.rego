package directdebit.architecture

deny["S3 bucket must have encryption"] {
  input.resource_type == "aws_s3_bucket"
  not input.encryption_enabled
}
