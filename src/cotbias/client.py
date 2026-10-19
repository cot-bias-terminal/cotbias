"""Client implementations for the COT Bias Terminal API.

Provides both synchronous (:class:`CotClient`) and asynchronous
(:class:`AsyncCotClient`) clients configured with automatic retry logic,
HTTP/2 connection pooling, and resource-oriented API access.
"""

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
    __version__ = "0.2.2"


class CotClient:
    """Synchronous client for the COT Bias Terminal Quant API.

    Designed for analytical workflows, quantitative backtesting scripts,
    Jupyter notebooks, and standard synchronous Python applications.

    Attributes:
        timeseries: Access to historical weekly CFTC positioning timeseries.
        inference: Access to current week AI positioning regimes and attribution.
        screener: Cross-asset filtering across tracked commodities, equities, FX, and rates.
        markets: Catalog of supported contracts, CFTC codes, and metadata.

    Example:
        ```python
        from cotbias import CotClient

        with CotClient(api_key="cot_live_...") as client:
            snapshot = client.inference.get("ES")
            print(snapshot.ai_bias_score, snapshot.cot_positioning_regime)
        ```
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SEC,
        max_retries: int = DEFAULT_MAX_RETRIES,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        """Initialize the synchronous COT Bias client.

        Args:
            api_key: Quant tier API key. If not provided, resolves from the
                `COT_API_KEY` environment variable.
            base_url: API root endpoint URL. Defaults to the production API.
            timeout: Request timeout in seconds. Defaults to 30.0s.
            max_retries: Number of retry attempts on transient network errors
                or HTTP 5xx responses. Defaults to 3.
            transport: Optional custom HTTPX transport for proxies or custom SSL.

        Raises:
            ValueError: If no API key was provided or found in `COT_API_KEY`.
        """
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
        """Close the underlying HTTP client and connection pool."""
        self._http.close()

    def __enter__(self) -> Self:
        """Enter the runtime context and return the client instance."""
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Exit the runtime context and close open network connections."""
        self.close()


class AsyncCotClient:
    """Asynchronous client for the COT Bias Terminal Quant API.

    Designed for high-throughput asynchronous services, FastAPI backends,
    async trading engines, and event-driven screeners.

    Attributes:
        timeseries: Access to historical weekly CFTC positioning timeseries.
        inference: Access to current week AI positioning regimes and attribution.
        screener: Cross-asset filtering across tracked commodities, equities, FX, and rates.
        markets: Catalog of supported contracts, CFTC codes, and metadata.

    Example:
        ```python
        import asyncio
        from cotbias import AsyncCotClient

        async def main():
            async with AsyncCotClient() as client:
                data = await client.inference.get("CL")
                print(data.ai_bias_score)

        asyncio.run(main())
        ```
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SEC,
        max_retries: int = DEFAULT_MAX_RETRIES,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        """Initialize the asynchronous COT Bias client.

        Args:
            api_key: Quant tier API key. If not provided, resolves from the
                `COT_API_KEY` environment variable.
            base_url: API root endpoint URL. Defaults to the production API.
            timeout: Request timeout in seconds. Defaults to 30.0s.
            max_retries: Number of retry attempts on transient network errors
                or HTTP 5xx responses. Defaults to 3.
            transport: Optional custom HTTPX async transport for proxies or testing.

        Raises:
            ValueError: If no API key was provided or found in `COT_API_KEY`.
        """
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
        """Close the underlying asynchronous HTTP client and connection pool."""
        await self._http.aclose()

    async def __aenter__(self) -> Self:
        """Enter the async runtime context and return the client instance."""
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Exit the async runtime context and close open network connections."""
        await self.aclose()
