# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-06-04  
## Executive Summary

This report evaluates the compliance of Terraform modules against the architecture diagram. Of the 4 modules evaluated, 1 is compliant and 3 require remediation.

## Module to Component Mapping

The following table shows which components from the architecture diagram are mapped to each module:

| Module Name | Components |
|-------------|------------|
| ecs-fargate-module | MandateUpdateController (Spring Boot), MandateUpdateService (Spring Logic), VaultCoreClient (Adapter) |
| observability-module | CloudWatch |
| rds-secrets-module | Secrets Manager, Audit Log (Amazon RDS PostgreSQL) |
| security-module | Amazon API Gateway |

## Module Compliance Summary

| Module Name | Status | Action Required |
|-------------|--------|----------------|
| ecs-fargate-module | ✅ COMPLIANT | No |
| observability-module | ❌ NON-COMPLIANT | Yes |
| rds-secrets-module | ❌ NON-COMPLIANT | Yes |
| security-module | ❌ NON-COMPLIANT | Yes |

## Non-Compliant Modules and Remediation Steps

### observability-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | CloudWatch                                                     |
| Components Present in PUML Diagram Not in Terraform Code | None                                                           |
| Components Present in Terraform Code Not in PUML Diagram | aws_cloudwatch_metric_alarm, aws_cloudwatch_log_group          |
| Connection Discrepancies                                 | MandateUpdateService -> CloudWatch and VaultCoreClient -> CloudWatch connections are not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                           |

#### Remediation Steps:

1. **[Connection Implementation]:**
   - Ensure that the connections from MandateUpdateService and VaultCoreClient to CloudWatch are explicitly defined in the Terraform code. This could involve setting up appropriate IAM roles and policies to allow logging and metrics from these services to CloudWatch.

2. **[Resource Alignment]:**
   - Align the Terraform resources with the architecture diagram by ensuring that the aws_cloudwatch_metric_alarm and aws_cloudwatch_log_group are represented in the diagram if they are part of the observability module's scope.
---

### rds-secrets-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | Secrets Manager, Audit Log (Amazon RDS PostgreSQL)              |
| Components Present in PUML Diagram Not in Terraform Code | None                                                            |
| Components Present in Terraform Code Not in PUML Diagram | aws_db_subnet_group.this                                        |
| Connection Discrepancies                                 | MandateUpdateController -> Secrets Manager connection not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                            |

#### Remediation Steps:

1. **[Connection Definition]:**
   - Ensure IAM roles and policies are defined in Terraform to allow MandateUpdateController to read secrets from Secrets Manager.
   - Verify that the IAM role used by MandateUpdateController has permissions to access the secrets stored in Secrets Manager.

2. **[Security and Network Configuration]:**
   - Confirm that the RDS instance is placed in private subnets and is not publicly accessible, as indicated in the Terraform code.
   - Ensure that the security group associated with the RDS instance allows connections only from trusted sources, such as the ECS Fargate Cluster.
---

### security-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | None                                                            |
| Components Present in PUML Diagram Not in Terraform Code | Amazon API Gateway                                              |
| Components Present in Terraform Code Not in PUML Diagram | aws_security_group.ecs, aws_security_group.alb, aws_security_group.rds |
| Connection Discrepancies                                 | Amazon API Gateway -> MandateUpdateController (Spring Boot): HTTPS Route not implemented in Terraform code |
| Label/Annotation Discrepancies                           | None                                                            |

#### Remediation Steps:

1. **[Amazon API Gateway Configuration]:**
   - Add a resource block for `aws_api_gateway_rest_api` to define the API Gateway.
   - Ensure the API Gateway is configured to route requests to the MandateUpdateController (Spring Boot) using HTTPS.

2. **[Connection Implementation]:**
   - Implement the connection from Amazon API Gateway to MandateUpdateController in Terraform using appropriate resources like `aws_api_gateway_integration`.
   - Ensure OAuth2 configuration for VaultCoreClient (Adapter) to Thought Machine Vault Core API is defined in Terraform, possibly using `aws_api_gateway_authorizer` or similar resources.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

