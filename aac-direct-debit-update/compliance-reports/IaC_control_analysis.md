# IaC - Control Policy Deviation Report

**Analysis Date**: 2025-05-29 10:25:32

## 1. IaC Module and Control Policy Mapping

| Iac Module     | Control ID | Implementation Evidence |
|----------------|------------|-------------------------|
| ecs-fargate-module | INFRA-002-control | The aws_lb_listener resource is configured to use HTTPS protocol on port 443, ensuring secure communication. |
|  | INFRA-005-control | The aws_ecs_service resource includes a network_configuration block, which typically supports CloudWatch logging for ECS services, although explicit logging configuration is not shown. |
| observability-module | INFRA-005-control | The module includes resources for CloudWatch log group and metric alarm, which captures logs and custom metrics for observability. |
| rds-secrets-module | INFRA-003-control | The aws_db_instance resource has storage_encrypted set to true, ensuring audit logs are stored in encrypted RDS. |
|  | INFRA-004-control | The aws_secretsmanager_secret resource is used to store DB credentials, preventing plaintext secrets in configs. |
|  | SEC-003-control | The aws_secretsmanager_secret resource is used to store DB credentials, ensuring secrets are not hardcoded in code or config. |
| security-module | INFRA-006-control | The security group configurations allow 0.0.0.0/0 for egress, which is a common tfsec check for high severity issues. This indicates awareness of potential tfsec checks, although not explicitly passing them. |

## 2. Control Policy Deviation Analysis

| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |
|------------|------------|---------------------------|-----------|------------|
| ecs-fargate-module | INFRA-002-control | Complaint✅ | No deviations found | N/A |
| ecs-fargate-module | INFRA-005-control | Non-Compliant❌ | The Terraform code does not explicitly enable CloudWatch logs for the ECS service. | Add a log configuration to the ECS task definition to enable CloudWatch logs. |
| observability-module | INFRA-005-control | Non-Compliant❌ | The Terraform code does not explicitly enable CloudWatch logs for the resources defined. The policy requires all resources to have CloudWatch logs enabled. | Ensure that all resources in the Terraform code have CloudWatch logs enabled by adding necessary configurations or attributes. |
| rds-secrets-module | INFRA-003-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-004-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | SEC-003-control | Non-Compliant❌ | Hardcoded secret found: db.password=admin123 | Use AWS Secrets Manager to store and retrieve the database password instead of hardcoding it. |
| security-module | INFRA-006-control | Non-Compliant❌ | Security group 'alb' allows ingress from 0.0.0.0/0 which is identified as a HIGH severity issue. | Restrict ingress rules to specific IP ranges or security groups instead of 0.0.0.0/0. |
|  |  |  | Security group 'ecs' allows egress to 0.0.0.0/0 which is identified as a HIGH severity issue. | Restrict egress rules to specific IP ranges or security groups instead of 0.0.0.0/0. |
|  |  |  | Security group 'rds' allows egress to 0.0.0.0/0 which is identified as a HIGH severity issue. | Restrict egress rules to specific IP ranges or security groups instead of 0.0.0.0/0. |
|  |  |  | Database encryption not enabled, identified as a CRITICAL severity issue. | Enable encryption for database resources. |
