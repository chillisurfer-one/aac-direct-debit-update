# IaC - Control Policy Deviation Report

**Analysis Date**: 2025-05-30 09:34:59

## 1. IaC Module and Control Policy Mapping

| Iac Module     | Control ID | Implementation Evidence |
|----------------|------------|-------------------------|
| ecs-fargate-module | INFRA-002-control | The aws_lb_listener resource is configured to use HTTPS protocol on port 443, ensuring secure communication. |
|  | INFRA-005-control | The aws_ecs_service resource includes a network_configuration block, which is a prerequisite for enabling CloudWatch logs, although explicit CloudWatch log configuration is not shown in the code. |
| observability-module | INFRA-005-control | The module includes resources for CloudWatch log group and metric alarm, which captures logs and custom metrics for observability. |
| rds-secrets-module | INFRA-003-control | The RDS instance 'aws_db_instance.audit' has 'storage_encrypted' set to true, ensuring data at rest protection. |
|  | INFRA-004-control | The module uses 'aws_secretsmanager_secret' to store DB credentials, preventing plaintext secrets in configs. |
|  | SEC-003-control | The module uses AWS Secrets Manager to store sensitive credentials, ensuring secrets are not hardcoded. |
| security-module | INFRA-006-control | The security group configurations allow 0.0.0.0/0 for egress, which is a common tfsec check for high severity issues. This indicates awareness of potential tfsec checks, although not explicitly passing them. |

## 2. Control Policy Deviation Analysis

| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |
|------------|------------|---------------------------|-----------|------------|
| ecs-fargate-module | INFRA-002-control | Complaint✅ | No deviations found | N/A |
| ecs-fargate-module | INFRA-005-control | Non-Compliant❌ | Resource 'aws_ecs_service.app' does not have CloudWatch logs enabled. | Add configuration to enable CloudWatch logs for the ECS service. |
| observability-module | INFRA-005-control | Non-Compliant❌ | The Terraform code does not explicitly enable CloudWatch logs for the resources defined. The policy requires that all resources have CloudWatch logs enabled. | Ensure that all resources in the Terraform code have CloudWatch logs enabled by adding necessary configurations or verifying existing ones. |
| rds-secrets-module | INFRA-003-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-004-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | SEC-003-control | Non-Compliant❌ | Hardcoded secret found: db.password=admin123 | Use AWS Secrets Manager to store and retrieve the database password instead of hardcoding it. |
| security-module | INFRA-006-control | Non-Compliant❌ | Security group allows 0.0.0.0/0 for egress traffic. | Restrict egress traffic to specific IP ranges instead of 0.0.0.0/0. |
|  |  |  | Database encryption not enabled. | Enable encryption for the database. |
