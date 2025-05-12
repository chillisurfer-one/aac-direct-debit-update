# Enforce DTO-layer boundaries (no entity leakage)

## Status
Accepted

## Context
Exposing JPA entities directly over the wire couples our persistence model to API clients, risking breakage and security issues.

## Decision
We use Data Transfer Objects (DTOs) for all inputs and outputs. Entities remain internal to the service.

## Consequences
Improved separation of concerns and ability to refactor entities without breaking API contracts. Requires manual or mapped transformations.

