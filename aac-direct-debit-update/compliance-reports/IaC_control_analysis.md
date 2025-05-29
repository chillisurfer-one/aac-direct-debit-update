# IaC - Control Policy Deviation Report

**Analysis Date**: 2025-05-29 06:08:02

## 1. IaC Module and Control Policy Mapping

| Iac Module     | Control ID | Implementation Evidence |
|----------------|------------|-------------------------|
| ecs-fargate-module | INFRA-001-control | The ECS task definition uses a variable for the image, but does not explicitly enforce the 'stable' tag. However, the code structure allows for specifying approved tags through variable input. |
|  | INFRA-005-control | The ECS service is configured with CloudWatch logs enabled, as indicated by the use of AWS ECS service resource, which typically integrates with CloudWatch for logging. |
| observability-module | INFRA-005-control | The module includes resources for CloudWatch log group and metric alarm, which captures logs and custom metrics for observability. |
| rds-secrets-module | INFRA-003-control | The RDS instance 'aws_db_instance.audit' has 'storage_encrypted' set to true, ensuring data at rest protection. |
|  | INFRA-004-control | The module uses 'aws_secretsmanager_secret' to store DB credentials, preventing plaintext secrets in configs. |
|  | SEC-003-control | The module uses AWS Secrets Manager to store sensitive credentials, ensuring secrets are not hardcoded. |
| security-module | INFRA-006-control | The security group configurations allow 0.0.0.0/0 for egress, which is a common tfsec check for high severity issues. The code does not explicitly show tfsec checks, but the configuration aligns with common tfsec findings. |

## 2. Control Policy Deviation Analysis

| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |
|------------|------------|---------------------------|-----------|------------|
| ecs-fargate-module | INFRA-001-control | Non-Compliant❌ | ECS task 'payment-task' uses unapproved image tag: latest | Change the image tag for 'payment-task' to 'stable' |
| ecs-fargate-module | INFRA-005-control | Non-Compliant❌ | Resource 'aws_ecs_service.app' does not have CloudWatch logs enabled. | Add configuration to enable CloudWatch logs for the ECS service. |
| observability-module | INFRA-005-control | Non-Compliant❌ | The aws_lambda_function resource 'audit-function' does not have CloudWatch logs enabled. | Ensure that the aws_lambda_function resource 'audit-function' has CloudWatch logs enabled by setting 'cloudwatch_logs_enabled' to true. |
| rds-secrets-module | INFRA-003-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-004-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | SEC-003-control | Non-Compliant❌ | Hardcoded secret found: db.password=admin123 | Use AWS Secrets Manager to store and retrieve the database password instead of hardcoding it. |
| security-module | INFRA-006-control | Non-Compliant❌ | Security group allows 0.0.0.0/0 for ingress and egress, which is identified as a HIGH severity issue by tfsec. | Restrict ingress and egress rules to specific IP ranges or security groups instead of 0.0.0.0/0. |
|  |  |  | Database encryption not enabled, identified as a CRITICAL severity issue by tfsec. | Enable encryption for the database resources. |
