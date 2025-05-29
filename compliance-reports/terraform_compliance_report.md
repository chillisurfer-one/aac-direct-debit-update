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
| Components Present in Terraform Code Not in PUML Diagram | aws_cloudwatch_metric_alarm (high_cpu)                         |
| Connection Discrepancies                                 | MandateUpdateService and VaultCoreClient connections to CloudWatch are not explicitly defined in Terraform. |
| Label/Annotation Discrepancies                           | No explicit labels or annotations for CloudWatch connections in Terraform. |

#### Remediation Steps:

1. **[Define Connections]:**
   - Ensure that the connections from MandateUpdateService and VaultCoreClient to CloudWatch are explicitly defined in the Terraform code. This could involve setting up appropriate IAM roles and policies to allow these services to send logs and metrics to CloudWatch.

2. **[Update Documentation]:**
   - Add comments or documentation in the Terraform code to reflect the intended connections and usage of CloudWatch for observability, ensuring alignment with the architecture diagram.

3. **[Review Alarms]:**
   - Consider whether the `aws_cloudwatch_metric_alarm` for high CPU usage should be part of the observability module, and if so, ensure it is documented in the architecture diagram. If it is not relevant, consider moving it to a more appropriate module.
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
   - Verify that the MandateUpdateService has the necessary permissions and configurations to write audit logs to the RDS PostgreSQL database.

2. **Documentation and Code Alignment:**
   - Update Terraform code to include explicit IAM role and policy definitions for the MandateUpdateController's access to Secrets Manager.
   - Ensure that the Terraform code reflects any specific labels or annotations used in the architecture diagram for clarity and consistency.
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

2. **Implement Connection for VaultCoreClient:**
   - Ensure the Terraform code includes resources or configurations for establishing a secure connection (HTTPS + OAuth2) between VaultCoreClient (Adapter) and Thought Machine Vault Core API.
   - Consider using `aws_api_gateway_method` and `aws_api_gateway_integration` to define the connection details.

3. **Review Security Group Usage:**
   - Verify if the security groups defined in Terraform are necessary for the "security-module" or if they should be part of another module.
   - Adjust the module boundaries or definitions accordingly to ensure alignment with the architecture diagram.
---

## Compliant Modules

### ecs-fargate-module
✅ All diagram components and connections are correctly implemented in code.

