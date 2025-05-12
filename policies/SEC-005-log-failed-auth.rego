package policies.security

# SEC-005: Mandatory logging of failed login/API attempts

__doc__ := {
  "id": "SEC-005",
  "title": "Log all failed authentication attempts",
  "description": "Ensure logs capture failed authentication for audit trail.",
  "enforcement": "soft"
}

violation[msg] {
  not input.logs.contains_failed_login_logs
  msg := "Failed login attempts are not being logged."
}
