package policies.architecture.aac_103

default deny = []

# Rule: only the 'VaultCoreClient' adapter is allowed to connect to the ThoughtMachine external system
deny[msg] {
  rel := input.relationships[_]
  rel.destination == "ThoughtMachine"
  rel.source != "VaultCoreClient"
  msg := sprintf("Container '%s' is not allowed to access ThoughtMachine directly", [rel.source])
}