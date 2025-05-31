# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-05-31  
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
| Components Present in Terraform Code Not in PUML Diagram | aws_lb, aws_lb_target_group, aws_lb_listener, aws_ecs_cluster, aws_ecs_service, aws_ecs_task_definition, aws_iam_role, aws_iam_role_policy_attachment |
| Connection Discrepancies                                 | MandateUpdateController -> MandateUpdateService and MandateUpdateService -> VaultCoreClient connections are not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | No explicit labels or annotations for connections in Terraform code. |

#### Remediation Steps:

1. **[Connection Implementation]:**
   - Define explicit connections between MandateUpdateController and MandateUpdateService in the Terraform code, possibly using environment variables or service discovery.
   - Define explicit connections between MandateUpdateService and VaultCoreClient in the Terraform code, ensuring proper network configuration and access permissions.

2. **[Label/Annotation Consistency]:**
   - Add comments or annotations in the Terraform code to reflect the connections and roles of each component as described in the architecture diagram.
---

### observability-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | CloudWatch                                                     |
| Components Present in PUML Diagram Not in Terraform Code | None                                                           |
| Components Present in Terraform Code Not in PUML Diagram | aws_cloudwatch_metric_alarm                                    |
| Connection Discrepancies                                 | MandateUpdateService -> CloudWatch: Logs, Metrics not explicitly defined in Terraform code. VaultCoreClient -> CloudWatch: Retry Logs not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | None                                                           |

#### Remediation Steps:

1. **[Connection Implementation]:**
   - Define resources or configurations in Terraform to explicitly capture logs and metrics from MandateUpdateService to CloudWatch.
   - Define resources or configurations in Terraform to explicitly capture retry logs from VaultCoreClient to CloudWatch.

2. **[Resource Alignment]:**
   - Ensure that the aws_cloudwatch_metric_alarm resource is appropriately linked to the components in the architecture diagram, if applicable.
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
   - Verify that the MandateUpdateService has the necessary permissions and configurations to write to the Audit Log (Amazon RDS PostgreSQL).

2. **[Subnet and Security Configuration]:**
   - Confirm that the aws_db_subnet_group.this is correctly configured to ensure the RDS instance is in private subnets.
   - Validate security group settings to ensure proper access control for the RDS instance.
---

### security-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | None                                                            |
| Components Present in PUML Diagram Not in Terraform Code | Amazon API Gateway                                              |
| Components Present in Terraform Code Not in PUML Diagram | aws_security_group.ecs, aws_security_group.alb, aws_security_group.rds |
| Connection Discrepancies                                 | Amazon API Gateway -> MandateUpdateController (Spring Boot): HTTPS Route is not implemented in Terraform code |
| Label/Annotation Discrepancies                           | No explicit labels or annotations for Amazon API Gateway in Terraform code |

#### Remediation Steps:

1. **[Amazon API Gateway]:**
   - Add a Terraform resource for Amazon API Gateway to the `security-module`.
   - Ensure the API Gateway is configured to route HTTPS requests to the MandateUpdateController (Spring Boot).

2. **[Connection Implementation]:**
   - Implement the connection from Amazon API Gateway to MandateUpdateController in the Terraform code, ensuring it matches the diagram's specification.

3. **[Security Group Review]:**
   - Review the security groups defined in the Terraform code to ensure they align with the architectural requirements and best practices, even if not explicitly mentioned in the diagram.
---

