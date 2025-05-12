package policies.architecture

# ARC-001: DTOs must be used for controller inputs/outputs

__doc__ := {
  "id": "ARC-001",
  "title": "DTOs must be used for all controller inputs/outputs",
  "description": "Ensure that controllers do not expose JPA entities directly.",
  "enforcement": "hard"
}

violation[msg] {
  c := input.code.controllers[_]
  not endswith(c.input_class, "DTO")
  msg := sprintf("Controller %s uses non-DTO input: %s", [c.name, c.input_class])
}
