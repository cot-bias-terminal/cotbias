"""Data models and type aliases for AI market positioning regimes and macro attribution."""

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
    """Macro and structural qualitative commentary synthesized by AI.

    Attributes:
        flow_dynamic_summary: Synthesis of weekly capital flow transitions across participant groups.
        macro_rationale: Underlying macro catalysts driving commercial and speculative positioning.
        structural_vulnerability: Potential vulnerabilities (e.g. illiquid basis, squeeze susceptibility).
    """

    model_config = ConfigDict(extra="allow")

    flow_dynamic_summary: str
    macro_rationale: str
    structural_vulnerability: str


class InferenceSchema(BaseModel):
    """Current week's AI positioning regime and macro attribution.

    Classification attributes use relaxed `str` types (backed by `Known*` typing aliases)
    and `extra="allow"` to prevent upstream schema drift from breaking client applications.

    Attributes:
        symbol: Asset ticker symbol (e.g. `'ES'`).
        report_date: Date of the corresponding CFTC report Tuesday (YYYY-MM-DD).
        ai_bias_score: High-level directional bias classification (`'Bullish'`, `'Bearish'`, etc.).
        regime_status: Structural alignment state (`'Bullish Alignment'`, `'Transitioning'`, etc.).
        primary_driver: Market participant group dominating the current weekly positioning shift.
        momentum: Open interest flow dynamic (`'New Longs'`, `'Short Covering'`, etc.).
        cot_positioning: Speculative vs Commercial divergence status.
        hedging_pressure: State of commercial hedging activity (`'Elevated'`, `'Conservative'`).
        historical_percentile: Long-term historical positioning percentile ranking.
        crowdedness_risk: Squeeze or liquidation risk assessment (`'High Liquidation Risk'`, etc.).
        smart_money_divergence: Aggressiveness of smart money accumulation/distribution.
        dumb_money_index: Speculative crowd sentiment index (`'Euphoria'`, `'Fear'`, `'Neutral'`).
        qualitative_attribution: In-depth commentary explaining the positioning drivers.
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
