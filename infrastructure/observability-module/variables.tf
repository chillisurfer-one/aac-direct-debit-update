
variable "region" {
  description = "AWS region"
  type        = string
}

variable "name_prefix" {
  description = "Prefix for resource naming"
  type        = string
}

variable "ecs_cluster_name" {
  description = "ECS cluster name for metric dimensions"
  type        = string
}

variable "ecs_service_name" {
  description = "ECS service name for metric dimensions"
  type        = string
}

variable "log_retention_days" {
  description = "Log retention period in days"
  type        = number
  default     = 14
}

variable "cpu_threshold" {
  description = "CPU threshold for triggering alarm"
  type        = number
  default     = 80
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
}
