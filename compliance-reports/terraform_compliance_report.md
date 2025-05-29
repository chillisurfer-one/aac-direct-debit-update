# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-05-29  
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
| Connection Discrepancies                                 | MandateUpdateService -> CloudWatch and VaultCoreClient -> CloudWatch connections are not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                           |

#### Remediation Steps:

1. **[Connection Implementation]:**
   - Ensure that the connections from MandateUpdateService and VaultCoreClient to CloudWatch are explicitly defined in the Terraform code. This could involve setting up appropriate IAM roles and policies to allow logging and metrics from these services to CloudWatch.

2. **[Resource Alignment]:**
   - Review the inclusion of `aws_cloudwatch_metric_alarm` in the Terraform code, as it is not represented in the architecture diagram. Ensure that its presence is justified or update the diagram to reflect its role in the observability module.
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
   - Ensure IAM roles and policies are defined to allow MandateUpdateController to read secrets from Secrets Manager.
   - Verify that the MandateUpdateService has the necessary permissions and configurations to write to the Audit Log (Amazon RDS PostgreSQL).

2. **[Security Enhancements]:**
   - Confirm that the RDS instance is placed within private subnets and that a NAT gateway is configured for outbound internet access if needed.
   - Review security group rules to ensure that only necessary traffic is allowed to the RDS instance.
---

### security-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | None                                                            |
| Components Present in PUML Diagram Not in Terraform Code | Amazon API Gateway                                              |
| Components Present in Terraform Code Not in PUML Diagram | aws_security_group.ecs, aws_security_group.alb, aws_security_group.rds |
| Connection Discrepancies                                 | Amazon API Gateway -> MandateUpdateController (Spring Boot): HTTPS Route is not implemented in Terraform code. VaultCoreClient (Adapter) -> Thought Machine Vault Core API: HTTPS + OAuth2 is not implemented in Terraform code. |
| Label/Annotation Discrepancies                           | No explicit labels or annotations in the diagram are reflected in the code. |

#### Remediation Steps:

1. **[Amazon API Gateway]:**
   - Add a resource definition for Amazon API Gateway in the Terraform code.
   - Ensure the API Gateway is configured to route requests to the MandateUpdateController.

2. **[Connection Implementations]:**
   - Implement the connection from Amazon API Gateway to MandateUpdateController (Spring Boot) using an HTTPS route in the Terraform code.
   - Implement the connection from VaultCoreClient (Adapter) to Thought Machine Vault Core API using HTTPS + OAuth2 in the Terraform code.

3. **[Label/Annotation Discrepancies]:**
   - Ensure that any labels or annotations present in the architecture diagram are reflected in the Terraform code, possibly through tags or comments.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

