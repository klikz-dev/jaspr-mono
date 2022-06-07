from typing import List, Literal

import django_rq
from django.conf import settings
from django.core.mail import send_mail
from django_twilio.client import twilio_client
from jaspr.apps.kiosk.models import Patient

DATABASE = "database"
CACHE = "cache"
TWILIO = "twilio"
EMAIL = "email"
HealthCheckType = List[Literal[DATABASE, CACHE, TWILIO, EMAIL]]

NULL_EMAIL_ADDRESS = "dev@jasprhealth.com"
SUBJECT = "Email Health Check"
EMAIL_TXT = "This email was sent as a health check."


def internal_health_check() -> HealthCheckType:
    could_not_reach: HealthCheckType = []

    try:
        ping_redis()
    except Exception as e:
        could_not_reach.append(CACHE)

    try:
        ping_postgres()
    except Exception:
        could_not_reach.append(DATABASE)

    return could_not_reach


def startup_health_check() -> HealthCheckType:
    could_not_reach: HealthCheckType = []

    try:
        ping_redis()
    except Exception:
        could_not_reach.append(CACHE)

    try:
        ping_postgres()
    except Exception:
        could_not_reach.append(DATABASE)

    try:
        ping_twilio()
    except Exception as err:
        could_not_reach.append(TWILIO)

    try:
        ping_email()
    except Exception as err:
        could_not_reach.append(EMAIL)

    return could_not_reach

def ping_redis() -> None:
    # Use `django_rq` (which we depend upon for pretty much all our redis stuff right
    # now anyways) to get the underlying `redis` (python library) connection and ping
    # Redis.
    conn = django_rq.get_connection()
    conn.ping()


def ping_postgres() -> None:
    # Pick a common-used model that's unlikely to change names or anything and just
    # query for the first one. This will definitely hit the database (calling `first`
    # will always evaluate the underlying `QuerySet` which will query the database).
    Patient.objects.values("pk").first()


def ping_twilio() -> None:
    return
    #if settings.ENVIRONMENT not in ("local", "test", "ci", "development"):
    #    twilio_client.api.accounts.list(limit=1)


def ping_email() -> None:
    return send_mail(
        SUBJECT,
        EMAIL_TXT,
        settings.DEFAULT_FROM_EMAIL,
        [NULL_EMAIL_ADDRESS],
        fail_silently=False,
    )
