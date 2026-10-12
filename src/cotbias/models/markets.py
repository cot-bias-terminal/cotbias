from __future__ import annotations

from pydantic import BaseModel, Field


class MarketMetadata(BaseModel):
    symbol: str
    name: str
    cftc_code: str
    sector: str
    report_type: str
    has_options: bool
    available_reports: list[str] = Field(default_factory=list)


class MarketsResponse(BaseModel):
    markets: list[MarketMetadata]
