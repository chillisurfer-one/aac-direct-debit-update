
package policies.infrastructure

__doc__ := {
  "id": "INFRA-003",
  "title": "Audit logs must be stored in encrypted RDS",
  "description": "Ensure database instances used for audit logs are encrypted at rest.",
  "enforcement": "hard"
}

violation[msg] {
  rds := input.terraform.resources[_]
  rds.type == "aws_db_instance"
  rds.name == "audit-logs-db"
  not rds.storage_encrypted
  msg := sprintf("RDS instance '%s' (used for audit logs) is not encrypted.", [rds.name])
}
