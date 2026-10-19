"""Data models for market contract catalogs and CFTC report mappings."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MarketMetadata(BaseModel):
    """Metadata describing a tracked futures contract.

    Attributes:
        symbol: Ticker symbol (e.g. `'ES'`, `'GC'`).
        name: Full contract description name.
        cftc_code: Official CFTC commodity code.
        sector: Asset class sector (`'Commodity'`, `'Equity'`, `'FX'`, `'Rates'`).
        report_type: Default report type.
        has_options: Whether combined options delta data is available.
        available_reports: List of CFTC report families published for this market.
    """

    model_config = ConfigDict(extra="allow")

    symbol: str
    name: str
    cftc_code: str
    sector: str
    report_type: str
    has_options: bool
    available_reports: list[str] = Field(default_factory=list)


class MarketsResponse(BaseModel):
    """Response payload containing a list of market metadata items.

    Attributes:
        markets: List of tracked market contracts.
    """

    model_config = ConfigDict(extra="allow")

    markets: list[MarketMetadata]
