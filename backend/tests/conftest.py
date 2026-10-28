import pytest
from fastapi.testclient import TestClient
from app.config import get_settings
from app.dependencies import analyzer_dependency
from app.main import app

class MockProvider:
    async def generate_json(self, prompt, schema):
        return {"severity":"high","probable_causes":["Mocked upstream dependency"],"diagnostic_steps":["Inspect structured request logs"],"remediation_steps":["Retry after validating configuration"]}
    async def generate_text(self, prompt): return "Inspect the request ID and Cloud Logging evidence."

@pytest.fixture(autouse=True)
def config(monkeypatch):
    monkeypatch.setenv("ENABLE_SIMULATIONS", "true"); monkeypatch.setenv("SIMULATION_TOKEN", "test-token")
    get_settings.cache_clear()
    yield
    app.dependency_overrides.clear(); get_settings.cache_clear()

@pytest.fixture
def client():
    from app.services.incident_analyzer import IncidentAnalyzer
    app.dependency_overrides[analyzer_dependency] = lambda: IncidentAnalyzer(MockProvider(), get_settings())
    with TestClient(app, raise_server_exceptions=False) as value: yield value
