
provider "aws" {
  region = var.region
}

resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/ecs/${var.name_prefix}/application"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.name_prefix}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 60
  statistic           = "Average"
  threshold           = var.cpu_threshold
  dimensions = {
    ClusterName = var.ecs_cluster_name
    ServiceName = var.ecs_service_name
  }
  alarm_description = "Alarm for high CPU on ECS service"
  tags              = var.tags
}
