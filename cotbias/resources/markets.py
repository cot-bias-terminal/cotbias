from typing import Optional
import httpx
from pydantic import BaseModel


class MarketMetadata(BaseModel):
    symbol: str
    name: str
    cftc_code: str
    sector: str
    report_type: str
    has_options: bool


class MarketsResource:
    def __init__(self, client: httpx.Client):
        self._client = client

    def list(self, sector: Optional[str] = None) -> list[MarketMetadata]:
        params = {"sector": sector} if sector else {}
        resp = self._client.get("/markets", params=params)
        resp.raise_for_status()
        return [MarketMetadata.model_validate(item) for item in resp.json().get("markets", [])]


class AsyncMarketsResource:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def list(self, sector: Optional[str] = None) -> list[MarketMetadata]:
        params = {"sector": sector} if sector else {}
        resp = await self._client.get("/markets", params=params)
        resp.raise_for_status()
        return [MarketMetadata.model_validate(item) for item in resp.json().get("markets", [])]