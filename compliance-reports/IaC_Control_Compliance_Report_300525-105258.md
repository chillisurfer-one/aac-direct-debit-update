# IaC - Control Policy Deviation Report

**Analysis Date**: 2025-05-30 10:52:56

## 1. IaC Module and Control Policy Mapping

| Iac Module     | Control ID | Implementation Evidence |
|----------------|------------|-------------------------|
| ecs-fargate-module | INFRA-002-control | The aws_lb_listener resource is configured to use HTTPS protocol on port 443, ensuring secure communication. |
|  | INFRA-005-control | The aws_ecs_service resource includes a network_configuration block, which is a prerequisite for enabling CloudWatch logging, although explicit CloudWatch configuration is not shown. |
| observability-module | INFRA-005-control | The module includes resources for CloudWatch log group and metric alarm, which captures logs and custom metrics for observability. |
| rds-secrets-module | INFRA-003-control | The RDS instance 'aws_db_instance.audit' has 'storage_encrypted = true', ensuring audit logs are stored in encrypted RDS. |
|  | INFRA-004-control | The module uses 'aws_secretsmanager_secret' to store DB credentials, ensuring sensitive credentials are not stored in plain text. |
|  | SEC-003-control | The module uses AWS Secrets Manager to store database credentials, preventing hardcoded secrets in the code. |
| security-module | INFRA-006-control | The security group configurations allow 0.0.0.0/0 for egress, which is a common tfsec check for high severity issues. This indicates awareness of potential tfsec checks, although not explicitly passing them. |

## 2. Control Policy Deviation Analysis

| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |
|------------|------------|---------------------------|-----------|------------|
| ecs-fargate-module | INFRA-002-control | Complaint✅ | No deviations found | N/A |
| ecs-fargate-module | INFRA-005-control | Non-Compliant❌ | Resource 'aws_ecs_service.app' does not have CloudWatch logs enabled. | Add configuration to enable CloudWatch logs for the ECS service. |
| observability-module | INFRA-005-control | Non-Compliant❌ | The 'aws_lambda_function' resource 'audit-function' does not have CloudWatch logs enabled. | Ensure that CloudWatch logs are enabled for the 'aws_lambda_function' resource 'audit-function'. |
| rds-secrets-module | INFRA-003-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-004-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | SEC-003-control | Non-Compliant❌ | Hardcoded secret found: db.password=admin123 | Use AWS Secrets Manager to store and retrieve the database password instead of hardcoding it. |
| security-module | INFRA-006-control | Non-Compliant❌ | Security group 'alb' allows ingress from 0.0.0.0/0 on port 80, which is flagged as HIGH severity by tfsec. | Restrict ingress to specific IP ranges or use security groups for controlled access. |
|  |  |  | Security group 'ecs' allows egress to 0.0.0.0/0, which is flagged as HIGH severity by tfsec. | Restrict egress to specific IP ranges or use security groups for controlled access. |
|  |  |  | Security group 'rds' allows egress to 0.0.0.0/0, which is flagged as HIGH severity by tfsec. | Restrict egress to specific IP ranges or use security groups for controlled access. |
|  |  |  | Database encryption not enabled, which is flagged as CRITICAL severity by tfsec. | Enable encryption for RDS instances. |
