import asyncio

import pytest
from app.core.errors import UpstreamTimeout
from app.core.retry import retry_transient


def test_retry_then_success():
    calls=0
    async def action():
        nonlocal calls; calls += 1
        if calls < 2: raise UpstreamTimeout("temporary")
        return "ok"
    assert asyncio.run(retry_transient(action, attempts=2, base_delay=0)) == "ok"

def test_retry_exhaustion():
    async def action(): raise UpstreamTimeout("temporary")
    with pytest.raises(UpstreamTimeout):
        asyncio.run(retry_transient(action, attempts=2, base_delay=0))
