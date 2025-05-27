package policies.security

# SEC-004: OAuth2 clients must not bypass token validation

__doc__ := {
  "id": "SEC-004",
  "title": "OAuth2 token validation must be enabled",
  "description": "Ensure token validation is enabled for OAuth2 clients.",
  "enforcement": "hard"
}

violation[msg] {
  input.spring_security.oauth2.enabled == true
  not input.spring_security.oauth2.validate_tokens
  msg := "OAuth2 is enabled but token validation is not configured."
}
