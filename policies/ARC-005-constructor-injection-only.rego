package policies.architecture

# ARC-005: Use constructor injection, not field injection

__doc__ := {
  "id": "ARC-005",
  "title": "Use constructor injection",
  "description": "Improve immutability and testability by enforcing constructor injection.",
  "enforcement": "hard"
}

violation[msg] {
  inj := input.code.injections[_]
  inj.method != "constructor"
  msg := sprintf("Non-constructor injection used in %s", [inj.class])
}
