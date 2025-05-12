package policies.architecture

# ARC-002: Repositories must not be injected into controllers

__doc__ := {
  "id": "ARC-002",
  "title": "Repositories must not be injected into controllers",
  "description": "Ensure that only services are injected into controller classes.",
  "enforcement": "hard"
}

violation[msg] {
  ctrl := input.code.controllers[_]
  repo := ctrl.dependencies[_]
  repo.type == "Repository"
  msg := sprintf("Repository %s injected into controller %s", [repo.name, ctrl.name])
}
