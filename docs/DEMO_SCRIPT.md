# Five-minute interview demo

## Start exactly here

Terminal 1:

```bash
PYTHONPATH=backend MOCK_MODE=true ENABLE_SIMULATIONS=true SIMULATION_TOKEN=demo-token \
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8080
```

Terminal 2:

```bash
npm --prefix frontend run dev -- --host 127.0.0.1
```

Open the URL Vite prints (normally `http://127.0.0.1:5173`). The frontend defaults to `http://localhost:8080`; set `VITE_API_BASE_URL=http://127.0.0.1:8080` if using the 127.0.0.1 Vite URL. The API permits both local Vite origins through CORS.

## Presentation flow

**0:00–0:30 — purpose.** “This is an incident-support API and operations dashboard. It takes a technical failure, produces structured diagnostic guidance, and is designed to run on Cloud Run with Vertex AI.”

**0:30–1:15 — health and architecture.** Show the dashboard’s green API badge. Explain: React calls FastAPI; request middleware assigns/propagates an ID and emits JSON stdout logs; the provider interface separates the API from Vertex AI; Terraform defines Cloud Run, IAM, Artifact Registry, and monitoring resources.

**1:15–2:30 — successful analysis.** Open *Incident Analyzer*, leave the realistic timeout example, and click **Analyze incident**. Point out severity, lists, latency, and returned request ID. State: “This run is explicit `MOCK_MODE=true`, so the response says that no Vertex request was made.”

**2:30–3:30 — protected failure.** Show *Failure Lab*, then run the two commands below. The first is intentionally indistinguishable from a missing route (404); the second returns safe 504 timeout JSON.

**3:30–4:30 — observability/reliability.** Show the request ID returned in both body and `X-Request-ID`. Explain that logging captures request ID, trace ID when supplied by Google, method, endpoint, status, latency, service, and sanitized error category. Transient timeout/429/503 failures use capped exponential backoff with jitter; permission failures do not retry.

**4:30–5:00 — honest close.** “The local suite tests this with mocks. Terraform and GitHub Actions are ready, but I have not claimed a Cloud Run deployment, live Monitoring data, or a live Vertex result without authorized GCP credentials.”

## Requests and expected results

```bash
curl -i http://127.0.0.1:8080/health/live
curl -i http://127.0.0.1:8080/health/ready
curl -i -H 'Content-Type: application/json' -H 'X-Request-ID: interview-001' \
  -d '{"incident_type":"timeout","error_message":"Vertex AI request exceeded timeout while processing the incident summary.","service_name":"incident-support-api","context":"Intermittent failures began after a traffic increase."}' \
  http://127.0.0.1:8080/api/v1/analyze
curl -i -X POST http://127.0.0.1:8080/api/v1/simulations/timeout
curl -i -X POST -H 'X-Simulation-Token: demo-token' http://127.0.0.1:8080/api/v1/simulations/timeout
```

Expected statuses: 200, 200, 200, 404, and 504. The analysis includes `request_id: interview-001`; mock responses say no Vertex call was made.

## Common questions

**Why FastAPI?** Typed Pydantic validation, automatic OpenAPI, async-compatible request handling, and dependency injection make provider mocking straightforward.

**How does production auth work?** Cloud Run’s dedicated runtime service account uses Application Default Credentials; no AI Studio API key is used. It receives the minimal Vertex AI user role.

**Why both liveness and readiness?** Liveness is process-only. Readiness reports local initialization/config state and deliberately avoids expensive model inference.

**How do you debug a request?** Start with the returned request ID, then correlate JSON Cloud Run logs and Google trace context when available.

**What does mock mode prove?** It proves endpoint validation, provider injection, structured responses, UI integration, logging, status mapping, and protected simulations. It does not prove Vertex availability, credentials, model output, latency, or cloud deployment.
