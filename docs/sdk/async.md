---
status: stub
---

# Asynchronous Client (`AsyncCotClient`)

High-throughput, non-blocking asynchronous client powered by `httpx.AsyncClient` for high-frequency workflows, dashboards, and background workers.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Quick Reference

```python
import asyncio
from cotbias import AsyncCotClient


async def main():
    async with AsyncCotClient() as client:
        # Fetch multiple markets concurrently
        es_task = client.timeseries.get("ES", lookback_weeks=10)
        gc_task = client.timeseries.get("GC", lookback_weeks=10)
        es, gc = await asyncio.gather(es_task, gc_task)


asyncio.run(main())
```

## Roadmap & Upcoming Content
- [ ] Concurrent batch fetching patterns with `asyncio.gather` and task pools.
- [ ] Async context manager lifecycle.
- [ ] Integration with FastAPI, Quart, and Celery workers.
