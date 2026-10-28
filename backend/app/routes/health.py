from fastapi import APIRouter
from app.config import get_settings
from app.services.health_service import readiness
router = APIRouter(tags=["health"])
@router.get("/health/live")
async def live(): return {"status": "alive"}
@router.get("/health/ready")
async def ready(): return readiness(get_settings())
