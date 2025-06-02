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

1. **[Connection Implementation]:**
   - Define explicit IAM roles and policies in Terraform to allow MandateUpdateService and VaultCoreClient to send logs and metrics to CloudWatch.
   - Ensure ECS services are configured to use these IAM roles for logging and monitoring.

2. **[Resource Alignment]:**
   - Ensure that the aws_cloudwatch_log_group and aws_cloudwatch_metric_alarm resources are correctly associated with the ECS services mentioned in the diagram.
   - Verify that the log group and metric alarm are configured to capture the necessary logs and metrics from the services.
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

1. **Connection Definition:**
   - Ensure IAM roles and policies are defined to allow MandateUpdateController to read secrets from Secrets Manager.
   - Verify that the MandateUpdateService has the necessary permissions and configurations to write to the Audit Log (Amazon RDS PostgreSQL).

2. **Documentation and Code Alignment:**
   - Update Terraform code to include explicit IAM role and policy definitions for the MandateUpdateController's access to Secrets Manager.
   - Review and document the connection between MandateUpdateService and Audit Log in Terraform code to ensure it matches the diagram.
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
   - Ensure the API Gateway is configured to route requests to the MandateUpdateController (Spring Boot) component.

2. **Implement Connection:**
   - Establish the connection between the Amazon API Gateway and the MandateUpdateController using appropriate Terraform resources such as `aws_api_gateway_integration` and `aws_api_gateway_method`.
   - Ensure the connection uses HTTPS as specified in the architecture diagram.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

