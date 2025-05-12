# Use PostgreSQL for audit log storage

## Status
Accepted

## Context
We require a reliable, ACID-compliant data store to persist audit logs for financial transactions.

## Decision
We selected PostgreSQL due to its performance, transactional integrity, widespread adoption, and compatibility with AWS RDS.

## Consequences
Reliable audit storage, support for structured queries and scalability with managed RDS services.

