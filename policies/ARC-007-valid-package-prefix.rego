package policies.architecture

# ARC-007: All packages must follow the base namespace convention

__doc__ := {
  "id": "ARC-007",
  "title": "Use approved package naming conventions",
  "description": "Ensure all packages follow modular structure: com.mycompany.directdebitupdate.*",
  "enforcement": "soft"
}

violation[msg] {
  p := input.code.packages[_]
  not startswith(p, "com.mycompany.directdebitupdate")
  msg := sprintf("Package does not conform: %s", [p])
}
