
resource "aws_lb" "api-server-lb" {
  name               = "lb-${local.deployment_name}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = local.public_subnet_ids


  access_logs {
    bucket = local.ACCESS_LOG_S3_BUCKET_NAME[var.environment]
    prefix = "api-lb"
    enabled = true
  }
}

resource "aws_lb_target_group" "api-server-lb-target-group" {
  name     = "lbtg-${local.deployment_name}"
  port     = 5000
  protocol = "HTTP"
  target_type = "ip"
  vpc_id   = local.vpc_id
  slow_start = 120 # 30 Second Delay for Django to startup
  depends_on = [aws_lb.api-server-lb]

  health_check {
    interval = 30
    path = "/health-check"
    port = 5000
    protocol = "HTTP"
    timeout = 5
    healthy_threshold = 2
    unhealthy_threshold = 2
    matcher = "200"
  }
}

resource "aws_alb_listener" "api-server_alb_listener" {
  load_balancer_arn = aws_lb.api-server-lb.arn
  port = 80
  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_alb_listener" "api-alb-listener-443" {
  load_balancer_arn = aws_lb.api-server-lb.arn
  port = 443
  protocol = "HTTPS"
  certificate_arn = data.aws_acm_certificate.api_cert.arn

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.api-server-lb-target-group.arn
  }
}
