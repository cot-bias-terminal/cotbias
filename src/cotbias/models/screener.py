from __future__ import annotations

from pydantic import BaseModel


class ScreenerResultItem(BaseModel):
    symbol: str
    ai_bias_score: str
    regime_status: str
    crowdedness_risk: str
    primary_driver: str
    momentum: str
    cot_52w_commercial: float | None = None


class ScreenerResponse(BaseModel):
    total_matches: int
    results: list[ScreenerResultItem]
