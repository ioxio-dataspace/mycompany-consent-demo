#!/usr/bin/env bash
#
# This step is for initializing the runtime environment
#

# shellcheck disable=SC2039
set -exuo pipefail

apt-get update
apt-get install -y --no-install-recommends \
    curl \

# Set up PYTHONPATH for the main package. Only this module will be installed
su "${USER}" -c ". ${POETRY_HOME}/env; poetry install --no-dev"

# Prevent parse-template from failing with permission error at runtime
chown "${USER}:${GROUP}" /etc/nginx/conf.d/default.conf

# Ensure user cannot edit the filesystem contents
chown -R root:root .
