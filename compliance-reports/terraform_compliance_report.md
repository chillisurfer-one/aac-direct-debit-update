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
   - Ensure that the connections from MandateUpdateService and VaultCoreClient to CloudWatch are explicitly defined in the Terraform code, possibly through IAM roles or policies that allow logging and metrics to be sent to CloudWatch.

2. **[Resource Alignment]:**
   - Review the inclusion of `aws_cloudwatch_metric_alarm` in the Terraform code to ensure it aligns with the intended observability scope of the module. If it is relevant, ensure its purpose is documented and reflected in the architecture diagram. If not, consider removing or relocating it to a more appropriate module.
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
   - Verify that the MandateUpdateController has the necessary permissions to access the secrets stored in Secrets Manager.

2. **[Security and Network Configuration]:**
   - Confirm that the RDS instance is placed in private subnets and is not publicly accessible, as indicated in the Terraform code.
   - Ensure that the security group associated with the RDS instance allows access only from necessary components, such as MandateUpdateService.
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
   - Ensure the API Gateway is configured to route requests to the MandateUpdateController (Spring Boot) using HTTPS.

2. **Implement Connection:**
   - Establish the connection between the Amazon API Gateway and the MandateUpdateController in the Terraform code.
   - Use `aws_api_gateway_integration` to define the integration with the ECS Fargate service hosting the MandateUpdateController.

3. **Review Security Group Usage:**
   - Verify if the security groups defined (ecs, alb, rds) are necessary for the "security-module" or if they should be part of another module.
   - Adjust the module boundaries and resource definitions accordingly.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

