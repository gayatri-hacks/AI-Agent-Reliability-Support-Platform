from app.config import Settings


def readiness(settings: Settings):
    return {"status": "ready", "configuration": {"vertex_configured": bool(settings.gcp_project_id), "environment": settings.environment, "model": settings.vertex_model}}
