# Store secrets in AWS Secrets Manager

## Status
Accepted

## Context
Hardcoded secrets or environment variables expose security risks.

## Decision
We use AWS Secrets Manager to store API tokens, DB credentials, and OAuth secrets securely.

## Consequences
Improved security posture, auditability, and dynamic secret rotation support.

