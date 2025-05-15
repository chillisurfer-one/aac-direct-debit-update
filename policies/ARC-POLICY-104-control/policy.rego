package policies.architecture.aac_104

default deny = []

# Deny if a container makes an external call and is not marked as using secrets
deny[msg] {
  rel := input.relationships[_]
  rel.external == true
  container := input.containers[_]
  container.alias == rel.source
  not container.stereotype[_] == "uses_secret"
  msg := sprintf("Container '%s' makes external calls but is not annotated <<uses_secret>>", [rel.source])
}