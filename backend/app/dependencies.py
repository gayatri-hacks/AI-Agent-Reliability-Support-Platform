from functools import lru_cache
from fastapi import Depends
from app.config import Settings, get_settings
from app.services.incident_analyzer import IncidentAnalyzer
from app.services.vertex_client import VertexProvider
@lru_cache
def get_analyzer():
    settings = get_settings(); return IncidentAnalyzer(VertexProvider(settings), settings)
def analyzer_dependency() -> IncidentAnalyzer: return get_analyzer()
