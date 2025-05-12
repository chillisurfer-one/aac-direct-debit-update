
output "cluster_name" {
  value = aws_ecs_cluster.this.name
}

output "service_name" {
  value = aws_ecs_service.app.name
}

output "load_balancer_dns" {
  value = aws_lb.this.dns_name
}
