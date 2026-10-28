# PermissionDenied — Vertex AI IAM failure

## Summary, symptoms, impact, detection

Vertex calls return 503 with `permission_denied`; analysis is unavailable. Detect through Cloud Run logs, 5xx alert, and request ID. Sample evidence below is hypothetical, not a verified incident.

## Reproduce and evidence

Use the protected `permission_denied` simulation locally. Collect request ID, Cloud Run revision, runtime service account, audit logs, and deployment change history.

## Diagnostics

`gcloud run services describe incident-support-api --region REGION`  
`gcloud projects get-iam-policy PROJECT --flatten='bindings[].members' --filter='bindings.members:incident-support-runtime'`

## Root cause, remediation, prevention, verification, lessons

Likely missing `roles/aiplatform.user` on the runtime identity or wrong project. Grant minimum role, redeploy, then invoke authenticated health and a non-sensitive test request. Prevent with Terraform/IAM review and deployment checks. Lesson: distinguish deploy identity from runtime identity.

## Verification and lessons learned

Verify the 403 is absent for a test request and record only verified evidence. The primary lesson is least-privilege identity separation.
