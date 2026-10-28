from fastapi import APIRouter, Depends, Request

from app.config import get_settings
from app.dependencies import analyzer_dependency
from app.schemas import ChatRequest, ChatResponse
from app.services.incident_analyzer import IncidentAnalyzer

router = APIRouter(prefix="/api/v1/support", tags=["support"])
@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatRequest, request: Request, analyzer: IncidentAnalyzer = Depends(analyzer_dependency)):
    answer, latency = await analyzer.chat(message)
    return ChatResponse(request_id=request.state.request_id, answer=answer, model_used=get_settings().vertex_model, latency_ms=latency)
@router.get("/examples")
async def examples():
    return {"examples": [{"incident_type":"timeout","error_message":"Vertex AI request exceeded timeout","service_name":"incident-support-api","context":"Requests are failing intermittently"}, {"incident_type":"permission_denied","error_message":"403 Permission denied","service_name":"incident-support-api","context":"New runtime identity deployed"}]}
