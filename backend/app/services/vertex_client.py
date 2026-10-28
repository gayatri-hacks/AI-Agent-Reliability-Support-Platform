import asyncio
import json
from typing import Protocol

from app.config import Settings
from app.core.errors import (
    UpstreamError,
    UpstreamPermissionDenied,
    UpstreamRateLimited,
    UpstreamTimeout,
    UpstreamUnavailable,
)


class AIProvider(Protocol):
    async def generate_json(self, prompt: str, schema: dict) -> dict: ...
    async def generate_text(self, prompt: str) -> str: ...

class VertexProvider:
    def __init__(self, settings: Settings):
        if not settings.gcp_project_id: raise UpstreamUnavailable("Vertex AI is not configured")
        self.settings = settings
        try:
            from google import genai
        except ImportError as exc:
            raise UpstreamUnavailable("google-genai SDK is not installed") from exc
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
        from google.genai import types
        result = await self._generate(prompt, types.GenerateContentConfig(response_mime_type="application/json", response_schema=schema, temperature=0.1))
        return json.loads(result.text)
    async def generate_text(self, prompt):
        from google.genai import types
        return (await self._generate(prompt, types.GenerateContentConfig(temperature=0.2))).text

class MockProvider:
    """Local-only deterministic provider; never selected unless MOCK_MODE=true."""
    async def generate_json(self, prompt: str, schema: dict) -> dict:
        return {
            "severity": "medium",
            "probable_causes": ["Mock-mode response; no Vertex AI request was made"],
            "diagnostic_steps": ["Inspect the request ID in local structured logs"],
            "remediation_steps": ["Configure Vertex AI credentials for live analysis"],
        }

    async def generate_text(self, prompt: str) -> str:
        return "Mock mode is active. Configure Vertex AI credentials for live support responses."
