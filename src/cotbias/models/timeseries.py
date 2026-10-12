from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TimeseriesRow(BaseModel):
    model_config = ConfigDict(extra="allow")

    report_date: str
    open_interest: int | None = None
    delta_open_interest: int | None = None
    commercial_long: int | None = None
    commercial_short: int | None = None
    commercial_net: int | None = None
    commercial_net_pct_oi: float | None = None
    noncommercial_net: int | None = None
    noncommercial_net_pct_oi: float | None = None
    cot_52w_commercial: float | None = None
    z_score_156w_commercial: float | None = None
    dumb_money_index: float | None = None
    smart_money_divergence_index: float | None = None
    commercial_hedging_pressure: float | None = None
    conc_top4_net_short: float | None = None


class TimeseriesResponse(BaseModel):
    symbol: str
    cftc_code: str
    contract_type: str
    report: str
    count: int
    data: list[TimeseriesRow]
