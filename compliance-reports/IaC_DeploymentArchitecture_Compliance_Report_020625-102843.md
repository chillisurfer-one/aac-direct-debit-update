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
| Components Present in Terraform Code Not in PUML Diagram | aws_cloudwatch_metric_alarm, aws_cloudwatch_log_group          |
| Connection Discrepancies                                 | MandateUpdateService -> CloudWatch and VaultCoreClient -> CloudWatch connections are not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                           |

#### Remediation Steps:

1. **[Define Connections]:**
   - Ensure that the connections from MandateUpdateService and VaultCoreClient to CloudWatch are explicitly defined in the Terraform code, possibly through IAM roles or policies that allow logging and metrics to be sent to CloudWatch.

2. **[Align Resources with Diagram]:**
   - Review the architecture diagram to ensure that the resources such as `aws_cloudwatch_metric_alarm` and `aws_cloudwatch_log_group` are accurately represented or justified within the context of the observability module. If necessary, update the diagram to reflect these resources or adjust the Terraform code to align with the intended architecture.
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
   - Verify that the MandateUpdateController has the necessary permissions to access the Secrets Manager using IAM roles.

2. **[Security and Network Configuration]:**
   - Confirm that the RDS instance is placed within private subnets and is not publicly accessible, as indicated in the Terraform code.
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

1. **Add Amazon API Gateway Resource:**
   - Define an `aws_api_gateway_rest_api` resource in the Terraform code to represent the Amazon API Gateway component.
   - Ensure the API Gateway is configured to route requests to the MandateUpdateController.

2. **Implement Connection:**
   - Establish the connection between the Amazon API Gateway and the MandateUpdateController using appropriate Terraform resources such as `aws_api_gateway_integration` and `aws_api_gateway_method`.
   - Ensure the connection uses HTTPS as specified in the architecture diagram.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

