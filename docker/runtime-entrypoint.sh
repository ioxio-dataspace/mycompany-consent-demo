#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Works even when mounted on Windows
export INVOKE_RUN_SHELL="/bin/sh"

# Using PORT if defined (in Google Cloud Run), defaulting to 8080
export PORT=${PORT:-8080}

set -- poetry run invoke serve
exec "$@"
