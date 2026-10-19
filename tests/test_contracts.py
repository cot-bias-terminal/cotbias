from __future__ import annotations

import json
from pathlib import Path

from cotbias.models.inference import InferenceSchema
from cotbias.models.markets import MarketsResponse
from cotbias.models.screener import ScreenerResponse
from cotbias.models.timeseries import TimeseriesResponse

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_contract_inference_fixture():
    with open(FIXTURES_DIR / "inference.json") as f:
        data = json.load(f)
    model = InferenceSchema.model_validate(data)
    assert model.symbol == "ES"
    assert model.ai_bias_score == "Bullish"
    assert model.qualitative_attribution.macro_rationale.startswith("Sustained corporate")
    # Verify extra="allow" preserves future backend fields
    assert model.custom_future_backend_field == "resilient_to_drift"


def test_contract_inference_schema_drift_resilience():
    """Verify that new or adjusted backend classifications do not cause ValidationError."""
    with open(FIXTURES_DIR / "inference.json") as f:
        data = json.load(f)

    # Simulate backend introducing new label variants
    data["ai_bias_score"] = "Ultra Bullish (New Label)"
    data["regime_status"] = "Dynamic Alignment"
    data["momentum"] = "Institutional Accumulation"

    model = InferenceSchema.model_validate(data)
    assert model.ai_bias_score == "Ultra Bullish (New Label)"
    assert model.regime_status == "Dynamic Alignment"
    assert model.momentum == "Institutional Accumulation"


def test_contract_markets_fixture():
    with open(FIXTURES_DIR / "markets.json") as f:
        data = json.load(f)
    model = MarketsResponse.model_validate(data)
    assert len(model.markets) == 2
    assert model.markets[0].symbol == "ES"
    assert model.markets[0].has_options is True


def test_contract_timeseries_fixture():
    with open(FIXTURES_DIR / "timeseries.json") as f:
        data = json.load(f)
    model = TimeseriesResponse.model_validate(data)
    assert model.symbol == "ES"
    assert model.count == 2
    assert model.data[1].open_interest == 2485000


def test_contract_screener_fixture():
    with open(FIXTURES_DIR / "screener.json") as f:
        data = json.load(f)
    model = ScreenerResponse.model_validate(data)
    assert model.total_matches == 2
    assert model.results[0].symbol == "ES"
    assert model.results[1].crowdedness_risk == "High Squeeze Risk"
