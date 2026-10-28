from typing import Literal

from pydantic import BaseModel, Field

IncidentType = Literal["timeout", "permission_denied", "application_error", "rate_limit", "service_unavailable", "other"]

class IncidentRequest(BaseModel):
    incident_type: IncidentType
    error_message: str = Field(min_length=3, max_length=4000)
    service_name: str = Field(min_length=2, max_length=120, pattern=r"^[a-zA-Z0-9._-]+$")
    context: str = Field(default="", max_length=8000)

class AnalysisResult(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    probable_causes: list[str] = Field(min_length=1, max_length=8)
    diagnostic_steps: list[str] = Field(min_length=1, max_length=10)
    remediation_steps: list[str] = Field(min_length=1, max_length=10)

class AnalyzeResponse(AnalysisResult):
    request_id: str
    incident_type: IncidentType
    model_used: str
    latency_ms: int

class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    context: str = Field(default="", max_length=8000)

class ChatResponse(BaseModel):
    request_id: str
    answer: str
    model_used: str
    latency_ms: int

class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: str | None = None
