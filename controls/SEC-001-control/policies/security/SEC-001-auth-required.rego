package policies.security

# SEC-001: All REST endpoints must require authentication

__doc__ := {
  "id": "SEC-001",
  "title": "All REST endpoints must require authentication",
  "description": "Ensure all OpenAPI paths define security requirements.",
  "enforcement": "hard"
}

violation[msg] {
  some path, method
  not input.openapi.paths[path][method].security
  msg := sprintf("Endpoint %s %s is missing authentication requirements.", [method, path])
}
