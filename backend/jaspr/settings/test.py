"""
Settings for running tests locally.

Ordering/Derivation Chart:
- root --> local_mixin --> base --> ci --> test
"""

from .ci import *  # isort:skip  # noqa

# Django RQ
# ------------------------------------------------------------------------------
# For local testing, we set the test Redis logical database to `2` so that it doesn't
# conflict with local development.
redis_regex = re.compile(r"\/([0-9]+)$")
for queue_config in RQ_QUEUES.values():
    redis_url = queue_config["URL"]
    if redis_match := redis_regex.search(redis_url):
        logical_database_number = int(redis_match.group(1))
        assert (
            logical_database_number != 2
        ), "Logical database 2 locally is for testing."
        new_redis_url = f"{redis_regex.sub('', redis_url)}/2"
    else:
        new_redis_url = redis_url
        if not redis_url.endswith("/"):
            new_redis_url += "/"
        new_redis_url += "2"
    assert re.search(r"[^/]\/2$", new_redis_url)
    queue_config["URL"] = new_redis_url

# Epic
# Note, this key is for testing only.  Do not use a production key here
EPIC_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9VC3jVUqEtqoA\ntuvNZRA23cSDQ5eN1q0F7ciDzI9J+F6Gd1d3MgIeQcjfhF8YhopKLRFvfIvzak30\n4mvfd/08deG1LKZgxOpbOeBt9gQTaXmK4dq4Me0EL6nD9XcSMlT/Rphn/PUSa01W\nHUYcQ4A922i5rteaopandxkCS/D71QT8i28F03t+AC9gsfnpv1rCzEgVySLBVkFr\nHYh6jTY+Gi0x4HiVDFiqLMwFCpY+EV4+9V+v6IxUuyUXUK9QFWkTQICygghcCJ+V\nYyv+DP3mYm/ls05bHNhwaX1DP8dp3vcFdJm6NkqFFhwdow4XBNlaIH7ukBZY3f01\n+gXiYvepAgMBAAECggEAGDevUvfy+zzeTA8Z5ID77Pi7DUtVFHiUU0DSOEGvRnf1\np1+WmZGVAcfKaQTmoR18jPZs14Tn5fAAHsXjpIcVpmkxwNoAQjqN+7NQiOBCLzV7\nrY8sSglg1vs9zOoWHAbCJpEiJ5MMyhldoBlIgY8E1WS+ZZn+zDHl8W/jjA6ouZ2S\nRbj1WFjT6J2AUQY0Y03icDIPbRg3Ek7cstVYmrb0Cep0pFNofMgVjezoxVrmT+D/\n+Y/klmQLTuV3hRG01EEVi6nEQcGi2yTwygVyMxRrJnXBhH7Q3RLBvpPXT5Ry5N6h\n4hilCTEFHLtuwn9CHlkNAx2e8cimUDZsjg/dzJfcrQKBgQD18lf7nsU7E5wNZ6hF\np9YbhnO01Hjg8N+uPiOXHyd2aRlZgkVZ0AUFVhpBykuJtC5vmPizFIu5pQX1q+xt\ngdm7jTFsoFQFyvbjV3NBZXlmTYssE0YTN6ozJQESMZvcKTQusGkA2hWqAMLQHrIV\nK6dxYlaZwGnIejmB2uPIOeGC9wKBgQDFEV7QC6Zx9xkC5k1dHfWnPuVd7lpMjDZ5\nt1+Hgq7NwujeOm4c5qn9uukEftsncwjVlw7W/CYT2zNi1ECPrb5LgSH73nOeMetK\nPqmz6rxDArA88XlAhDv8/U3qJ7oDlOfGQ4+7JOW1v5U+cGuApGuA8WMKm4TBVort\nvH1+efISXwKBgHXL3cIBOFvkN4DgHeNG0LCcQ/zfKwoptCiDUI6H+GGpUt/hGhA7\nJrx4kdji6C0LJJaEwNEczRNca69P6cxFPiCrLnnljHi9zmPytZwj2vJZv4ebr5ty\ntM0MMyggpJLdFUYrbg9fZLLo7GW73fVv1CHlRK8dTk0b5UFBsolq14zfAoGBAIOE\nESt06vLZvjZiLjU7nkqsPfSO8nJtjJl0WGueOjyVnEVa50ugYMg1afcXFfjg2393\n3W56Pos32bZWAnQgtoO7PUvS7IQhum4FHco1mMh7zdQOLyZwWXyAK/Rd6NUlFf0J\n760sdaTyo45VBlmG4TvfXIKiwVkqAXOhPHsgtP2vAoGAEsofcoyU/sLqsoKWtrwm\nDNY9cs6zB5sRF4AEUII/dAdoH3w5OJNLCSTgzUyjnkGmujzkgCCigbOUl5jRkGu1\n0opRrjqEoiGTFcAmJ9If4V6yduMRR+ccrMTbBFQOfSzZeBpXeJHHWY/cXbTJXSua\nUEPtcz8lZs3ecjWUFCwsZqM=\n-----END PRIVATE KEY-----"
