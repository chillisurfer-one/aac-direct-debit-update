
package policies.infrastructure

__doc__ := {
  "id": "INFRA-005",
  "title": "CloudWatch must capture logs and custom metrics",
  "description": "Ensure all applications push logs and metrics to CloudWatch for observability.",
  "enforcement": "hard"
}

violation[msg] {
  res := input.terraform.resources[_]
  not res.cloudwatch_logs_enabled
  msg := sprintf("Resource '%s' does not have CloudWatch logs enabled.", [res.name])
}
