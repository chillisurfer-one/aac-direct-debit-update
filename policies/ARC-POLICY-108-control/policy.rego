package policies.architecture.aac_108

default deny = []

# At least one container must be labeled as <<observability>> or include 'cloudwatch' in the name
deny[msg] {
  not some c
  c := input.containers[_]
  contains(lower(c.name), "cloudwatch") or
  c.stereotype[_] == "observability"
  msg := "Architecture must include at least one observability component (e.g., CloudWatch)"
}