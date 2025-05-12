
package policies.infrastructure

__doc__ := {
  "id": "INFRA-002",
  "title": "API Gateway must use HTTPS-only endpoints",
  "description": "Ensure all API Gateway deployments enforce secure HTTPS-only communication.",
  "enforcement": "hard"
}

violation[msg] {
  gw := input.terraform.resources[_]
  gw.type == "aws_api_gateway"
  gw.protocol != "HTTPS"
  msg := sprintf("API Gateway '%s' is not enforcing HTTPS: protocol is %s", [gw.name, gw.protocol])
}
