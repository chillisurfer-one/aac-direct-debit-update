package policies.infrastructure

# INFRA-005: CloudWatch must capture logs and metrics

__doc__ := {
  "id": "INFRA-005",
  "title": "Enable CloudWatch logs and metrics",
  "description": "Ensure observability of app and infra with log groups and metric filters.",
  "enforcement": "hard"
}

violation[msg] {
  cw := input.terraform.resources[_]
  cw.type == "aws_cloudwatch_log_group"
  cw.metrics_enabled != true
  msg := sprintf("CloudWatch log group %s does not have metrics enabled", [cw.name])
}
