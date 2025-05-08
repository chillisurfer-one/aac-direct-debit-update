# ADR 0002: Integrate with Thought Machine for Direct Debit Updates

## Status
Accepted

## Context
The Direct Debit Update Service must update mandates in a secure and compliant manner. Thought Machine provides core banking APIs with full regulatory compliance.

## Decision
Integrate with Thought Machine via secure REST API using mutual TLS authentication.

## Consequences
- Requires client credential management.
- Enforces strict API contract with external core banking service.
