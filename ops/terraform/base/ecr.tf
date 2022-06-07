
locals {
  api_server_registry_name = "jaspr-api-server"
  worker_registry_name = "jaspr-worker"
  scheduler_registry_name = "jaspr-scheduler"
}

module "api_server_registry" {
  source = "../modules/elastic-container-registry"
  registry_name = local.api_server_registry_name
}

module "worker_registry" {
  source = "../modules/elastic-container-registry"
  registry_name = local.worker_registry_name
}

module "scheduler_registry" {
  source = "../modules/elastic-container-registry"
  registry_name = local.scheduler_registry_name
}
