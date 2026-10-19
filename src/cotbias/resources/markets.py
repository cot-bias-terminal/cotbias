"""Markets resource endpoint for querying the catalog of tracked CFTC futures contracts."""

from __future__ import annotations

import httpx

from cotbias.exceptions import handle_error_response
from cotbias.models.markets import MarketMetadata, MarketsResponse


class MarketsResource:
    """Synchronous resource for querying the catalog of tracked futures contracts."""

    def __init__(self, client: httpx.Client) -> None:
        """Initialize the markets resource with an active HTTP client.

        Args:
            client: Active synchronous HTTP client session.
        """
        self._client = client

    def list(self, sector: str | None = None) -> list[MarketMetadata]:
        """List tracked futures contracts with sector and CFTC report mappings.

        Args:
            sector: Optional sector filter: `'Commodity'`, `'Equity'`, `'FX'`, or `'Rates'`.
                If omitted, returns all tracked contracts.

        Returns:
            A list of :class:`~cotbias.models.markets.MarketMetadata` objects detailing
            symbol, descriptive name, CFTC commodity code, sector, and supported report types.

        Raises:
            AuthenticationError: If API key is missing or invalid (HTTP 401).
            PermissionDeniedError: If account tier lacks access (HTTP 403).
            RateLimitExceededError: If daily request quota is exceeded (HTTP 429).
            ServerError: If upstream COT Bias servers return an error (HTTP 5xx).
            CotApiError: Base exception for any unexpected API errors.

        Example:
            ```python
            from cotbias import CotClient

            client = CotClient()
            fx_markets = client.markets.list(sector="FX")
            for m in fx_markets:
                print(f"{m.symbol} ({m.name}): CFTC #{m.cftc_code}")
            ```
        """
        params = {"sector": sector} if sector else {}
        resp = self._client.get("/markets", params=params)
        handle_error_response(resp)
        parsed = MarketsResponse.model_validate(resp.json())
        return parsed.markets


class AsyncMarketsResource:
    """Asynchronous resource for querying the catalog of tracked futures contracts."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        """Initialize the async markets resource with an active async HTTP client.

        Args:
            client: Active asynchronous HTTP client session.
        """
        self._client = client

    async def list(self, sector: str | None = None) -> list[MarketMetadata]:
        """List tracked futures contracts asynchronously.

        Args:
            sector: Optional sector filter: `'Commodity'`, `'Equity'`, `'FX'`, or `'Rates'`.
                If omitted, returns all tracked contracts.

        Returns:
            A list of :class:`~cotbias.models.markets.MarketMetadata` objects detailing
            symbol, descriptive name, CFTC commodity code, sector, and supported report types.

        Raises:
            AuthenticationError: If API key is missing or invalid (HTTP 401).
            PermissionDeniedError: If account tier lacks access (HTTP 403).
            RateLimitExceededError: If daily request quota is exceeded (HTTP 429).
            ServerError: If upstream COT Bias servers return an error (HTTP 5xx).
            CotApiError: Base exception for any unexpected API errors.

        Example:
            ```python
            import asyncio
            from cotbias import AsyncCotClient

            async def main():
                async with AsyncCotClient() as client:
                    all_markets = await client.markets.list()
                    print(f"Total contracts tracked: {len(all_markets)}")

            asyncio.run(main())
            ```
        """
        params = {"sector": sector} if sector else {}
        resp = await self._client.get("/markets", params=params)
        handle_error_response(resp)
        parsed = MarketsResponse.model_validate(resp.json())
        return parsed.markets
