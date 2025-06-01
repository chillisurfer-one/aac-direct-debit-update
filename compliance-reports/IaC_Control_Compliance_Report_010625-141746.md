# IaC - Control Policy Deviation Report

**Analysis Date**: 2025-06-01 14:17:44

## 1. IaC Module and Control Policy Mapping

| Iac Module     | Control ID | Implementation Evidence |
|----------------|------------|-------------------------|
| ecs-fargate-module | INFRA-002-control | The aws_lb_listener resource uses HTTPS protocol for secure communication. |
|  | INFRA-005-control | The aws_ecs_service resource is configured with CloudWatch logs enabled, as indicated by the network_configuration and load_balancer settings. |
| observability-module | INFRA-005-control | The module includes resources for CloudWatch log group and metric alarm, which captures logs and custom metrics for observability. |
| rds-secrets-module | INFRA-003-control | The aws_db_instance resource has storage_encrypted set to true, ensuring that audit logs are stored in encrypted RDS. |
|  | INFRA-004-control | The module uses aws_secretsmanager_secret to store DB credentials, ensuring sensitive credentials are not stored in plain text. |
|  | SEC-003-control | The module uses AWS Secrets Manager to store database credentials, preventing hardcoded secrets in the code. |
| security-module | INFRA-006-control | The Terraform code includes security group configurations that allow 0.0.0.0/0, which is a HIGH severity issue identified by tfsec. |

## 2. Control Policy Deviation Analysis

| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |
|------------|------------|---------------------------|-----------|------------|
| ecs-fargate-module | INFRA-002-control | Complaint✅ | No deviations found | N/A |
| ecs-fargate-module | INFRA-005-control | Non-Compliant❌ | The Terraform code does not explicitly enable CloudWatch logs for the ECS service. | Add a log configuration to the ECS task definition to enable CloudWatch logs. |
| observability-module | INFRA-005-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-003-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-004-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | SEC-003-control | Complaint✅ | No deviations found | N/A |
| security-module | INFRA-006-control | Non-Compliant❌ | Security group allows 0.0.0.0/0 for egress traffic. | Restrict egress traffic to specific IP ranges instead of 0.0.0.0/0. |
|  |  |  | Database encryption not enabled. | Enable encryption for the database. |
