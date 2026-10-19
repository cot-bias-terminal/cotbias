from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

KnownAiBiasScore = Literal[
    "Strongly Bullish",
    "Bullish",
    "Neutral",
    "Bearish",
    "Strongly Bearish",
]

KnownRegimeStatus = Literal[
    "Bullish Alignment",
    "Bearish Alignment",
    "Neutral / Balanced",
    "Transitioning",
]

KnownPrimaryDriver = Literal[
    "Leveraged Funds",
    "Asset Managers",
    "Dealer",
    "Other Reportables",
    "Commercials",
    "Non-Reportables",
]

KnownMomentum = Literal[
    "New Longs (OI Expanding)",
    "Short Covering (OI Contracting)",
    "New Shorts (OI Expanding)",
    "Long Liquidation (OI Contracting)",
    "Stagnant",
]

KnownCrowdednessRisk = Literal[
    "High Liquidation Risk",
    "High Squeeze Risk",
    "Balanced",
]

KnownCotPositioning = Literal["Convergence", "Divergence"]
KnownHedgingPressure = Literal["Elevated", "Conservative"]
KnownSmartMoneyDivergence = Literal["Aggressive", "Conservative", "Neutral"]
KnownDumbMoneyIndex = Literal["Euphoria", "Fear", "Neutral"]


class QualitativeAttribution(BaseModel):
    model_config = ConfigDict(extra="allow")

    flow_dynamic_summary: str
    macro_rationale: str
    structural_vulnerability: str


class InferenceSchema(BaseModel):
    """Current week's AI positioning regime and macro attribution.

    Classification attributes use relaxed `str` types (backed by `Known*` typing aliases)
    and `extra="allow"` to prevent schema drift from breaking downstream applications.
    """

    model_config = ConfigDict(extra="allow")

    symbol: str
    report_date: str
    ai_bias_score: str
    regime_status: str
    primary_driver: str
    momentum: str
    cot_positioning: str
    hedging_pressure: str
    historical_percentile: str
    crowdedness_risk: str
    smart_money_divergence: str
    dumb_money_index: str
    qualitative_attribution: QualitativeAttribution
