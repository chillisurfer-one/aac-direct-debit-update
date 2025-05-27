package policies.security

# SEC-002: No @PermitAll or unsecured /api/** paths

__doc__ := {
  "id": "SEC-002",
  "title": "No @PermitAll or unsecured /api/** paths",
  "description": "Avoid exposing unsecured public endpoints.",
  "enforcement": "hard"
}

violation[msg] {
  input.spring_security.annotations[_] == "@PermitAll"
  msg := "Annotation @PermitAll detected in Spring Security config."
}

violation[msg] {
  input.spring_security.unsecured_paths[_] == "/api/"
  msg := "Unsecured /api/ path detected in Spring Security config."
}
