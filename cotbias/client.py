import os
from typing import Optional
import httpx

from cotbias.resources.inference import AsyncInferenceResource, InferenceResource
from cotbias.resources.markets import AsyncMarketsResource, MarketsResource
from cotbias.resources.screener import AsyncScreenerResource, ScreenerResource
from cotbias.resources.timeseries import AsyncTimeseriesResource, TimeseriesResource


DEFAULT_BASE_URL = "https://api.cotbiasterminal.com/v1"


class CotClient:
    """Synchronous client for Pandas, Jupyter, and quantitative workflows."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 15.0,
    ):
        resolved_key = api_key or os.getenv("COT_API_KEY")
        if not resolved_key:
            raise ValueError(
                "API key missing. Pass `api_key` explicitly or set the `COT_API_KEY` environment variable."
            )

        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": resolved_key,
                "User-Agent": "cotbias-python/1.0.0",
                "Accept": "application/json",
            },
            timeout=timeout,
            http2=True,
        )

        # Expose sub-resources
        self.inference = InferenceResource(self._http)
        self.timeseries = TimeseriesResource(self._http)
        self.screener = ScreenerResource(self._http)
        self.markets = MarketsResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncCotClient:
    """Asynchronous client for MCP servers, bots, and FastAPI backends."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 15.0,
    ):
        resolved_key = api_key or os.getenv("COT_API_KEY")
        if not resolved_key:
            raise ValueError(
                "API key missing. Pass `api_key` explicitly or set the `COT_API_KEY` environment variable."
            )

        self._http = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": resolved_key,
                "User-Agent": "cotbias-python-async/1.0.0",
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()