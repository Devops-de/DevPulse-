# Terraform Infrastructure as Code for DevPulse
# Configured for AWS Cloud-Native Deployment

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Target AWS Region"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Deployment environment"
}

# ECS Cluster definition for containerized backend
resource "aws_ecs_cluster" "devpulse_cluster" {
  name = "devpulse-${var.environment}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Project     = "DevPulse"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# CloudWatch Log Group for structured telemetry
resource "aws_cloudwatch_log_group" "devpulse_logs" {
  name              = "/ecs/devpulse-${var.environment}"
  retention_in_days = 30

  tags = {
    Project     = "DevPulse"
    Environment = var.environment
  }
}

# CloudWatch Metric Alarm for High CPU Saturation
resource "aws_cloudwatch_metric_alarm" "high_cpu_alarm" {
  alarm_name          = "devpulse-${var.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 60
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "Triggered when DevPulse container CPU exceeds 80%"

  dimensions = {
    ClusterName = aws_ecs_cluster.devpulse_cluster.name
  }
}
