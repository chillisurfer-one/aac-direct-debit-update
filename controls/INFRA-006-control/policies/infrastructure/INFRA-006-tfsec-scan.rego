
package policies.infrastructure

__doc__ := {
  "id": "INFRA-006",
  "title": "Terraform plans must pass tfsec checks with no HIGH/Critical issues",
  "description": "Ensure Terraform plan results are clean from high or critical tfsec rule violations.",
  "enforcement": "hard"
}

violation[msg] {
  r := input.results[_]
  r.severity == "HIGH" or r.severity == "CRITICAL"
  msg := sprintf("tfsec violation: [%s] %s (%s)", [r.severity, r.rule_id, r.description])
}
