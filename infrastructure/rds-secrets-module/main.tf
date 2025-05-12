
provider "aws" {
  region = var.region
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.name_prefix}-db-subnet-group"
  subnet_ids = var.private_subnet_ids
  tags       = var.tags
}

resource "aws_db_instance" "audit" {
  identifier              = "${var.name_prefix}-audit-db"
  engine                  = "postgres"
  instance_class          = var.instance_class
  allocated_storage       = var.storage
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.this.name
  vpc_security_group_ids  = [var.db_sg_id]
  skip_final_snapshot     = true
  backup_retention_period = 7
  storage_encrypted       = true
  publicly_accessible     = false
  tags                    = var.tags
}

resource "aws_secretsmanager_secret" "db_creds" {
  name        = "${var.name_prefix}/rds/db-credentials"
  description = "RDS credentials for audit log database"
  tags        = var.tags
}

resource "aws_secretsmanager_secret_version" "db_creds_version" {
  secret_id     = aws_secretsmanager_secret.db_creds.id
  secret_string = jsonencode({
    username = var.db_username,
    password = var.db_password,
    engine   = "postgres",
    dbname   = aws_db_instance.audit.db_name,
    host     = aws_db_instance.audit.address,
    port     = aws_db_instance.audit.port
  })
}
