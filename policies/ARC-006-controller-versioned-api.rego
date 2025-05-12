package policies.architecture

# ARC-006: Each REST controller must be versioned (/api/v1/)

__doc__ := {
  "id": "ARC-006",
  "title": "REST APIs must be versioned",
  "description": "Ensure all public APIs use URI versioning strategy.",
  "enforcement": "hard"
}

violation[msg] {
  not startswith(input.openapi.paths[_], "/api/v1/")
  msg := "Unversioned REST endpoint found"
}
