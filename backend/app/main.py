from collections import deque
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config import get_settings
from app.core.errors import UpstreamError
from app.core.logging import sanitize
from app.middleware.request_logging import RequestLoggingMiddleware, logger
from app.routes import analyze, health, simulations, support

settings = get_settings(); recent_events = deque(maxlen=settings.event_history_size)
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(health.router); app.include_router(analyze.router); app.include_router(support.router); app.include_router(simulations.router)

def error_response(request: Request, status: int, error: str, message: str):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(status_code=status, content={"error": error, "message": sanitize(message), "request_id": request_id}, headers={"X-Request-ID": request_id or ""})
@app.exception_handler(UpstreamError)
async def upstream_handler(request, exc): return error_response(request, exc.status_code, exc.category, str(exc))
@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc): return error_response(request, 422, "validation_error", "Request validation failed")
@app.exception_handler(StarletteHTTPException)
async def http_handler(request, exc): return error_response(request, exc.status_code, "bad_request" if exc.status_code < 500 else "http_error", str(exc.detail))
@app.exception_handler(Exception)
async def unexpected_handler(request, exc):
    logger.exception("unhandled application error", extra={"request_id":getattr(request.state,"request_id",None),"error_category":"internal_error"})
    return error_response(request, 500, "internal_error", "An unexpected internal error occurred")
@app.get("/")
async def root(): return {"name": settings.app_name, "version": settings.app_version, "docs": "/docs", "health": "/health/ready"}
@app.get("/api/v1/events")
async def events(): return {"source":"instance-local bounded history; not project-wide Cloud Logging", "events": list(recent_events)}
