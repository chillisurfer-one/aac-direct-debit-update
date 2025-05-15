package policies.architecture.aac_106

default deny = []

# At least one container must have 'secrets' in the name or be labeled <<secrets_store>>
deny[msg] {
  not some c
  c := input.containers[_]
  contains(lower(c.name), "secret") or
  c.stereotype[_] == "secrets_store"
  msg := "Architecture must declare a secrets management component (e.g., AWS Secrets Manager)"
}