# InternalServerError — application exception

## Summary, symptoms, impact, detection

Unexpected processing failures return sanitized 500s. Detect through 5xx alert and request ID; no stack trace is exposed. Examples are hypothetical.

## Reproduce and evidence

Use the protected `application_error` simulation. Capture revision, request ID, structured error category, and sanitized server log.

## Diagnostics

`gcloud logging read 'resource.type="cloud_run_revision" AND severity>=ERROR' --project PROJECT`

## Root cause, remediation, prevention, verification, lessons

Inspect the exact revision and regression tests, then patch, test, deploy a new revision, and validate an authenticated request. Prevention: schema validation, exception handlers and CI. Lesson: error responses must be safe while logs remain actionable.

## Verification and lessons learned

Verify the new revision with the request ID and test suite; retain sanitized evidence only.
