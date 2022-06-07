#!/bin/bash

###########
# Create a tag for this commit using the version from the commit message.
###########

VERSION=$(./get_software_version.sh)
git tag "$VERSION"
git push origin "$VERSION"
