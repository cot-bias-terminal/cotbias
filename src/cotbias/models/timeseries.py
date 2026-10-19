"""Data models for weekly Commitment of Traders historical timeseries."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TimeseriesRow(BaseModel):
    """A single weekly report row in the positioning timeseries.

    Attributes:
        report_date: Date of the CFTC Tuesday report (YYYY-MM-DD).
        open_interest: Aggregate total open interest across all participants.
        delta_open_interest: Week-over-week change in aggregate open interest.
        commercial_long: Commercial / Producer-Merchant long contracts.
        commercial_short: Commercial / Producer-Merchant short contracts.
        commercial_net: Commercial net positioning (long minus short).
        commercial_net_pct_oi: Commercial net position as percentage of open interest.
        noncommercial_net: Non-Commercial / Speculative net positioning.
        noncommercial_net_pct_oi: Speculative net position as percentage of open interest.
        cot_52w_commercial: 52-week normalized COT Index (0 to 100).
        z_score_156w_commercial: 3-year rolling Z-score of commercial net positioning.
        dumb_money_index: Dumb money positioning index.
        smart_money_divergence_index: Indicator of divergence between smart and dumb money.
        commercial_hedging_pressure: Institutional commercial hedging pressure ratio.
        conc_top4_net_short: Concentration ratio of the 4 largest net short traders.
    """

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
    """Response payload containing metadata and historical positioning rows.

    Attributes:
        symbol: Ticker symbol (e.g. `'ES'`).
        cftc_code: CFTC commodity identification code.
        contract_type: Position breakdown type (`'fut'`, `'futopt'`, `'opt'`).
        report: CFTC report family (`'legacy'`, `'disaggregated'`, `'tff'`, `'supplemental'`).
        count: Number of weekly records returned.
        data: List of weekly positioning rows in chronological order.
    """

    model_config = ConfigDict(extra="allow")

    symbol: str
    cftc_code: str
    contract_type: str
    report: str
    count: int
    data: list[TimeseriesRow]
