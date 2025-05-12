# Use Amazon API Gateway as HTTP entrypoint

## Status
Accepted

## Context
We need to expose the service securely with throttling, logging, and easy integration with other AWS services.

## Decision
We decided to use Amazon API Gateway as the public interface to the ECS microservice.

## Consequences
Centralized access control, rate limiting, and simplified SSL/TLS handling.

