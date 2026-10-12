from __future__ import annotations

import httpx
import respx
from cotbias import CotClient
from cotbias.models import MarketMetadata


@respx.mock
def test_markets_list():
    mock_payload = {
        "markets": [
            {
                "symbol": "GC",
                "name": "GOLD - COMMODITY EXCHANGE INC.",
                "cftc_code": "088691",
                "sector": "METALS",
                "report_type": "disaggregated",
                "has_options": True,
                "available_reports": ["legacy", "disaggregated", "pro"],
            }
        ]
    }
    respx.get("https://api.cot-bias-terminal.com/v1/markets", params={"sector": "METALS"}).mock(
        return_value=httpx.Response(200, json=mock_payload)
    )

    with CotClient(api_key="cot_live_test") as cot:
        markets = cot.markets.list(sector="METALS")

    assert len(markets) == 1
    m = markets[0]
    assert isinstance(m, MarketMetadata)
    assert m.symbol == "GC"
    assert m.has_options is True
    assert "disaggregated" in m.available_reports
