class UpstreamError(Exception):
    status_code = 502
    category = "upstream_failure"

class UpstreamTimeout(UpstreamError):
    status_code, category = 504, "timeout"

class UpstreamPermissionDenied(UpstreamError):
    status_code, category = 503, "permission_denied"

class UpstreamRateLimited(UpstreamError):
    status_code, category = 429, "rate_limited"

class UpstreamUnavailable(UpstreamError):
    status_code, category = 503, "service_unavailable"

class SimulationError(Exception):
    pass
