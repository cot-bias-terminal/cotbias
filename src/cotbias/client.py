from __future__ import annotations

import os
import httpx

from cotbias.config import DEFAULT_BASE_URL, DEFAULT_TIMEOUT_SEC
from cotbias.resources.inference import AsyncInferenceResource, InferenceResource
from cotbias.resources.markets import AsyncMarketsResource, MarketsResource
from cotbias.resources.screener import AsyncScreenerResource, ScreenerResource
from cotbias.resources.timeseries import AsyncTimeseriesResource, TimeseriesResource


class CotClient:
    """Synchronous client for Pandas, Jupyter, and quantitative pipelines."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SEC,
    ) -> None:
        resolved_key = api_key or os.getenv("COT_API_KEY")
        if not resolved_key:
            raise ValueError("API key missing. Pass  or set the  environment variable.")

        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": resolved_key,
                "User-Agent": "cotbias-python/0.1.0",
                "Accept": "application/json",
            },
            timeout=timeout,
            http2=True,
        )

        self.inference = InferenceResource(self._http)
        self.timeseries = TimeseriesResource(self._http)
        self.screener = ScreenerResource(self._http)
        self.markets = MarketsResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> CotClient:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()


class AsyncCotClient:
    """Asynchronous client for FastAPI, Discord/Telegram bots, and real-time screeners."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SEC,
    ) -> None:
        resolved_key = api_key or os.getenv("COT_API_KEY")
        if not resolved_key:
            raise ValueError("API key missing. Pass  or set the  environment variable.")

        self._http = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": resolved_key,
                "User-Agent": "cotbias-python-async/0.1.0",
                "Accept": "application/json",
            },
            timeout=timeout,
            http2=True,
        )

        self.inference = AsyncInferenceResource(self._http)
        self.timeseries = AsyncTimeseriesResource(self._http)
        self.screener = AsyncScreenerResource(self._http)
        self.markets = AsyncMarketsResource(self._http)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncCotClient:
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        await self.aclose()
