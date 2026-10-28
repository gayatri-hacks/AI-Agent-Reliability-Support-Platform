# Monitoring

The Terraform dashboard uses Cloud Run request count and latency metrics. The included 5xx policy uses `run.googleapis.com/request_count` filtered by response-code class. Configure an uptime check only for a permitted authenticated probe or deliberately public endpoint; this project does not claim private `/health/live` is externally probeable.
