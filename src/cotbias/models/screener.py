from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ScreenerResultItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    ai_bias_score: str
    regime_status: str
    crowdedness_risk: str
    primary_driver: str
    momentum: str
    cot_52w_commercial: float | None = None


class ScreenerResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    total_matches: int
    results: list[ScreenerResultItem]
