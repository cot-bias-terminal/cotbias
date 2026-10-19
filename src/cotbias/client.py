from __future__ import annotations

import importlib.metadata
import os
import sys

import httpx

from cotbias.config import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT_SEC
from cotbias.resources.inference import AsyncInferenceResource, InferenceResource
from cotbias.resources.markets import AsyncMarketsResource, MarketsResource
from cotbias.resources.screener import AsyncScreenerResource, ScreenerResource
from cotbias.resources.timeseries import AsyncTimeseriesResource, TimeseriesResource
from cotbias.retry import AsyncRetryTransport, RetryTransport

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

try:
    __version__ = importlib.metadata.version("cotbias")
except (importlib.metadata.PackageNotFoundError, ValueError):
    __version__ = "0.2.0"


class CotClient:
    """Synchronous client for quantitative pipelines, analytics, and scripting."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SEC,
        max_retries: int = DEFAULT_MAX_RETRIES,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        resolved_key = api_key or os.getenv("COT_API_KEY")
        if not resolved_key:
            raise ValueError("API key missing. Pass api_key or set the COT_API_KEY environment variable.")

        raw_transport = transport or httpx.HTTPTransport(http2=True)
        final_transport = RetryTransport(raw_transport, max_retries=max_retries) if max_retries > 0 else raw_transport

        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": resolved_key,
                "User-Agent": f"cotbias-python/{__version__}",
                "Accept": "application/json",
            },
            timeout=timeout,
            transport=final_transport,
        )

        self.inference = InferenceResource(self._http)
        self.timeseries = TimeseriesResource(self._http)
        self.screener = ScreenerResource(self._http)
        self.markets = MarketsResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()


class AsyncCotClient:
    """Asynchronous client for FastAPI, async bots, and real-time screeners."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SEC,
        max_retries: int = DEFAULT_MAX_RETRIES,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        resolved_key = api_key or os.getenv("COT_API_KEY")
        if not resolved_key:
            raise ValueError("API key missing. Pass api_key or set the COT_API_KEY environment variable.")

        raw_transport = transport or httpx.AsyncHTTPTransport(http2=True)
        final_transport = (
            AsyncRetryTransport(raw_transport, max_retries=max_retries) if max_retries > 0 else raw_transport
        )

        self._http = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": resolved_key,
                "User-Agent": f"cotbias-python-async/{__version__}",
                "Accept": "application/json",
            },
            timeout=timeout,
            transport=final_transport,
        )

        self.inference = AsyncInferenceResource(self._http)
        self.timeseries = AsyncTimeseriesResource(self._http)
        self.screener = AsyncScreenerResource(self._http)
        self.markets = AsyncMarketsResource(self._http)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        await self.aclose()
