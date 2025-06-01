# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-06-01  
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

1. **[Define Connections]:**
   - Ensure that the connections from MandateUpdateService and VaultCoreClient to CloudWatch are explicitly defined in the Terraform code, possibly through IAM roles or policies that allow logging and metrics to be sent to CloudWatch.

2. **[Align Resources with Diagram]:**
   - Review the architecture diagram to ensure that the resources like `aws_cloudwatch_metric_alarm` and `aws_cloudwatch_log_group` are accurately represented or justified within the context of the observability module. If necessary, update the diagram to reflect these resources or adjust the Terraform code to align with the intended architecture.
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

1. **Define IAM Permissions for Secrets Access:**
   - Ensure that the IAM role associated with the MandateUpdateController has permissions to access the Secrets Manager secret.
   - Add IAM policy to allow `secretsmanager:GetSecretValue` for the secret ARN.

2. **Document Connection in Terraform Code:**
   - Explicitly document the connection between MandateUpdateController and Secrets Manager in the Terraform code, possibly through comments or additional resources that define IAM roles and policies.
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

1. **[Amazon API Gateway]:**
   - Add a Terraform resource for Amazon API Gateway to the `security-module`.
   - Ensure the API Gateway is configured to route requests to the MandateUpdateController (Spring Boot).

2. **[Connection Implementation]:**
   - Implement the connection from Amazon API Gateway to MandateUpdateController (Spring Boot) in the Terraform code.
   - Ensure the connection uses HTTPS as specified in the architecture diagram.

3. **[Security Group Review]:**
   - Review the security groups defined in the Terraform code to ensure they align with the architecture's security requirements.
   - Consider adding any missing security configurations that might be necessary for the API Gateway and its connections.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

