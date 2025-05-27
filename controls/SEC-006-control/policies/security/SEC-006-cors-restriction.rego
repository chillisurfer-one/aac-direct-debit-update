package policies.security

# SEC-006: CORS must not be unrestricted in production

__doc__ := {
  "id": "SEC-006",
  "title": "Restrict CORS to specific origins",
  "description": "Avoid wildcard origins in CORS configuration.",
  "enforcement": "hard"
}

violation[msg] {
  input.config.cors.allowed_origins[_] == "*"
  msg := "CORS is configured with wildcard origin '*'"
}
