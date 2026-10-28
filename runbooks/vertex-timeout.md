# DeadlineExceeded — upstream timeout

## Summary, symptoms, impact, detection

Vertex calls reach timeout and return 504 after bounded retries. Impact is delayed/failed analysis; detect in latency charts and structured logs. Evidence examples are hypothetical.

## Reproduce and evidence

Use local protected `timeout` simulation. Collect request ID, latency, model, retry count, quota and regional availability evidence.

## Diagnostics

`gcloud logging read 'resource.type="cloud_run_revision" AND jsonPayload.error_category="timeout"' --project PROJECT`

## Root cause, remediation, prevention, verification, lessons

Typical causes are model congestion, an undersized budget, or network disruption. Validate model/region, tune only within Cloud Run timeout, and preserve retry limits. Verify a controlled request and latency recovery. Lesson: retries need budgets.

## Verification and lessons learned

Verify with a controlled request and recovered latency; do not label sample simulation evidence as a cloud incident.
