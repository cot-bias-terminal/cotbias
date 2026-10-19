"""Data models for multi-market positioning screeners."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ScreenerResultItem(BaseModel):
    """A matched market returned by a screener query.

    Attributes:
        symbol: Market ticker symbol.
        ai_bias_score: Directional bias classification.
        regime_status: Structural alignment regime.
        crowdedness_risk: Squeeze or liquidation risk.
        primary_driver: Dominant participant group.
        momentum: Open interest flow dynamic.
        cot_52w_commercial: 52-week normalized commercial COT Index.
    """

    model_config = ConfigDict(extra="allow")

    symbol: str
    ai_bias_score: str
    regime_status: str
    crowdedness_risk: str
    primary_driver: str
    momentum: str
    cot_52w_commercial: float | None = None


class ScreenerResponse(BaseModel):
    """Response payload containing matching screen results.

    Attributes:
        total_matches: Count of contracts matching the query filters.
        results: List of matched market items.
    """

    model_config = ConfigDict(extra="allow")

    total_matches: int
    results: list[ScreenerResultItem]
