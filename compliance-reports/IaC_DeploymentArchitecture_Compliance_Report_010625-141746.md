# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-06-01  
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
| Components Present in PUML Diagram and Terraform Code    | None                                                            |
| Components Present in PUML Diagram Not in Terraform Code | MandateUpdateController, MandateUpdateService, VaultCoreClient  |
| Components Present in Terraform Code Not in PUML Diagram | aws_ecs_cluster.this, aws_iam_role.ecs_task_execution, aws_iam_role_policy_attachment.ecs_exec_attach, aws_ecs_task_definition.app, aws_lb.this, aws_lb_target_group.this, aws_lb_listener.http, aws_ecs_service.app |
| Connection Discrepancies                                 | MandateUpdateController -> MandateUpdateService, MandateUpdateService -> VaultCoreClient connections are not explicitly defined in the Terraform code. |
| Label/Annotation Discrepancies                           | No explicit labels or annotations from the diagram are reflected in the Terraform code. |

#### Remediation Steps:

1. **[Component Definition]:**
   - Define ECS task definitions for MandateUpdateController, MandateUpdateService, and VaultCoreClient in the Terraform code.
   - Ensure each component has its own container definition within the ECS task.

2. **[Connection Implementation]:**
   - Implement the connection between MandateUpdateController and MandateUpdateService by ensuring the service logic is encapsulated within the ECS task.
   - Implement the connection between MandateUpdateService and VaultCoreClient by configuring the necessary network and IAM permissions.

3. **[Label/Annotation Consistency]:**
   - Add labels or tags in the Terraform code to reflect the roles of each component as described in the diagram (e.g., "Spring Boot", "Spring Logic", "Adapter").
---

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
   - Ensure that the connections from MandateUpdateService and VaultCoreClient to CloudWatch are explicitly defined in the Terraform code. This could involve adding resources or configurations that capture logs and metrics from these services to CloudWatch.

2. **[Align Code with Diagram]:**
   - Review the architecture diagram and Terraform code to ensure that all components and connections are accurately represented. Consider adding comments or documentation in the Terraform code to clarify the intended connections and their purpose.
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

2. **[Security Enhancements]:**
   - Confirm that the RDS instance is deployed in private subnets and that a NAT gateway is configured for outbound internet access if needed.
   - Review security group rules to ensure that only necessary traffic is allowed to the RDS instance.
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

1. **Amazon API Gateway Implementation:**
   - Add a resource definition for Amazon API Gateway in the Terraform code.
   - Ensure the API Gateway is configured to route HTTPS requests to the MandateUpdateController.

2. **Connection Implementation:**
   - Define the connection between Amazon API Gateway and MandateUpdateController in the Terraform code, ensuring it uses HTTPS.

3. **Review Security Group Usage:**
   - Verify if the security groups defined in Terraform are necessary for the "security-module" or if they should be part of another module.
---

