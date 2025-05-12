
package policies.infrastructure

__doc__ := {
  "id": "INFRA-004",
  "title": "Secrets Manager must store DB and API credentials",
  "description": "Ensure sensitive credentials are not stored in plain text or environment variables.",
  "enforcement": "hard"
}

violation[msg] {
  res := input.terraform.resources[_]
  is_credential(res.name)
  not using_secretsmanager(res)
  msg := sprintf("Sensitive credential '%s' is not stored in Secrets Manager", [res.name])
}

is_credential(name) {
  contains(lower(name), "db") or contains(lower(name), "api")
}

using_secretsmanager(res) {
  res.type == "aws_secretsmanager_secret"
}
