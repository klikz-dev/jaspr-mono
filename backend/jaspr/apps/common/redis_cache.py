import hashlib
from functools import wraps
from django.core.cache import caches, DEFAULT_CACHE_ALIAS
from django.utils.encoding import force_bytes

TTL = 500  # 5min
MARKER = object()


def class_cache(
        timeout=TTL,
        key_fields=None,
        key_func=None,
        prefix=None,
        cache_exceptions=(),
        cache_alias=DEFAULT_CACHE_ALIAS
):
    def decorator(func):
        def _make_cache_key(*args, **kwargs):
            cache_key = ""
            instance = args[0]
            if key_fields:
                for key in key_fields:
                    cache_key += str(getattr(instance, key)) + ":"
            elif key_func:
                cache_key = key_func(instance)

            prefix_ = prefix or ".".join((func.__module__ or "", func.__qualname__))
            return hashlib.md5(
                force_bytes("class_cache" + prefix_ + cache_key)
            ).hexdigest()

        @wraps(func)
        def inner(*args, **kwargs):
            # The cache backend is fetched here (not in the outer decorator scope)
            # to guarantee thread-safety at runtime.
            cache = caches[cache_alias]
            cache_key = _make_cache_key(*args, **kwargs)
            result = cache.get(cache_key, MARKER)
            if result is MARKER:

                # If the function all raises an exception we want to cache,
                # catch it, else let it propagate.
                try:
                    result = func(*args, **kwargs)
                except cache_exceptions as exception:
                    result = exception

                cache.set(cache_key, result, timeout)

            # If the result is an exception we've caught and cached, raise it
            # in the end as to not change the API of the function we're caching.
            if isinstance(result, Exception):
                raise result
            return result

        def invalidate(*args, **kwargs):
            # The cache backend is fetched here (not in the outer decorator scope)
            # to guarantee thread-safety at runtime.
            cache = caches[cache_alias]
            kwargs.pop("_refresh", None)
            cache_key = _make_cache_key(*args, **kwargs)
            cache.delete(cache_key)

        def get_cache_key(*args, **kwargs):
            kwargs.pop("_refresh", None)
            return _make_cache_key(*args, **kwargs)

        inner.invalidate = invalidate
        inner.get_cache_key = get_cache_key
        return inner

    return decorator