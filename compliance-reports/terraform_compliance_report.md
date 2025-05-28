# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-05-28  
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
| Components Present in PUML Diagram and Terraform Code    | MandateUpdateController, MandateUpdateService, VaultCoreClient |
| Components Present in PUML Diagram Not in Terraform Code | None                                                           |
| Components Present in Terraform Code Not in PUML Diagram | aws_lb, aws_lb_target_group, aws_lb_listener                   |
| Connection Discrepancies                                 | MandateUpdateController -> MandateUpdateService and MandateUpdateService -> VaultCoreClient connections are not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | No explicit labels or annotations for connections in Terraform code. |

#### Remediation Steps:

1. **Define Connections:**
   - Implement explicit definitions for the connections between MandateUpdateController and MandateUpdateService, and between MandateUpdateService and VaultCoreClient in the Terraform code. This could involve defining IAM roles and policies that allow these components to communicate securely.

2. **Label/Annotation Enhancements:**
   - Add comments or labels in the Terraform code to reflect the connections and roles of each component, ensuring clarity and alignment with the architecture diagram.
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
   - Review the necessity of `aws_cloudwatch_metric_alarm` in the context of the observability module and ensure it aligns with the intended architecture. If it is relevant, update the architecture diagram to reflect its presence.
---

### rds-secrets-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | Secrets Manager, Audit Log (Amazon RDS PostgreSQL)              |
| Components Present in PUML Diagram Not in Terraform Code | None                                                            |
| Components Present in Terraform Code Not in PUML Diagram | aws_db_subnet_group.this, aws_secretsmanager_secret_version.db_creds_version |
| Connection Discrepancies                                 | MandateUpdateController -> Secrets Manager connection not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                            |

#### Remediation Steps:

1. **[Connection Definition]:**
   - Ensure IAM roles and policies are defined to allow MandateUpdateController to read secrets from Secrets Manager.
   - Verify that the MandateUpdateService has the necessary permissions and configurations to write to the Audit Log (Amazon RDS PostgreSQL).

2. **[Resource Alignment]:**
   - Review the necessity of `aws_db_subnet_group.this` and `aws_secretsmanager_secret_version.db_creds_version` in the context of the architecture diagram and ensure they are accurately represented or justified in the diagram.
---

### security-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | None                                                            |
| Components Present in PUML Diagram Not in Terraform Code | Amazon API Gateway                                              |
| Components Present in Terraform Code Not in PUML Diagram | aws_security_group.ecs, aws_security_group.alb, aws_security_group.rds |
| Connection Discrepancies                                 | Amazon API Gateway -> MandateUpdateController (Spring Boot): HTTP Route not implemented in Terraform code |
| Label/Annotation Discrepancies                           | None                                                            |

#### Remediation Steps:

1. **[Amazon API Gateway Configuration]:**
   - Add a resource block in Terraform for `aws_api_gateway_rest_api` to define the API Gateway.
   - Ensure the API Gateway is configured to route HTTP requests to the MandateUpdateController.

2. **[Connection Implementation]:**
   - Implement the connection from Amazon API Gateway to MandateUpdateController using `aws_api_gateway_integration` to define the HTTP route.

3. **[Security Group Review]:**
   - Review the security groups defined in Terraform to ensure they align with the architecture diagram and intended security posture.
   - Consider adding security group rules for API Gateway if necessary.
---

