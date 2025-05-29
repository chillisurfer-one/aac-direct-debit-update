# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-05-29  
## Executive Summary

This report evaluates the compliance of Terraform modules against the architecture diagram. Of the 4 modules evaluated, 0 are compliant and 4 require remediation.

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
| ecs-fargate-module | ❌ NON-COMPLIANT | Yes |
| observability-module | ❌ NON-COMPLIANT | Yes |
| rds-secrets-module | ❌ NON-COMPLIANT | Yes |
| security-module | ❌ NON-COMPLIANT | Yes |

## Non-Compliant Modules and Remediation Steps

### ecs-fargate-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | MandateUpdateController, MandateUpdateService, VaultCoreClient  |
| Components Present in PUML Diagram Not in Terraform Code | None                                                            |
| Components Present in Terraform Code Not in PUML Diagram | aws_lb, aws_lb_target_group, aws_lb_listener, aws_ecs_cluster, aws_ecs_service, aws_iam_role, aws_iam_role_policy_attachment, aws_ecs_task_definition |
| Connection Discrepancies                                 | MandateUpdateController -> MandateUpdateService and MandateUpdateService -> VaultCoreClient connections are not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                            |

#### Remediation Steps:

1. **[Connection Implementation]:**
   - Define explicit connections between MandateUpdateController and MandateUpdateService, and between MandateUpdateService and VaultCoreClient in the Terraform code, possibly through environment variables or service discovery mechanisms.

2. **[Resource Alignment]:**
   - Ensure that the resources such as load balancer, target group, and listener are appropriately documented or referenced in the architecture diagram to reflect their role in the module.
---

### observability-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | CloudWatch                                                     |
| Components Present in PUML Diagram Not in Terraform Code | None                                                           |
| Components Present in Terraform Code Not in PUML Diagram | aws_cloudwatch_metric_alarm                                    |
| Connection Discrepancies                                 | MandateUpdateService and VaultCoreClient connections to CloudWatch are not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                           |

#### Remediation Steps:

1. **[Connection Implementation]:**
   - Define explicit IAM roles and policies in Terraform to allow MandateUpdateService and VaultCoreClient to send logs and metrics to CloudWatch.
   - Ensure that the ECS services are configured to use these IAM roles for logging and monitoring.

2. **[Resource Alignment]:**
   - Review the necessity of `aws_cloudwatch_metric_alarm` in the context of the observability module and ensure it aligns with the architectural intent. If it is relevant, update the architecture diagram to reflect its presence.
---

### rds-secrets-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | Secrets Manager, Audit Log (Amazon RDS PostgreSQL)             |
| Components Present in PUML Diagram Not in Terraform Code | None                                                           |
| Components Present in Terraform Code Not in PUML Diagram | aws_db_subnet_group                                            |
| Connection Discrepancies                                 | MandateUpdateController -> Secrets Manager connection not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                           |

#### Remediation Steps:

1. **[Connection Discrepancies]:**
   - Ensure that the IAM role or policy allowing `MandateUpdateController` to read secrets from Secrets Manager is defined in the Terraform code.
   - Verify that the necessary permissions are granted to the ECS Fargate task role to access the Secrets Manager.

2. **[Components Present in Terraform Code Not in PUML Diagram]:**
   - Consider adding the `aws_db_subnet_group` to the architecture diagram if it is a significant part of the architecture, or ensure it is documented elsewhere if it is an implementation detail.
---

### security-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | None                                                            |
| Components Present in PUML Diagram Not in Terraform Code | Amazon API Gateway                                              |
| Components Present in Terraform Code Not in PUML Diagram | aws_security_group.ecs, aws_security_group.alb, aws_security_group.rds |
| Connection Discrepancies                                 | Amazon API Gateway -> MandateUpdateController (Spring Boot): HTTP Route is not implemented in Terraform code |
| Label/Annotation Discrepancies                           | No explicit labels or annotations for Amazon API Gateway in Terraform code |

#### Remediation Steps:

1. **[Amazon API Gateway Implementation]:**
   - Add a resource definition for Amazon API Gateway in the Terraform code.
   - Ensure the API Gateway is configured to route HTTP requests to the MandateUpdateController.

2. **[Connection Implementation]:**
   - Implement the connection from Amazon API Gateway to MandateUpdateController (Spring Boot) in the Terraform code.
   - Ensure the connection is secured and follows best practices for API Gateway integrations.

3. **[Security Group Review]:**
   - Review the existing security groups to ensure they align with the architecture diagram and security best practices.
   - Consider adding annotations or comments in the Terraform code to clarify the purpose of each security group in relation to the architecture diagram.
---

