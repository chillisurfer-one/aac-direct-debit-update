
package policies.infrastructure

__doc__ := {
  "id": "INFRA-001",
  "title": "Fargate tasks must use latest approved image tag (e.g., :stable)",
  "description": "Ensure ECS tasks do not use mutable or unapproved image tags like :latest or :dev.",
  "enforcement": "hard"
}

violation[msg] {
  task := input.terraform.resources[_]
  task.type == "aws_ecs_task_definition"
  not approved_tag(task.image_tag)
  msg := sprintf("ECS task '%s' uses unapproved image tag: %s", [task.name, task.image_tag])
}

approved_tag(tag) {
  tag == "stable"
}
