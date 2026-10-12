from __future__ import annotations

import httpx
import pytest
import respx
import pandas as pd
from cotbias import CotClient
from cotbias.exceptions import NotFoundError
from cotbias.models import TimeseriesResponse


@respx.mock
def test_timeseries_as_dataframe():
    mock_payload = {
        "symbol": "GC",
        "cftc_code": "088691",
        "contract_type": "futopt",
        "report": "legacy",
        "count": 2,
        "data": [
            {
                "report_date": "2026-03-31",
                "open_interest": 500000,
                "commercial_net": -180000,
                "cot_52w_commercial": 15.2,
            },
            {
                "report_date": "2026-04-07",
                "open_interest": 512400,
                "commercial_net": -184200,
                "cot_52w_commercial": 18.4,
            },
        ],
    }
    route = respx.get("https://api.cot-bias-terminal.com/v1/timeseries/GC").mock(
        return_value=httpx.Response(200, json=mock_payload)
    )

    with CotClient(api_key="cot_live_test") as cot:
        df = cot.timeseries.get("GC", contract_type="futopt", lookback_weeks=156, as_dataframe=True)

    assert route.called
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.loc["2026-04-07", "open_interest"] == 512400


@respx.mock
def test_timeseries_as_model():
    mock_payload = {
        "symbol": "GC",
        "cftc_code": "088691",
        "contract_type": "futopt",
        "report": "pro",
        "count": 1,
        "data": [
            {
                "report_date": "2026-04-07",
                "open_interest": 512400,
            }
        ],
    }
    respx.get("https://api.cot-bias-terminal.com/v1/timeseries/GC").mock(
        return_value=httpx.Response(200, json=mock_payload)
    )

    with CotClient(api_key="cot_live_test") as cot:
        res = cot.timeseries.get("GC", report="pro", as_dataframe=False)

    assert isinstance(res, TimeseriesResponse)
    assert res.symbol == "GC"
    assert res.report == "pro"
    assert len(res.data) == 1
    assert res.data[0].open_interest == 512400


@respx.mock
def test_timeseries_not_found_error():
    respx.get("https://api.cot-bias-terminal.com/v1/timeseries/UNKNOWN").mock(
        return_value=httpx.Response(
            404,
            json={
                "error": {
                    "code": "ASSET_NOT_FOUND",
                    "message": "Asset symbol not found",
                    "status": 404,
                }
            },
        )
    )

    with CotClient(api_key="cot_live_test") as cot:
        with pytest.raises(NotFoundError) as exc_info:
            cot.timeseries.get("UNKNOWN")
        assert exc_info.value.code == "ASSET_NOT_FOUND"
        assert exc_info.value.status_code == 404
