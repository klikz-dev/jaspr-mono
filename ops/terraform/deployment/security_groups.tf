
resource "aws_security_group" "alb_sg" {
  name        = "alb_sg_${local.deployment_name}"
  description = "Allow App Traffic"
  vpc_id      = local.vpc_id

  ingress {
    description = "TLS from VPC"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb_sg"
  }
}

resource "aws_security_group" "background_worker_sg" {
  name        = "background_worker_sg_${local.deployment_name}"
  description = "Allow App Traffic"
  vpc_id      = local.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "background_worker_sg"
  }
}

resource "aws_security_group" "api_server_sg" {
  name        = "api_server_sg_${local.deployment_name}"
  description = "Allow App Traffic"
  vpc_id      = local.vpc_id

  /*ingress {
    description = "TLS from VPC"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
    self = true
  }*/

  ingress {
    description = "TLS from VPC"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "api_server_sg"
  }
}

resource "aws_security_group" "postgres_sg" {
  name        = "postgres_sg_${local.deployment_name}"
  description = "Allow Postgres Traffic"
  vpc_id      = local.vpc_id

  ingress {
    description = "Postgres TCP from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [
      aws_security_group.api_server_sg.id,
      aws_security_group.background_worker_sg.id
    ]
    self = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "postgres_sg"
  }
}

resource "aws_security_group" "segment_postgres_sg" {
  count       = var.environment == local.PRODUCTION ? 1 : 0
  name        = "segment_postgres_sg"
  description = "Allow Postgres Traffic"
  vpc_id      = local.vpc_id

  ingress {
    description = "Postgres TCP from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [
      "52.25.130.38/32",   # Segment.io
      "34.208.207.197/32", # Tableau: 10ax.online.tableau.com, US West, Oregon
      "52.39.159.250/32",  # Tableau: 10ax.online.tableau.com, US West, Oregon
      "34.218.129.202/32", # Tableau: 10ay.online.tableau.com, US West, Oregon
      "52.40.235.24/32",   # Tableau: 10ay.online.tableau.com, US West, Oregon
      "34.218.83.207/32",  # Tableau: 10az.online.tableau.com, US West, Oregon
      "52.37.252.60/32",   # Tableau: 10az.online.tableau.com, US West, Oregon
      "34.214.85.34/32",   # Tableau: US West, Oregon
      "34.214.85.244/32",  # Tableau: US West, Oregon
      "98.237.201.201/32", # JACOB Office
      "71.227.225.114/32"  # EMMA
    ]
    self = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "segment_postgres_sg"
  }
}

resource "aws_security_group" "redis_sg" {
  name        = "redis_sg_${local.deployment_name}"
  description = "Allow Postgres Traffic"
  vpc_id      = local.vpc_id

  ingress {
    description = "Redis TCP from VPC"
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    security_groups = [
      aws_security_group.api_server_sg.id,
      aws_security_group.background_worker_sg.id
    ]
    self = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "redis_sg"
  }
}

