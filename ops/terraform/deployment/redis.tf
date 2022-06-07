locals {
  redis_port = 6379
}

resource "aws_elasticache_subnet_group" "redis_subnet" {
  name       = "redis-cache-subnet-${local.deployment_name}"
  subnet_ids = local.private_subnet_ids
}

resource "aws_elasticache_replication_group" "redis" {
  automatic_failover_enabled    = true
  availability_zones            = local.availability_zones
  replication_group_id          = "redis-rg-${local.deployment_name}"
  replication_group_description = "Main Redis Replication Group"
  node_type                     = var.environment == local.PRODUCTION ? "cache.m4.large" : "cache.t2.small"
  number_cache_clusters         = 2
  parameter_group_name          = "default.redis5.0"
  port                          = local.redis_port
  engine                        = "redis"
  engine_version                = "5.0.6"
  security_group_ids            = [aws_security_group.redis_sg.id]
  subnet_group_name             = aws_elasticache_subnet_group.redis_subnet.name
  at_rest_encryption_enabled    = true
  transit_encryption_enabled    = true

  lifecycle {
    ignore_changes = [number_cache_clusters]
  }
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id            = "jaspr-redis-${local.deployment_name}"
  count                 = 1
  replication_group_id  = aws_elasticache_replication_group.redis.id
}

resource "aws_secretsmanager_secret" "jaspr_redis_connection_secret" {
  name_prefix = "jaspr_redis_connection_${local.deployment_name}"
}

resource "aws_secretsmanager_secret_version" "jaspr_redis_connection_secret_version" {
  secret_id     = aws_secretsmanager_secret.jaspr_redis_connection_secret.id
  secret_string = "rediss://${aws_elasticache_replication_group.redis.primary_endpoint_address}:${local.redis_port}/0"
}