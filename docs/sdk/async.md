# Asynchronous Client (`AsyncCotClient`)

The **asynchronous client** (`AsyncCotClient`) provides high-throughput, non-blocking network I/O powered by `httpx.AsyncClient`.

It is designed for real-time market dashboards, FastAPI or Quart backends, algorithmic trading bots, and high-performance quantitative data ingestion pipelines.

---

## ⚡ Quick Example

```python
import asyncio
from cotbias import AsyncCotClient


async def main():
    async with AsyncCotClient() as client:
        # Fetch multiple markets concurrently
        es_task = client.inference.get("ES")
        nq_task = client.inference.get("NQ")
        cl_task = client.inference.get("CL")

        es, nq, cl = await asyncio.gather(es_task, nq_task, cl_task)

        print(f"ES: {es.ai_bias_score} | NQ: {nq.ai_bias_score} | CL: {cl.ai_bias_score}")


asyncio.run(main())
```

---

## 🚀 Concurrent Batch Ingestion

When pulling timeseries or inference for dozens of contracts simultaneously, `asyncio.gather` dramatically reduces total fetch time:

```python
import asyncio
import pandas as pd
from cotbias import AsyncCotClient

SYMBOLS = ["ES", "NQ", "YM", "RTY", "GC", "SI", "CL", "NG", "6E", "6J", "ZB", "ZN"]


async def fetch_timeseries(client: AsyncCotClient, symbol: str) -> tuple[str, pd.DataFrame]:
    df = await client.timeseries.get(symbol, lookback_weeks=52, as_dataframe=True)
    return symbol, df


async def main():
    async with AsyncCotClient() as client:
        tasks = [fetch_timeseries(client, sym) for sym in SYMBOLS]
        results = await asyncio.gather(*tasks)

    for symbol, df in results:
        latest = df.iloc[-1]
        print(f"{symbol:<4}: 52w COT Index = {latest['cot_52w_commercial']:.1f}")


asyncio.run(main())
```

---

## 🚦 Rate Limit Protection with Semaphores

To avoid overwhelming local network sockets or triggering transient rate limit spikes when querying hundreds of records, bound your concurrency using `asyncio.Semaphore`:

```python
import asyncio
from cotbias import AsyncCotClient

SEMAPHORE_LIMIT = 5  # Max 5 simultaneous HTTP requests


async def worker(sem: asyncio.Semaphore, client: AsyncCotClient, symbol: str):
    async with sem:
        return await client.inference.get(symbol)


async def main():
    sem = asyncio.Semaphore(SEMAPHORE_LIMIT)
    async with AsyncCotClient() as client:
        all_markets = await client.markets.list()
        symbols = [m.symbol for m in all_markets]

        tasks = [worker(sem, client, sym) for sym in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = [r for r in results if not isinstance(r, Exception)]
    print(f"Successfully processed {len(successes)} / {len(symbols)} markets.")


asyncio.run(main())
```

---

## 🌐 FastAPI Integration Example

In modern web applications, instantiate a shared `AsyncCotClient` within the application lifespan:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from cotbias import AsyncCotClient

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create client pool
    state["cot_client"] = AsyncCotClient()
    yield
    # Shutdown: close connections cleanly
    await state["cot_client"].aclose()


app = FastAPI(lifespan=lifespan)


def get_cot_client() -> AsyncCotClient:
    return state["cot_client"]


@app.get("/api/market/{symbol}")
async def get_market_analysis(symbol: str, client: AsyncCotClient = Depends(get_cot_client)):
    regime = await client.inference.get(symbol)
    return {
        "symbol": regime.symbol,
        "bias": regime.ai_bias_score,
        "regime": regime.regime_status,
        "rationale": regime.qualitative_attribution.macro_rationale,
    }
```
