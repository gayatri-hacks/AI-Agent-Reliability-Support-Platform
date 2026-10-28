import asyncio
from fastapi import APIRouter, Header, HTTPException
from app.config import get_settings
from app.core.errors import UpstreamPermissionDenied, UpstreamRateLimited, UpstreamTimeout, UpstreamUnavailable
router = APIRouter(prefix="/api/v1/simulations", tags=["simulations"])
SCENARIOS = {"permission_denied": (503, "Vertex AI IAM permission failure"), "timeout": (504, "Upstream timeout"), "application_error": (500, "Synthetic processing exception"), "rate_limit": (429, "Upstream rate limit"), "service_unavailable": (503, "Upstream service unavailable"), "slow_request": (200, "Bounded synthetic delay")}
def authorize(token: str | None):
    settings = get_settings()
    if not settings.simulations_available or token != settings.simulation_token: raise HTTPException(404, "Not found")
@router.get("")
async def list_scenarios(x_simulation_token: str | None = Header(default=None)):
    authorize(x_simulation_token); return {"synthetic": True, "scenarios": SCENARIOS}
@router.post("/{scenario}")
async def simulate(scenario: str, x_simulation_token: str | None = Header(default=None)):
    authorize(x_simulation_token)
    if scenario not in SCENARIOS: raise HTTPException(404, "Unknown scenario")
    if scenario == "slow_request": await asyncio.sleep(.25); return {"synthetic": True, "scenario": scenario, "result": "completed"}
    code, message = SCENARIOS[scenario]
    if scenario == "permission_denied": raise UpstreamPermissionDenied(message)
    if scenario == "timeout": raise UpstreamTimeout(message)
    if scenario == "rate_limit": raise UpstreamRateLimited(message)
    if scenario == "service_unavailable": raise UpstreamUnavailable(message)
    raise RuntimeError(message)
