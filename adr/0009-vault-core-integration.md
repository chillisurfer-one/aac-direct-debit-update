# Integrate with Vault Core via secure OAuth2 client

## Status
Accepted

## Context
Communication with Thought Machine Vault Core must be authenticated and auditable.

## Decision
We use an OAuth2-secured REST client to call Vault Core APIs from the adapter layer.

## Consequences
Secure, standards-based integration with audit trail of token usage. Requires token rotation and error handling logic.

