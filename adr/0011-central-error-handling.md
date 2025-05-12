# Handle errors centrally using @ControllerAdvice

## Status
Accepted

## Context
Error handling must be consistent, secure, and helpful for clients.

## Decision
We use a global exception handler with @ControllerAdvice to catch and format all API errors uniformly.

## Consequences
Improves developer experience, consistent client responses, and reduces duplication in controller code.

