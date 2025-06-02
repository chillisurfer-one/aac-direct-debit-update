# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-06-02  
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
| Components Present in Terraform Code Not in PUML Diagram | aws_cloudwatch_metric_alarm                                    |
| Connection Discrepancies                                 | MandateUpdateService and VaultCoreClient connections to CloudWatch are not explicitly defined in Terraform. |
| Label/Annotation Discrepancies                           | No explicit labels or annotations for CloudWatch connections in Terraform. |

#### Remediation Steps:

1. **[Define Connections]:**
   - Ensure that the connections from MandateUpdateService and VaultCoreClient to CloudWatch are explicitly defined in the Terraform code. This could involve setting up appropriate IAM roles and policies to allow these services to send logs and metrics to CloudWatch.

2. **[Update Documentation]:**
   - Add comments or documentation in the Terraform code to reflect the intended connections and usage of CloudWatch for observability, ensuring alignment with the architecture diagram.

3. **[Review Alarms]:**
   - Consider whether the `aws_cloudwatch_metric_alarm` should be represented in the architecture diagram or if it should be documented as part of the observability strategy.
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

1. **Connection Implementation:**
   - Ensure IAM roles and policies are defined to allow MandateUpdateController to read secrets from Secrets Manager.
   - Verify that the MandateUpdateService has the necessary permissions and configurations to write to the Audit Log (Amazon RDS PostgreSQL).

2. **Documentation and Code Alignment:**
   - Update Terraform code to include any missing IAM roles or policies that facilitate the connections specified in the architecture diagram.
   - Ensure that all components and connections in the architecture diagram are accurately represented in the Terraform code.
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
   - Implement the connection from Amazon API Gateway to MandateUpdateController using `aws_api_gateway_integration` to define the HTTPS route.

3. **[Security Group Review]:**
   - Review the security groups defined in the Terraform code to ensure they align with the architecture diagram and intended security posture.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

