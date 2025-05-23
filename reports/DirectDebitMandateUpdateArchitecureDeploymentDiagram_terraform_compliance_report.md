# Terraform Architecture Compliance Report

**Architecture Diagram**: `DirectDebitMandateUpdateArchitecureDeploymentDiagram.puml`  
**Date**: 2025-05-22  
## Executive Summary

This report evaluates the compliance of Terraform modules against the architecture diagram. Of the 4 modules evaluated, 1 is compliant and 3 require remediation.

## Module to Component Mapping

The following table shows which components from the architecture diagram are mapped to each module:

| Module Name | Components |
|-------------|------------|
| ecs-fargate-module | ECS Fargate Task, MandateUpdateController (Spring Boot) |
| observability-module | CloudWatch Logs, Service Logs |
| rds-secrets-module | Secrets Manager, DB/API Credentials, RDS PostgreSQL, AuditLogDB |
| security-module | AWS VPC (10.0.0.0/16), Public Subnet (10.0.1.0/24), Application Load Balancer, HTTP Listener (Port 80), Private Subnet (10.0.11.0/24) |

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
| Components Present in PUML Diagram and Terraform Code    | CloudWatch Logs, Service Logs                                  |
| Components Present in PUML Diagram Not in Terraform Code | Service Logs                                                   |
| Components Present in Terraform Code Not in PUML Diagram | aws_cloudwatch_metric_alarm.high_cpu                           |
| Connection Discrepancies                                 | MandateUpdateController -> Service Logs connection not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | No explicit labels or annotations for log encryption in Terraform code. |

#### Remediation Steps:

1. **Service Logs Implementation:**
   - Ensure the "Service Logs" component is explicitly defined in the Terraform code, possibly as a separate log group or resource.
   - Verify that the logs are encrypted as per the compliance note in the diagram.

2. **Connection Definition:**
   - Define the connection from MandateUpdateController to Service Logs in the Terraform code, ensuring that logs are correctly routed and stored.

3. **Label/Annotation for Encryption:**
   - Add annotations or configurations in the Terraform code to ensure logs are encrypted, reflecting the compliance note in the diagram.
---

### rds-secrets-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | Secrets Manager, RDS PostgreSQL, AuditLogDB                    |
| Components Present in PUML Diagram Not in Terraform Code | DB/API Credentials                                             |
| Components Present in Terraform Code Not in PUML Diagram | aws_db_subnet_group                                            |
| Connection Discrepancies                                 | MandateUpdateController -> DB/API Credentials connection is not explicitly defined in Terraform code. |
| Label/Annotation Discrepancies                           | No explicit labels or annotations discrepancies found.         |

#### Remediation Steps:

1. **DB/API Credentials:**
   - Ensure that the `DB/API Credentials` component is explicitly defined in the Terraform code. This could involve ensuring that the `aws_secretsmanager_secret` and `aws_secretsmanager_secret_version` resources are correctly configured to represent this component.

2. **Connection Implementation:**
   - Define the connection between `MandateUpdateController` and `DB/API Credentials` in the Terraform code. This could involve ensuring that the application code or infrastructure configuration explicitly retrieves credentials from AWS Secrets Manager.

3. **Documentation and Annotations:**
   - Update documentation or comments in the Terraform code to reflect the architectural intent and ensure that all components and connections are clearly annotated.
---

### security-module

| Category                                              | Details                                                         |
|----------------------------------------------------------|----------------------------------------------------------------|
| Components Present in PUML Diagram and Terraform Code    | Application Load Balancer, HTTP Listener (Port 80)             |
| Components Present in PUML Diagram Not in Terraform Code | AWS VPC (10.0.0.0/16), Public Subnet (10.0.1.0/24), Private Subnet (10.0.11.0/24) |
| Components Present in Terraform Code Not in PUML Diagram | aws_security_group.ecs, aws_security_group.alb, aws_security_group.rds |
| Connection Discrepancies                                 | No explicit connections for subnets or VPC in Terraform code   |
| Label/Annotation Discrepancies                           | No labels or annotations in Terraform code for security groups |

#### Remediation Steps:

1. **[VPC and Subnets]:**
   - Define the AWS VPC (10.0.0.0/16) in the Terraform code.
   - Define the Public Subnet (10.0.1.0/24) and Private Subnet (10.0.11.0/24) in the Terraform code.

2. **[Connections]:**
   - Ensure that the connections between the ALB and ECS, and ECS to RDS are explicitly defined in the Terraform code, possibly through route tables or subnet associations.

3. **[Labels/Annotations]:**
   - Add labels or annotations in the Terraform code to reflect the descriptions and purposes of the security groups, similar to the diagram.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

