# IaC - Control Policy Deviation Report

**Analysis Date**: 2025-05-31 15:29:07

## 1. IaC Module and Control Policy Mapping

| Iac Module     | Control ID | Implementation Evidence |
|----------------|------------|-------------------------|
| ecs-fargate-module | INFRA-002-control | The aws_lb_listener resource uses HTTPS protocol for secure communication. |
|  | INFRA-005-control | The aws_ecs_service resource is configured to use CloudWatch logs, as indicated by the presence of the 'cloudwatch_logs_enabled' attribute in the JSON configuration. |
| observability-module | INFRA-005-control | The module includes resources for CloudWatch log groups and metric alarms, which aligns with the requirement to capture logs and custom metrics for observability. |
| rds-secrets-module | INFRA-003-control | The aws_db_instance resource has storage_encrypted set to true, ensuring audit logs are stored in encrypted RDS. |
|  | INFRA-004-control | The module uses aws_secretsmanager_secret to store DB credentials, preventing plaintext secrets in configs. |
|  | SEC-003-control | The module uses AWS Secrets Manager to store database credentials, ensuring secrets are not hardcoded. |
| security-module | INFRA-006-control | The security group configuration allows 0.0.0.0/0 for egress, which is a common tfsec check for high severity issues. The code should be reviewed to ensure compliance with tfsec checks. |

## 2. Control Policy Deviation Analysis

| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |
|------------|------------|---------------------------|-----------|------------|
| ecs-fargate-module | INFRA-002-control | Complaint✅ | No deviations found | N/A |
| ecs-fargate-module | INFRA-005-control | Non-Compliant❌ | Resource 'aws_ecs_service.app' does not have CloudWatch logs enabled. | Add configuration to enable CloudWatch logs for the ECS service. |
| observability-module | INFRA-005-control | Non-Compliant❌ | The Terraform code does not explicitly enable CloudWatch logs for the resources defined. The policy requires that all resources have CloudWatch logs enabled. | Ensure that all resources in the Terraform code have CloudWatch logs enabled by adding necessary configurations or attributes. |
| rds-secrets-module | INFRA-003-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-004-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | SEC-003-control | Complaint✅ | No deviations found | N/A |
| security-module | INFRA-006-control | Non-Compliant❌ | Security group allows 0.0.0.0/0 for egress traffic. | Restrict egress traffic to specific IP ranges instead of 0.0.0.0/0. |
|  |  |  | Database encryption not enabled. | Enable encryption for the database. |
