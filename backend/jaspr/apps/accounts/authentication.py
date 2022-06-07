from .models import LogUserLoginAttempts


def log_login_attempt(
    user_id: int, ip: str, was_successful: bool, locked_out: bool
) -> LogUserLoginAttempts:
    return LogUserLoginAttempts.objects.create(
        user_id=user_id,
        ip_address=ip,
        was_successful=was_successful,
        locked_out=locked_out,
    )
