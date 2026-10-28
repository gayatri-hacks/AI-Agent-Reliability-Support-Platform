import asyncio, random
from collections.abc import Awaitable, Callable
from app.core.errors import UpstreamRateLimited, UpstreamTimeout, UpstreamUnavailable

RETRYABLE = (UpstreamRateLimited, UpstreamTimeout, UpstreamUnavailable)

async def retry_transient(operation: Callable[[], Awaitable[object]], attempts: int = 3, base_delay: float = .15):
    last_error = None
    for attempt in range(attempts):
        try:
            return await operation()
        except RETRYABLE as error:
            last_error = error
            if attempt == attempts - 1:
                raise
            await asyncio.sleep(min(2.0, base_delay * (2 ** attempt)) * (0.5 + random.random()))
    raise last_error  # pragma: no cover
