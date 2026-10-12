from __future__ import annotations

from typing import Literal
from pydantic import BaseModel


class QualitativeAttribution(BaseModel):
    flow_dynamic_summary: str
    macro_rationale: str
    structural_vulnerability: str


class InferenceSchema(BaseModel):
    symbol: str
    report_date: str
    ai_bias_score: Literal[
        "Strongly Bullish",
        "Bullish",
        "Neutral",
        "Bearish",
        "Strongly Bearish",
    ]
    regime_status: Literal[
        "Bullish Alignment",
        "Bearish Alignment",
        "Neutral / Balanced",
        "Transitioning",
    ]
    primary_driver: Literal[
        "Leveraged Funds",
        "Asset Managers",
        "Dealer",
        "Other Reportables",
        "Commercials",
        "Non-Reportables",
    ]
    momentum: Literal[
        "New Longs (OI Expanding)",
        "Short Covering (OI Contracting)",
        "New Shorts (OI Expanding)",
        "Long Liquidation (OI Contracting)",
        "Stagnant",
    ]
    cot_positioning: Literal["Convergence", "Divergence"]
    hedging_pressure: Literal["Elevated", "Conservative"]
    historical_percentile: Literal[
        "Extreme Overbought (>90%)",
        "Elevated (70-90%)",
        "Neutral (30-70%)",
        "Depressed (10-30%)",
        "Extreme Oversold (<10%)",
    ]
    crowdedness_risk: Literal["High Liquidation Risk", "High Squeeze Risk", "Balanced"]
    smart_money_divergence: Literal["Aggressive", "Conservative", "Neutral"]
    dumb_money_index: Literal["Euphoria", "Fear", "Neutral"]
    qualitative_attribution: QualitativeAttribution
