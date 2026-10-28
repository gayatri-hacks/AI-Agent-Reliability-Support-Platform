import pytest
from app.core.errors import UpstreamTimeout
from app.core.retry import retry_transient
@pytest.mark.asyncio
async def test_retry_then_success():
    calls=0
    async def action():
        nonlocal calls; calls += 1
        if calls < 2: raise UpstreamTimeout("temporary")
        return "ok"
    assert await retry_transient(action, attempts=2, base_delay=0) == "ok"
@pytest.mark.asyncio
async def test_retry_exhaustion():
    async def action(): raise UpstreamTimeout("temporary")
    with pytest.raises(UpstreamTimeout): await retry_transient(action, attempts=2, base_delay=0)
