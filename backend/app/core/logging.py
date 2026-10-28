import json
import logging
import re
import sys

SECRET_RE = re.compile(r"(?i)(bearer\s+|api[_-]?key[=:]\s*|token[=:]\s*)[^\s,]+")
def sanitize(value: str | None) -> str | None:
    if not value: return value
    return SECRET_RE.sub(r"\1[REDACTED]", value)[:512]

class JsonFormatter(logging.Formatter):
    def format(self, record):
        event = {"timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"), "severity": record.levelname, "message": sanitize(record.getMessage())}
        for key in ("request_id", "trace_id", "http_method", "endpoint", "status_code", "latency_ms", "service_name", "error_category", "error_message_sanitized", "logging.googleapis.com/trace"):
            if hasattr(record, key) and getattr(record, key) is not None: event[key] = getattr(record, key)
        return json.dumps(event, default=str)

def configure_logging():
    handler = logging.StreamHandler(sys.stdout); handler.setFormatter(JsonFormatter())
    logger = logging.getLogger("app"); logger.handlers = [handler]; logger.setLevel(logging.INFO); logger.propagate = False
    return logger
