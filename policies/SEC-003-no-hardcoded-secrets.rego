package policies.security

# SEC-003: Secrets must not be hardcoded

__doc__ := {
  "id": "SEC-003",
  "title": "Secrets must not be hardcoded in code or config",
  "description": "Ensure AWS Secrets Manager or environment injection is used.",
  "enforcement": "hard"
}

violation[msg] {
  secret := input.code.secrets[_]
  not contains(secret, "AWS::SecretsManager")
  msg := sprintf("Hardcoded secret found: %s", [secret])
}
