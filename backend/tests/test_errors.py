import pytest
from app.core.errors import UpstreamPermissionDenied, UpstreamRateLimited, UpstreamTimeout
from app.dependencies import analyzer_dependency
from app.services.incident_analyzer import IncidentAnalyzer
class ErrorProvider:
    def __init__(self, error): self.error=error
    async def generate_json(self, *_): raise self.error
    async def generate_text(self, *_): raise self.error
@pytest.mark.parametrize(("error","status"), [(UpstreamTimeout("x"),504),(UpstreamPermissionDenied("x"),503),(UpstreamRateLimited("x"),429)])
def test_classified_upstream_errors(client, error, status):
    from app.config import get_settings
    client.app.dependency_overrides[analyzer_dependency] = lambda: IncidentAnalyzer(ErrorProvider(error), get_settings())
    assert client.post("/api/v1/analyze", json={"incident_type":"timeout","error_message":"bad","service_name":"api"}).status_code == status
def test_unexpected_exception_hidden(client):
    response = client.post("/api/v1/simulations/application_error", headers={"X-Simulation-Token":"test-token"}); assert response.status_code == 500 and "RuntimeError" not in response.text
