"""
This script is used in the fixture transfer process (moving fixtures from release to integration and production).
It checks to see if the bucket and key provided as arguments has been touched in the last 2 minutes.
Its assumed that if the fixture file has been updated, it was done by the scheduler process that was just relaunched
with Env Vars instructing it to dump particular fixture data to json and sent to S3.

@arg1 S3 bucket name
@arg2 S3 Key Name (full path within the bucket)
"""

import sys
import os
import json
from dateutil.parser import parse
from datetime import datetime, timezone, timedelta
import time

S3_BUCKET = sys.argv[1]
S3_KEY = sys.argv[2]

SLEEP_TIME = 30
ERROR_TIME = 15 * 60 # 15min
ITERATIONS_UNTIL_ERROR = ERROR_TIME / SLEEP_TIME

def check_for_fixtures():
    try:
        with os.popen(f'aws s3api head-object --bucket {S3_BUCKET} --key {S3_KEY}') as stream:
            file_metadata = json.load(stream)
    except Exception as e:
        return False

    last_modified = parse(file_metadata["LastModified"])
    print(last_modified)
    now = datetime.now(timezone.utc)
    delta = now - last_modified
    max_delta = timedelta(minutes=2)
    print(delta)
    print(max_delta)
    return delta < max_delta


if __name__ == "__main__":
    itr_countdown = ITERATIONS_UNTIL_ERROR
    while True:
        print("Starting new fixture check loop")
        time.sleep(30)
        print("checking...")
        if check_for_fixtures():
            break
        itr_countdown -= 1
        print("fixture not found...")
        if itr_countdown <= 0:
            print("Max iteration limit reached. Fixture still not found.")
            sys.exit(1)

    print("Fixture found. Success.")
    sys.exit(0)