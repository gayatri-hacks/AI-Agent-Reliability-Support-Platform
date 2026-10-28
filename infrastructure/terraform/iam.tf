resource "google_project_iam_member" "vertex_user" { project=var.project_id; role="roles/aiplatform.user"; member="serviceAccount:${google_service_account.runtime.email}" }
