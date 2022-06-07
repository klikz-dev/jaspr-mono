from .root import env

RQ = {
    # The `@job` decorator will set this value as a default `result_ttl` in seconds.
    # NOTE: Right now, we don't do anything with results in the codebase (as of March
    # 2019). However, if we ever did, this value might want to be increased so results
    # could stay around longer.
    "DEFAULT_RESULT_TTL": 300
}
RQ_QUEUES = {
    "high": {
        "URL": env("REDIS_URL"),
        # Default database is 0. Override in local if you want a different one.
        "DB": 0,
        # High jobs shouldn't take longer than 30 minutes to run
        "DEFAULT_TIMEOUT": 1800,
    },
    "default": {
        "URL": env("REDIS_URL"),
        # Default database is 0. Override in local in if you want a different one.
        "DB": 0,
        # Default jobs shouldn't take longer than 30 minutes to run
        "DEFAULT_TIMEOUT": 1800,
    },
    "low": {
        "URL": env("REDIS_URL"),
        # Default database is 0. Override in local if you want a different one.
        "DB": 0,
        # Low jobs shouldn't take longer than one hour to run.
        "DEFAULT_TIMEOUT": 3600,
    },
}
# If `REDIS_TOKEN` is in the environment, we assume that's the `AUTH`
# (https://redis.io/commands/auth) to provide for Redis, which for `django_rq` is
# `"PASSWORD"`, and for the underlying `redis-py` library, it's just `password=` in the
# `Connection` kwargs.

# redis_token = env("REDIS_TOKEN", default=None)
# if redis_token is not None:
#    for queue_configuration in RQ_QUEUES:
#        queue_configuration["PASSWORD"] = redis_token

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True, # Mimic Memcache with no exceptions
        },
    }
}