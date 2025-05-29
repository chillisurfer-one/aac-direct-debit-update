# IaC - Control Policy Deviation Report

**Analysis Date**: 2025-05-29 10:16:38

## 1. IaC Module and Control Policy Mapping

| Iac Module     | Control ID | Implementation Evidence |
|----------------|------------|-------------------------|
| ecs-fargate-module | INFRA-002-control | The aws_lb_listener resource is configured to use HTTPS protocol on port 443, ensuring secure communication. |
|  | INFRA-005-control | The aws_ecs_service resource includes a network_configuration block, which is a prerequisite for enabling CloudWatch logs, although explicit CloudWatch configuration is not shown. |
| observability-module | INFRA-005-control | The module includes resources for CloudWatch log group and metric alarm, which captures logs and custom metrics for observability. |
| rds-secrets-module | INFRA-003-control | The aws_db_instance resource has storage_encrypted set to true, ensuring audit logs are stored in encrypted RDS. |
|  | INFRA-004-control | The aws_secretsmanager_secret resource is used to store DB credentials, preventing plaintext secrets in configs. |
|  | SEC-003-control | The aws_secretsmanager_secret resource is used to store DB credentials, ensuring secrets are not hardcoded in code or config. |
| security-module | INFRA-006-control | Security group configurations allow 0.0.0.0/0 for egress, which is a HIGH severity issue according to tfsec results. |

## 2. Control Policy Deviation Analysis

| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |
|------------|------------|---------------------------|-----------|------------|
| ecs-fargate-module | INFRA-002-control | Complaint✅ | No deviations found | N/A |
| ecs-fargate-module | INFRA-005-control | Non-Compliant❌ | The Terraform code does not explicitly enable CloudWatch logs for the ECS service. | Add a log configuration to the ECS task definition to enable CloudWatch logs. |
| observability-module | INFRA-005-control | Non-Compliant❌ | The Terraform code does not explicitly enable CloudWatch logs for the resources defined in the input JSON configuration. | Ensure that all resources, such as 'aws_lambda_function' and 'aws_ecs_service', have CloudWatch logs enabled in the Terraform code. |
| rds-secrets-module | INFRA-003-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-004-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | SEC-003-control | Complaint✅ | No deviations found | N/A |
| security-module | INFRA-006-control | Non-Compliant❌ | Security group allows 0.0.0.0/0 for egress traffic. | Restrict egress traffic to specific IP ranges instead of 0.0.0.0/0. |
|  |  |  | Database encryption not enabled. | Enable encryption for the RDS database. |
