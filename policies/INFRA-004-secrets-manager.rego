package policies.infrastructure

# INFRA-004: Store secrets in AWS Secrets Manager

__doc__ := {
  "id": "INFRA-004",
  "title": "Secrets must be stored in Secrets Manager",
  "description": "Avoid hardcoding sensitive values or using plaintext env vars.",
  "enforcement": "hard"
}

violation[msg] {
  secret := input.terraform.resources[_]
  secret.type == "aws_secretsmanager_secret"
  not (contains(secret.name, "db") or contains(secret.name, "api"))
  msg := sprintf("Secrets resource %s is not properly named", [secret.name])
}
