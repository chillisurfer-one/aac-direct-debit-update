package policies.architecture.aac_105

default deny = []

# Require a data store related to audit or logging
deny[msg] {
  not some c
  c := input.containers[_]
  (contains(lower(c.name), "audit") or contains(lower(c.name), "log")) and
  contains(lower(c.technology), "postgresql") or contains(lower(c.technology), "rds") or c.stereotype[_] == "data_store"
} else {
  msg := "Architecture must include an audit log or persistent data store for compliance"
}