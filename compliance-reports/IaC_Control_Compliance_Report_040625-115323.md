# IaC - Control Policy Deviation Report

**Analysis Date**: 2025-06-04 11:53:20

## 1. IaC Module and Control Policy Mapping

| Iac Module     | Control ID | Implementation Evidence |
|----------------|------------|-------------------------|
| ecs-fargate-module | INFRA-002-control | The aws_lb_listener resource uses HTTPS protocol for secure communication. |
|  | INFRA-005-control | The aws_ecs_service resource is configured to use CloudWatch logs, as indicated by the presence of the 'cloudwatch_logs_enabled' attribute in the JSON configuration. |
| observability-module | INFRA-005-control | The module includes resources for CloudWatch log group and metric alarm, which captures logs and custom metrics for observability. |
| rds-secrets-module | INFRA-003-control | The aws_db_instance resource has storage_encrypted set to true, ensuring audit logs are stored in encrypted RDS. |
|  | INFRA-004-control | The aws_secretsmanager_secret resource is used to store DB credentials, preventing plaintext secrets in configs. |
|  | SEC-003-control | The module uses AWS Secrets Manager to store database credentials, ensuring secrets are not hardcoded. |
| security-module | INFRA-006-control | The security group configurations allow 0.0.0.0/0 for egress, which is flagged by tfsec as a HIGH severity issue. This indicates awareness of tfsec checks, although the code does not explicitly resolve the issue. |

## 2. Control Policy Deviation Analysis

| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |
|------------|------------|---------------------------|-----------|------------|
| ecs-fargate-module | INFRA-002-control | Complaint✅ | No deviations found | N/A |
| ecs-fargate-module | INFRA-005-control | Non-Compliant❌ | Resource 'aws_ecs_service.app' does not have CloudWatch logs enabled. | Add configuration to enable CloudWatch logs for the ECS service. |
| observability-module | INFRA-005-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-003-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | INFRA-004-control | Complaint✅ | No deviations found | N/A |
| rds-secrets-module | SEC-003-control | Complaint✅ | No deviations found | N/A |
| security-module | INFRA-006-control | Non-Compliant❌ | Security group 'alb' allows ingress from 0.0.0.0/0 which is flagged as HIGH severity by tfsec. | Restrict ingress to specific IP ranges or security groups instead of 0.0.0.0/0. |
|  |  |  | Security group 'ecs' allows egress to 0.0.0.0/0 which is flagged as HIGH severity by tfsec. | Restrict egress to specific IP ranges or security groups instead of 0.0.0.0/0. |
|  |  |  | Security group 'rds' allows egress to 0.0.0.0/0 which is flagged as HIGH severity by tfsec. | Restrict egress to specific IP ranges or security groups instead of 0.0.0.0/0. |
