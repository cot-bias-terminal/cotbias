from __future__ import annotations

import httpx
import pytest
import respx
from cotbias import CotClient
from cotbias.exceptions import RateLimitExceededError
from cotbias.models import InferenceSchema


@respx.mock
def test_inference_success():
    mock_payload = {
        "symbol": "GC",
        "report_date": "2026-04-07",
        "ai_bias_score": "Bullish",
        "regime_status": "Bullish Alignment",
        "primary_driver": "Asset Managers",
        "momentum": "New Longs (OI Expanding)",
        "cot_positioning": "Convergence",
        "hedging_pressure": "Elevated",
        "historical_percentile": "Elevated (70-90%)",
        "crowdedness_risk": "Balanced",
        "smart_money_divergence": "Aggressive",
        "dumb_money_index": "Euphoria",
        "qualitative_attribution": {
            "flow_dynamic_summary": "Asset Managers added 12,400 contracts.",
            "macro_rationale": "Sovereign reserve accumulation.",
            "structural_vulnerability": "Speculative positioning elevated.",
        },
    }
    respx.get("https://api.cot-bias-terminal.com/v1/inference/GC").mock(
        return_value=httpx.Response(200, json=mock_payload)
    )

    with CotClient(api_key="cot_live_test") as cot:
        inf = cot.inference.get("GC")

    assert isinstance(inf, InferenceSchema)
    assert inf.symbol == "GC"
    assert inf.ai_bias_score == "Bullish"
    assert inf.qualitative_attribution.flow_dynamic_summary.startswith("Asset Managers")


@respx.mock
def test_inference_rate_limited():
    respx.get("https://api.cot-bias-terminal.com/v1/inference/GC").mock(
        return_value=httpx.Response(
            429,
            headers={"Retry-After": "45"},
            json={
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Minute limit reached",
                    "status": 429,
                }
            },
        )
    )

    with CotClient(api_key="cot_live_test") as cot:
        with pytest.raises(RateLimitExceededError) as exc_info:
            cot.inference.get("GC")
        assert exc_info.value.retry_after == 45
        assert exc_info.value.code == "RATE_LIMIT_EXCEEDED"
