package policies.infrastructure

# INFRA-001: Fargate tasks must use :stable tag

__doc__ := {
  "id": "INFRA-001",
  "title": "Use stable image tag in ECS",
  "description": "Prevent use of latest or dev tags in ECS deployments.",
  "enforcement": "hard"
}

violation[msg] {
  task := input.terraform.resources[_]
  task.type == "aws_ecs_task_definition"
  task.image_tag != "stable"
  msg := sprintf("ECS task %s does not use stable image tag", [task.name])
}
