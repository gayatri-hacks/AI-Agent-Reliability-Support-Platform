from functools import lru_cache

from app.config import get_settings
from app.services.incident_analyzer import IncidentAnalyzer
from app.services.vertex_client import MockProvider, VertexProvider


@lru_cache
def get_analyzer():
    settings = get_settings()
    provider = MockProvider() if settings.mock_mode else VertexProvider(settings)
    return IncidentAnalyzer(provider, settings)
def analyzer_dependency() -> IncidentAnalyzer: return get_analyzer()
