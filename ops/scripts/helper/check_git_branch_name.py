import sys
import re

"""
The deployment system converts the git branch name into the subdomain used to host the feature branch builds.
As a result, we need to make sure no one uses a character this isn't allowed.
"""

PATTERN = "^[A-Za-z0-9\-]+$"
expression = re.compile(PATTERN)
branch = sys.argv[1]
result = expression.match(branch)
if result is not None:
    print("Valid branch name.")
    sys.exit(0)
else:
    print(f"Invalid branch name: {branch}")
    sys.exit(1)
