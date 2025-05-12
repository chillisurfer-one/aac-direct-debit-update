
variable "region" {
  description = "AWS region"
  type        = string
}

variable "name_prefix" {
  description = "Prefix to use for all resource names"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "alb_sg_id" {
  description = "Security group ID for ALB"
  type        = string
}

variable "ecs_sg_id" {
  description = "Security group ID for ECS tasks"
  type        = string
}

variable "image" {
  description = "Docker image URI for the container"
  type        = string
}

variable "cpu" {
  description = "CPU units for the ECS task"
  type        = string
  default     = "256"
}

variable "memory" {
  description = "Memory for the ECS task"
  type        = string
  default     = "512"
}

variable "desired_count" {
  description = "Number of ECS task instances"
  type        = number
  default     = 1
}

variable "environment" {
  description = "Environment variables for container"
  type        = list(object({
    name  = string
    value = string
  }))
  default = []
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
}
