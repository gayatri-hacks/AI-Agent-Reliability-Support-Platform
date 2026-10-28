import json, logging
from app.core.logging import JsonFormatter
def test_json_log_and_redaction():
    record=logging.LogRecord("x",20,"",0,"Bearer abcdef",(),None); record.request_id="request"
    data=json.loads(JsonFormatter().format(record)); assert data["request_id"] == "request" and "abcdef" not in data["message"]
