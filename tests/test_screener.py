from __future__ import annotations

import httpx
import pandas as pd
import respx

from cotbias import CotClient
from cotbias.models import ScreenerResponse


@respx.mock
def test_screener_as_dataframe():
    mock_payload = {
        "total_matches": 1,
        "results": [
            {
                "symbol": "GC",
                "ai_bias_score": "Bullish",
                "regime_status": "Bullish Alignment",
                "crowdedness_risk": "Balanced",
                "primary_driver": "Asset Managers",
                "momentum": "New Longs (OI Expanding)",
                "cot_52w_commercial": 18.4,
            }
        ],
    }
    respx.get(
        "https://api.cot-bias-terminal.com/v1/screener",
        params={"ai_bias_score": "Bullish"},
    ).mock(return_value=httpx.Response(200, json=mock_payload))

    with CotClient(api_key="cot_live_test") as cot:
        df = cot.screener.scan(ai_bias_score="Bullish", as_dataframe=True)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["symbol"] == "GC"


@respx.mock
def test_screener_as_model():
    mock_payload = {
        "total_matches": 1,
        "results": [
            {
                "symbol": "GC",
                "ai_bias_score": "Bullish",
                "regime_status": "Bullish Alignment",
                "crowdedness_risk": "Balanced",
                "primary_driver": "Asset Managers",
                "momentum": "New Longs (OI Expanding)",
                "cot_52w_commercial": 18.4,
            }
        ],
    }
    respx.get("https://api.cot-bias-terminal.com/v1/screener").mock(return_value=httpx.Response(200, json=mock_payload))

    with CotClient(api_key="cot_live_test") as cot:
        res = cot.screener.scan(as_dataframe=False)

    assert isinstance(res, ScreenerResponse)
    assert res.total_matches == 1
    assert res.results[0].symbol == "GC"
