import time, uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import get_settings
from app.core.logging import configure_logging, sanitize
from app.core.request_context import request_id_context, trace_id_context
logger = configure_logging()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        trace_header = request.headers.get("X-Cloud-Trace-Context", "")
        trace_id = trace_header.split("/", 1)[0]
        request.state.request_id = request_id
        tokens = (request_id_context.set(request_id), trace_id_context.set(trace_id))
        started = time.perf_counter(); status = 500; category = None
        try:
            if request.headers.get("content-length") and int(request.headers["content-length"]) > get_settings().max_request_bytes:
                from fastapi import HTTPException
                raise HTTPException(413, "Request body is too large")
            response = await call_next(request); status = response.status_code
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            category = getattr(exc, "category", "internal_error")
            raise
        finally:
            latency = int((time.perf_counter() - started) * 1000)
            extra = {"request_id": request_id, "trace_id": trace_id or None, "http_method": request.method, "endpoint": request.url.path, "status_code": status, "latency_ms": latency, "service_name": get_settings().service_name, "error_category": category}
            logger.info("request complete", extra=extra)
            request_id_context.reset(tokens[0]); trace_id_context.reset(tokens[1])
