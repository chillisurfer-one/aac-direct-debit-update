package policies.architecture.aac_102

default deny = []

# Define external systems (you could make this dynamic or regex-driven)
external_systems = {"ClientApp", "ExternalUser", "CRM"}

# Define valid API Gateway aliases (can be updated to support stereotypes in advanced versions)
api_gateway_aliases = {"ApiGateway"}

# Deny if any external system connects directly to a non-API-Gateway
deny[msg] {
  rel := input.relationships[_]
  external_systems[rel.source]
  not api_gateway_aliases[rel.destination]
  msg := sprintf("External system '%s' must not access '%s' directly", [rel.source, rel.destination])
}