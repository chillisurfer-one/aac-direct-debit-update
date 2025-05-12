
variable "region" {
  description = "AWS region"
  type        = string
}

variable "name_prefix" {
  description = "Prefix for naming all resources"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "db_sg_id" {
  description = "Security group ID for RDS"
  type        = string
}

variable "db_username" {
  description = "RDS database master username"
  type        = string
}

variable "db_password" {
  description = "RDS database master password"
  type        = string
  sensitive   = true
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "storage" {
  description = "RDS allocated storage in GB"
  type        = number
  default     = 20
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
}
