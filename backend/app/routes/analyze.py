from fastapi import APIRouter, Depends, Request
from app.config import get_settings
from app.dependencies import analyzer_dependency
from app.schemas import AnalyzeResponse, IncidentRequest
from app.services.incident_analyzer import IncidentAnalyzer
router = APIRouter(prefix="/api/v1", tags=["analysis"])
@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(incident: IncidentRequest, request: Request, analyzer: IncidentAnalyzer = Depends(analyzer_dependency)):
    result, latency = await analyzer.analyze(incident)
    return AnalyzeResponse(request_id=request.state.request_id, incident_type=incident.incident_type, model_used=get_settings().vertex_model, latency_ms=latency, **result.model_dump())
