# Expose REST API with versioning (/api/v1/)

## Status
Accepted

## Context
The API must be backward compatible and allow safe iteration over time.

## Decision
We decided to version all public REST endpoints under `/api/v1/` to allow future evolution of the interface without breaking clients.

## Consequences
Clear migration path for clients. Adds some URL length and maintenance cost for versioning strategy.

