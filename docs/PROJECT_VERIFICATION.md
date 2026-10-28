# Project verification

## Implemented

- FastAPI health, analysis, support, structured errors, request IDs, JSON logging, retry policy, CORS for local Vite origins, and protected development-only simulations.
- React/Vite dashboard using `VITE_API_BASE_URL` (default `http://localhost:8080`) and a live readiness probe.
- Explicit `MOCK_MODE=true` provider; it never calls Vertex AI and identifies itself in the response.
- Dockerfile, Terraform configuration, runbooks, and GitHub Actions CI/CD source.

## Tested locally

- Ruff completed successfully.
- Pytest completed successfully: 15 tests, including CORS, request IDs, retries, failure mapping, redaction, and simulation authorization.
- Frontend TypeScript check and production build completed successfully.
- Manual mock API check: health 200, analysis 200, unauthenticated simulation 404, authorized timeout simulation 504.

## Pending / not represented as complete

- No live Vertex AI inference, Vertex credentials, Cloud Run deployment, Artifact Registry push, Cloud Monitoring dashboard data, or alert delivery has been verified.
- Docker build is pending a running Docker daemon.
- Terraform validation/apply is pending a Terraform installation and an authorized, billed GCP project.
- GitHub Actions workflow syntax was locally parsed, but no remote workflow run is claimed.

## Requirements before real GCP deployment

Use an authorized billed project, enable required APIs, create/configure Workload Identity Federation with repository restrictions, grant deployment roles, provision the runtime service account, choose a supported Vertex model/region, and provide a private-service smoke-test identity. Keep `MOCK_MODE=false` in Cloud Run.
