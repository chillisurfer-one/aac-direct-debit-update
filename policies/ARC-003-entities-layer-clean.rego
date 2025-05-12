package policies.architecture

# ARC-003: Domain entities must not depend on controller or DTO packages

__doc__ := {
  "id": "ARC-003",
  "title": "Domain entities must not depend on controller or DTO packages",
  "description": "Enforces clean layering between domain, service, and controller layers.",
  "enforcement": "hard"
}

violation[msg] {
  d := input.code.domain_dependencies[_]
  d == "controller" or d == "dto"
  msg := sprintf("Domain layer depends on %s package", [d])
}
