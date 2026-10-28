import asyncio, json
from typing import Protocol
from google import genai
from google.genai import types
from app.config import Settings
from app.core.errors import UpstreamPermissionDenied, UpstreamRateLimited, UpstreamTimeout, UpstreamUnavailable, UpstreamError

class AIProvider(Protocol):
    async def generate_json(self, prompt: str, schema: dict) -> dict: ...
    async def generate_text(self, prompt: str) -> str: ...

class VertexProvider:
    def __init__(self, settings: Settings):
        if not settings.gcp_project_id: raise UpstreamUnavailable("Vertex AI is not configured")
        self.settings = settings
        self.client = genai.Client(vertexai=True, project=settings.gcp_project_id, location=settings.gcp_location)
    async def _generate(self, prompt, config):
        try:
            result = await asyncio.wait_for(asyncio.to_thread(self.client.models.generate_content, model=self.settings.vertex_model, contents=prompt, config=config), timeout=self.settings.vertex_timeout_seconds)
            return result
        except asyncio.TimeoutError as exc: raise UpstreamTimeout("Vertex request timed out") from exc
        except Exception as exc:
            text = str(exc).lower()
            if "permission" in text or "403" in text: raise UpstreamPermissionDenied("Vertex AI authorization failed") from exc
            if "429" in text or "resource exhausted" in text: raise UpstreamRateLimited("Vertex AI rate limit reached") from exc
            if "503" in text or "unavailable" in text: raise UpstreamUnavailable("Vertex AI unavailable") from exc
            raise UpstreamError("Vertex AI request failed") from exc
    async def generate_json(self, prompt, schema):
        result = await self._generate(prompt, types.GenerateContentConfig(response_mime_type="application/json", response_schema=schema, temperature=0.1))
        return json.loads(result.text)
    async def generate_text(self, prompt):
        return (await self._generate(prompt, types.GenerateContentConfig(temperature=0.2))).text
