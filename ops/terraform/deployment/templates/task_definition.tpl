[
  {
    "name": "${container_name}",
    "image": "${erc_image_url}",
    "portMappings": [
      {
        "containerPort": 5000,
        "hostPort": 5000,
        "protocol": "tcp"
      }
    ],
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "${awslog_group}",
            "awslogs-region": "${region}",
            "awslogs-stream-prefix": "api-server"
        }
    },
    "environment": ${environment_vars},
    "secrets": [
      {
        "name": "AWS_ACCESS_KEY_ID",
        "valueFrom": "${aws_access_key_arn}"
      },
      {
        "name": "AWS_SECRET_ACCESS_KEY",
        "valueFrom": "${aws_secret_key_arn}"
      },
      {
        "name": "TWILIO_AUTH_TOKEN",
        "valueFrom": "${twilio_auth_token_arn}"
      },
      {
        "name": "DJANGO_SECRET_KEY",
        "valueFrom": "${django_secret_key_arn}"
      },
      {
        "name": "FERNET_KEYS",
        "valueFrom": "${fernet_keys_arn}"
      },
      {
        "name": "EPIC_CLIENT_ID",
        "valueFrom": "${epic_client_id_arn}"
      },
      {
        "name": "EPIC_BACKEND_CLIENT_ID",
        "valueFrom": "${epic_backend_client_id_arn}"
      },
      {
        "name": "EPIC_PRIVATE_KEY",
        "valueFrom": "${epic_private_key_arn}"
      },
      {
        "name": "DATABASE_URL",
        "valueFrom": "${database_url_arn}"
      },
      {
        "name": "REDIS_URL",
        "valueFrom": "${redis_url_arn}"
      },
      {
        "name": "SENTRY_DSN",
        "valueFrom": "${sentry_dsn_arn}"
      }
    ],
    "user": "django",
    "healthCheck": {
      "command": [ "CMD-SHELL", "curl -f http://localhost:5000/health-check?auth=7qp6FnKJLYHa3F6y || exit 1" ],
      "startPeriod": 120,
      "retries": 4,
      "interval": 30
    },
    "cpu": ${cpu},
    "memory": ${memory}
  }
]