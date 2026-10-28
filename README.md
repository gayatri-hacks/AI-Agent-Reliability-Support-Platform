# AI Agent Reliability & Support Platform

Production-inspired portfolio monorepo for an incident-support API. It uses FastAPI, structured JSON logs, retries, protected fault injection, Vertex AI through the supported `google-genai` Vertex mode, Cloud Run/Terraform configuration, GitHub Actions WIF deployment, and a Vite operations dashboard.

## What is implemented

- `backend`: typed API, liveness/readiness, centralized safe errors, request/trace IDs, Cloud Logging-compatible stdout events, bounded transient retries, mockable provider abstraction.
- `frontend`: responsive dark SRE dashboard. It labels unavailable data rather than inventing metrics.
- `infrastructure/terraform`: Artifact Registry, private Cloud Run, minimal Vertex runtime role, dashboard and 5xx alert.
- `runbooks`: safe reproduction, evidence, diagnostics, RCA, remediation, prevention, verification and lessons for four common failures.

## Local setup

```bash
python3 -m venv .venv && .venv/bin/pip install -r backend/requirements-dev.txt
PYTHONPATH=backend .venv/bin/uvicorn app.main:app --reload --port 8080
curl localhost:8080/health/ready
PYTHONPATH=backend .venv/bin/pytest backend/tests
cd frontend && npm install && npm run build
```

For local analysis tests, the suite injects a mock provider. To use Vertex, set `GCP_PROJECT_ID`, authenticate with `gcloud auth application-default login`, and ensure the identity has Vertex access. No API key is used.

For a fully local demonstration without the Vertex SDK or credentials, start the API with `MOCK_MODE=true`; its responses explicitly identify mock mode and never claim a Vertex call occurred.

## Cloud deployment

Do not deploy until you have an authorized project and billing approval. Copy `infrastructure/terraform/terraform.tfvars.example`, run Terraform, then use `scripts/deploy.sh`. Cloud Run is private by default; call it with the identity-token example in [deployment docs](docs/deployment.md). The Terraform config does not create an external uptime check because a private endpoint needs an explicitly designed authenticated probe.

## Security and costs

No credentials are committed. The runtime identity has `roles/aiplatform.user`, not Owner/Editor. Simulations require development mode plus a token and return 404 otherwise. Cloud Run starts at zero instances, maximum four, 512MiB/1 CPU, concurrency 40. Vertex/model usage and monitoring retention incur costs.

## Verification status

Local unit/integration tests, lint, frontend build, Docker build, and Terraform validation should be run from this checkout. This repository does **not** claim a real Google Cloud deployment, credential validation, live Vertex inference, or real monitoring values; those require user-authorized cloud credentials and are intentionally pending.

See [architecture](docs/architecture.md), [monitoring](docs/monitoring.md), [simulations](docs/incident-simulation.md), and [interview guide](docs/interview-guide.md).
