
output "rds_endpoint" {
  value = aws_db_instance.audit.endpoint
}

output "rds_identifier" {
  value = aws_db_instance.audit.id
}

output "secrets_arn" {
  value = aws_secretsmanager_secret.db_creds.arn
}
