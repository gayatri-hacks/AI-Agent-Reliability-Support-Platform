# Architecture

Cloud Run hosts a non-root FastAPI container. The runtime service account uses Application Default Credentials to call Vertex AI through `google-genai`. Cloud Run stdout is captured by Cloud Logging; request IDs and Cloud trace IDs correlate evidence. Terraform creates the service, least-privilege Vertex role, registry, dashboard and error alert.
