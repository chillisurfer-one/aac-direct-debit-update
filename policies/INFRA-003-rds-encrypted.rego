package policies.infrastructure

# INFRA-003: RDS must be encrypted

__doc__ := {
  "id": "INFRA-003",
  "title": "RDS encryption required",
  "description": "Ensure at-rest encryption is enabled for database instances.",
  "enforcement": "hard"
}

violation[msg] {
  rds := input.terraform.resources[_]
  rds.type == "aws_db_instance"
  rds.storage_encrypted != true
  msg := sprintf("RDS instance %s is not encrypted", [rds.name])
}
