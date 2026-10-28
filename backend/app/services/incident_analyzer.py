import time

from app.config import Settings
from app.core.retry import retry_transient
from app.schemas import AnalysisResult, ChatRequest, IncidentRequest
from app.services.vertex_client import AIProvider


class IncidentAnalyzer:
    def __init__(self, provider: AIProvider, settings: Settings): self.provider, self.settings = provider, settings
    async def analyze(self, incident: IncidentRequest):
        prompt = ("You are an SRE. Return concise remediation for this incident. Do not include secrets. "
                  f"Type: {incident.incident_type}; service: {incident.service_name}; error: {incident.error_message}; context: {incident.context}")
        start = time.perf_counter(); data = await retry_transient(lambda: self.provider.generate_json(prompt, AnalysisResult.model_json_schema()))
        return AnalysisResult.model_validate(data), int((time.perf_counter()-start)*1000)
    async def chat(self, message: ChatRequest):
        start = time.perf_counter(); answer = await retry_transient(lambda: self.provider.generate_text(f"You are an SRE. Give safe, actionable advice: {message.question}. Context: {message.context}"))
        return answer, int((time.perf_counter()-start)*1000)
