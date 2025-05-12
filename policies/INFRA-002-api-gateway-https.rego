package policies.infrastructure

# INFRA-002: API Gateway must enforce HTTPS

__doc__ := {
  "id": "INFRA-002",
  "title": "API Gateway must use HTTPS",
  "description": "Prevent HTTP-only access to public APIs.",
  "enforcement": "hard"
}

violation[msg] {
  gw := input.terraform.resources[_]
  gw.type == "aws_api_gateway"
  gw.protocol != "HTTPS"
  msg := sprintf("API Gateway %s does not enforce HTTPS", [gw.name])
}
