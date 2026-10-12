from __future__ import annotations

import httpx
import pytest
import respx
from cotbias import AsyncCotClient


@pytest.mark.asyncio
@respx.mock
async def test_async_timeseries_and_inference():
    respx.get("https://api.cot-bias-terminal.com/v1/timeseries/GC").mock(
        return_value=httpx.Response(
            200,
            json={
                "symbol": "GC",
                "cftc_code": "088691",
                "contract_type": "futopt",
                "report": "legacy",
                "count": 1,
                "data": [{"report_date": "2026-04-07", "open_interest": 500000}],
            },
        )
    )
    respx.get("https://api.cot-bias-terminal.com/v1/inference/GC").mock(
        return_value=httpx.Response(
            200,
            json={
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
                    "flow_dynamic_summary": "Asset Managers expanding.",
                    "macro_rationale": "Macro hedging.",
                    "structural_vulnerability": "Balanced risk.",
                },
            },
        )
    )

    async with AsyncCotClient(api_key="cot_live_test") as cot:
        df = await cot.timeseries.get("GC")
        inf = await cot.inference.get("GC")

    assert len(df) == 1
    assert inf.ai_bias_score == "Bullish"
