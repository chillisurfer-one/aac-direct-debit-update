package policies.architecture

# ARC-004: All exceptions must be handled via @ControllerAdvice

__doc__ := {
  "id": "ARC-004",
  "title": "Central error handling with @ControllerAdvice",
  "description": "Ensure that exceptions are handled in one centralized handler.",
  "enforcement": "hard"
}

violation[msg] {
  not input.code.annotations[_] == "@ControllerAdvice"
  msg := "Missing global exception handler annotated with @ControllerAdvice"
}
