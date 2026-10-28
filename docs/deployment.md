# Deployment

Copy `terraform.tfvars.example`, provide a real image URI, then run `terraform init && terraform validate && terraform apply`. Keep Cloud Run private and invoke it with `gcloud auth print-identity-token`. GitHub deployment requires repository variables `GCP_PROJECT_ID`, `REGION`, `ARTIFACT_REPOSITORY`, `CLOUD_RUN_SERVICE`, `WIF_PROVIDER`, and `DEPLOY_SERVICE_ACCOUNT`; WIF must be configured separately.
