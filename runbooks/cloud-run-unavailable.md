# ServiceUnavailable — Cloud Run availability issue

## Summary, symptoms, impact, detection

Requests may return 503 during revision, upstream, or capacity problems. Detect with Cloud Run request metrics and logs. No real outage is claimed.

## Reproduce and evidence

Use protected `service_unavailable` locally. Collect revision traffic split, instance count, deployment history, quotas, and request IDs.

## Diagnostics

`gcloud run revisions list --service incident-support-api --region REGION`  
Review Cloud Monitoring request count, 5xx rate, CPU and memory.

## Root cause, remediation, prevention, verification, lessons

Rollback unhealthy revisions, correct configuration, or adjust bounded concurrency/resources. Verify authenticated requests and 5xx recovery. Prevention: canary rollouts, alerts, and capacity tests. Lesson: separate application and platform evidence.

## Verification and lessons learned

Verify normal authenticated traffic and recovered error rate. Keep synthetic and real evidence distinct.
