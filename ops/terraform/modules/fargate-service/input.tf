
variable "family_name" {
  type = string
}

variable "container_definition" {
  type = string
}

variable "task_role_arn" {
  type = string
}

variable "execution_role_arn" {
  type = string
}

variable "cpu" {
  type = number
}

variable "memory" {
  type = number
}

variable "task_definition_tags" {
  type = map(string)
  default = {}
}

variable "ecs_service_tags" {
  type = map(string)
  default = {}
}

variable "ecs_cluster_tags" {
  type = map(string)
  default = {}
}

variable "ecs_cluster_name" {
  type = string
  default = "ecs-cluster"
}

variable "ecs_service_name" {
  type = string
  default = "ecs-service"
}

variable "instance_count" {
  type = number
  default = 1
}

variable "subnets" {
  type = list(string)
}

variable "security_groups" {
  type = list(string)
}

variable "assign_public_ip" {
  type = bool
  default = true
}

variable "load_balancer" {
  type = object({
    target_group_arn = string
    container_name   = string
    container_port   = number
  })
  default = null
}
