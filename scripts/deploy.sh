#!/usr/bin/env bash
set -euo pipefail
: "${PROJECT_ID:?Set PROJECT_ID}"; : "${REGION:=us-central1}"
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/incident-support/incident-support:$(git rev-parse --short HEAD)"
gcloud builds submit backend --tag "$IMAGE" --project "$PROJECT_ID"
gcloud run deploy incident-support-api --image "$IMAGE" --region "$REGION" --no-allow-unauthenticated --project "$PROJECT_ID"
