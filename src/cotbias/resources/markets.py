from __future__ import annotations

import httpx

from cotbias.exceptions import handle_error_response
from cotbias.models.markets import MarketMetadata, MarketsResponse


class MarketsResource:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(self, sector: str | None = None) -> list[MarketMetadata]:
        """List tracked markets across sectors with available CFTC report mappings."""
        params = {"sector": sector} if sector else {}
        resp = self._client.get("/markets", params=params)
        handle_error_response(resp)
        parsed = MarketsResponse.model_validate(resp.json())
        return parsed.markets


class AsyncMarketsResource:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def list(self, sector: str | None = None) -> list[MarketMetadata]:
        params = {"sector": sector} if sector else {}
        resp = await self._client.get("/markets", params=params)
        handle_error_response(resp)
        parsed = MarketsResponse.model_validate(resp.json())
        return parsed.markets
