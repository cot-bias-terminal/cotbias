from __future__ import annotations

import json
import subprocess
import sys

import httpx
import pytest
import respx

from cotbias.mcp.server import create_server


@pytest.fixture
def mcp_server():
    return create_server(api_key="cot_live_test_mcp", enable_cache=True)


@respx.mock
async def test_mcp_list_markets(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        return_value=httpx.Response(
            200,
            json={
                "markets": [
                    {
                        "symbol": "ES",
                        "name": "E-MINI S&P 500",
                        "cftc_code": "13874+",
                        "sector": "Equity",
                        "report_type": "legacy",
                        "has_options": True,
                        "available_reports": ["legacy"],
                    }
                ]
            },
        )
    )

    result = await mcp_server.call_tool("list_markets", {})
    assert not result.is_error
    data = result.structured_content
    assert data["total_markets"] == 1
    assert data["markets"][0]["symbol"] == "ES"
    assert data["cached"] is False

    # Second call should hit in-memory cache without hitting network
    result_cached = await mcp_server.call_tool("list_markets", {})
    assert result_cached.structured_content["cached"] is True


@respx.mock
async def test_mcp_get_ai_inference(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/inference/ES").mock(
        return_value=httpx.Response(
            200,
            json={
                "symbol": "ES",
                "report_date": "2026-10-13",
                "ai_bias_score": "Bullish",
                "regime_status": "Bullish Alignment",
                "primary_driver": "Asset Managers",
                "momentum": "New Longs (OI Expanding)",
                "cot_positioning": "Convergence",
                "hedging_pressure": "Conservative",
                "historical_percentile": "Elevated (70-90%)",
                "crowdedness_risk": "Balanced",
                "smart_money_divergence": "Aggressive",
                "dumb_money_index": "Euphoria",
                "qualitative_attribution": {
                    "flow_dynamic_summary": "Net longs expanded.",
                    "macro_rationale": "Strong macro tailwinds.",
                    "structural_vulnerability": "Low.",
                },
            },
        )
    )

    result = await mcp_server.call_tool("get_ai_inference", {"symbol": "es"})
    assert not result.is_error
    data = result.structured_content
    assert data["symbol"] == "ES"
    assert data["ai_bias_score"] == "Bullish"
    assert data["cached"] is False


@respx.mock
async def test_mcp_get_timeseries(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/timeseries/GC").mock(
        return_value=httpx.Response(
            200,
            json={
                "symbol": "GC",
                "cftc_code": "088691",
                "contract_type": "futopt",
                "report": "legacy",
                "count": 1,
                "data": [
                    {
                        "report_date": "2026-10-13",
                        "open_interest": 500000,
                        "delta_open_interest": 10000,
                        "commercial_net": -150000,
                        "commercial_net_pct_oi": -30.0,
                        "noncommercial_net": 120000,
                        "noncommercial_net_pct_oi": 24.0,
                        "cot_52w_commercial": 80.0,
                        "z_score_156w_commercial": 1.2,
                        "dumb_money_index": 65.0,
                        "smart_money_divergence_index": 70.0,
                        "commercial_hedging_pressure": 0.35,
                    }
                ],
            },
        )
    )

    result = await mcp_server.call_tool("get_timeseries", {"symbol": "GC", "lookback_weeks": 26})
    assert not result.is_error
    data = result.structured_content
    assert data["symbol"] == "GC"
    assert data["count"] == 1
    assert data["data"][0]["open_interest"] == 500000


@respx.mock
async def test_mcp_scan_markets(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/screener").mock(
        return_value=httpx.Response(
            200,
            json={
                "total_matches": 1,
                "results": [
                    {
                        "symbol": "CL",
                        "ai_bias_score": "Bearish",
                        "regime_status": "Bearish Alignment",
                        "crowdedness_risk": "High Liquidation Risk",
                        "primary_driver": "Leveraged Funds",
                        "momentum": "Long Liquidation (OI Contracting)",
                        "cot_52w_commercial": 12.5,
                    }
                ],
            },
        )
    )

    result = await mcp_server.call_tool("scan_markets", {"crowdedness_risk": "High Liquidation Risk"})
    assert not result.is_error
    data = result.structured_content
    assert data["total_matches"] == 1
    assert data["results"][0]["symbol"] == "CL"


@respx.mock
async def test_mcp_get_market_snapshot(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/inference/ES").mock(
        return_value=httpx.Response(
            200,
            json={
                "symbol": "ES",
                "report_date": "2026-10-13",
                "ai_bias_score": "Bullish",
                "regime_status": "Bullish Alignment",
                "primary_driver": "Asset Managers",
                "momentum": "New Longs (OI Expanding)",
                "cot_positioning": "Convergence",
                "hedging_pressure": "Conservative",
                "historical_percentile": "Elevated (70-90%)",
                "crowdedness_risk": "Balanced",
                "smart_money_divergence": "Aggressive",
                "dumb_money_index": "Euphoria",
                "qualitative_attribution": {
                    "flow_dynamic_summary": "Net longs expanded.",
                    "macro_rationale": "Macro strength.",
                    "structural_vulnerability": "Low.",
                },
            },
        )
    )
    respx.get("https://api.cot-bias-terminal.com/v1/timeseries/ES").mock(
        return_value=httpx.Response(
            200,
            json={
                "symbol": "ES",
                "cftc_code": "13874+",
                "contract_type": "futopt",
                "report": "legacy",
                "count": 1,
                "data": [
                    {
                        "report_date": "2026-10-13",
                        "open_interest": 2400000,
                        "delta_open_interest": 10000,
                        "commercial_net": -50000,
                        "commercial_net_pct_oi": -2.0,
                        "noncommercial_net": 40000,
                        "noncommercial_net_pct_oi": 1.6,
                        "cot_52w_commercial": 70.0,
                        "z_score_156w_commercial": 0.8,
                        "dumb_money_index": 75.0,
                        "smart_money_divergence_index": 60.0,
                        "commercial_hedging_pressure": 0.4,
                    }
                ],
            },
        )
    )

    result = await mcp_server.call_tool("get_market_snapshot", {"symbol": "ES"})
    assert not result.is_error
    data = result.structured_content
    assert data["symbol"] == "ES"
    assert "inference" in data
    assert "recent_positioning_trend" in data
    assert len(data["recent_positioning_trend"]) == 1


@respx.mock
async def test_mcp_error_envelope_401(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        return_value=httpx.Response(
            401,
            json={"error": {"code": "INVALID_API_KEY", "message": "API key invalid or expired."}},
        )
    )

    result = await mcp_server.call_tool("list_markets", {})
    data = result.structured_content
    assert "error" in data
    assert data["error"]["code"] == "INVALID_API_KEY"
    assert "COT_API_KEY" in data["error"]["hint"]


@respx.mock
async def test_mcp_error_envelope_403(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/inference/ES").mock(
        return_value=httpx.Response(
            403,
            json={"error": {"code": "TIER_RESTRICTED", "message": "Quant subscription required."}},
        )
    )

    result = await mcp_server.call_tool("get_ai_inference", {"symbol": "ES"})
    data = result.structured_content
    assert "error" in data
    assert "Quant tier subscription is required" in data["error"]["hint"]


@respx.mock
async def test_mcp_error_envelope_404(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/inference/UNKNOWN").mock(
        return_value=httpx.Response(
            404,
            json={"error": {"code": "ASSET_NOT_FOUND", "message": "Asset symbol not found."}},
        )
    )

    result = await mcp_server.call_tool("get_ai_inference", {"symbol": "UNKNOWN"})
    data = result.structured_content
    assert "error" in data
    assert "list_markets" in data["error"]["hint"]


@respx.mock
async def test_mcp_error_envelope_429(mcp_server):
    respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        return_value=httpx.Response(
            429,
            json={"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Quota exceeded."}},
            headers={"Retry-After": "120"},
        )
    )

    result = await mcp_server.call_tool("list_markets", {})
    data = result.structured_content
    assert "error" in data
    assert data["error"]["retry_after"] == 120
    assert "120s" in data["error"]["hint"]


async def test_mcp_resource(mcp_server):
    contents = await mcp_server.read_resource("cot://markets")
    assert len(contents) > 0
    assert contents[0].mime_type == "application/json"


async def test_mcp_prompts(mcp_server):
    briefing = await mcp_server.get_prompt("cot-macro-briefing", {})
    assert "scan_markets" in briefing.messages[0].content.text

    deep_dive = await mcp_server.get_prompt("cot-market-deep-dive", {"symbol": "GC"})
    assert "GC" in deep_dive.messages[0].content.text
    assert "get_market_snapshot" in deep_dive.messages[0].content.text


def test_mcp_stdio_cli_protocol():
    """Verify that the cotbias-mcp CLI can start in stdio mode and process JSON-RPC messages."""
    proc = subprocess.Popen(
        [sys.executable, "-m", "cotbias.mcp.server", "--transport", "stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Send initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"},
        },
    }

    try:
        assert proc.stdin is not None
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()

        assert proc.stdout is not None
        response_line = proc.stdout.readline()
        assert response_line, "Expected JSON-RPC response from cotbias-mcp"
        resp = json.loads(response_line)
        assert resp.get("id") == 1
        assert "serverInfo" in resp.get("result", {})
        assert resp["result"]["serverInfo"]["name"] == "cotbias-mcp"
    finally:
        proc.terminate()
        proc.wait(timeout=5)
