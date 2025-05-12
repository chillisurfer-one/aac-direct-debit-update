# Run service on AWS ECS Fargate

## Status
Accepted

## Context
We want to run our service in containers without managing infrastructure.

## Decision
We chose AWS ECS with Fargate to eliminate EC2 provisioning and use a serverless container model.

## Consequences
Improved scalability, reduced operational overhead, but less fine-grained control over network/storage settings.

