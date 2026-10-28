#!/usr/bin/env bash
set -euo pipefail
: "${PROJECT_ID:?Set PROJECT_ID}"; : "${REGION:=us-central1}"
gcloud services enable run.googleapis.com aiplatform.googleapis.com artifactregistry.googleapis.com monitoring.googleapis.com --project "$PROJECT_ID"
gcloud artifacts repositories create incident-support --repository-format=docker --location="$REGION" --project="$PROJECT_ID" || true
