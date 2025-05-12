package policies.infrastructure

# INFRA-006: tfsec must pass with no HIGH or CRITICAL issues

__doc__ := {
  "id": "INFRA-006",
  "title": "tfsec report must be clean of high/critical issues",
  "description": "Ensure infrastructure config passes security scans before deployment.",
  "enforcement": "hard"
}

violation[msg] {
  input.tfsec.summary.high > 0
  msg := "tfsec detected high severity issues"
}

violation[msg] {
  input.tfsec.summary.critical > 0
  msg := "tfsec detected critical severity issues"
}
