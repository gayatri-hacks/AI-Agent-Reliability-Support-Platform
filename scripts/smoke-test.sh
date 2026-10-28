#!/usr/bin/env bash
set -euo pipefail
: "${SERVICE_URL:?Set SERVICE_URL}"; curl --fail --silent --show-error -H "Authorization: Bearer $(gcloud auth print-identity-token)" "$SERVICE_URL/health/live"
