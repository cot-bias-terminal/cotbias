from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from typing import Any

from mcp.server.mcpserver import MCPServer

from cotbias.client import AsyncCotClient
from cotbias.config import DEFAULT_BASE_URL
from cotbias.exceptions import (
    AuthenticationError,
    CotApiError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitExceededError,
    ServerError,
)

logger = logging.getLogger("cotbias.mcp")


class TTLCache:
    """Thread/asyncio-safe lightweight in-memory TTL cache to safeguard Quant API quota."""

    def __init__(self) -> None:
        self._cache: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        if key in self._cache:
            ts, val = self._cache[key]
            if time.monotonic() < ts:
                return val
            del self._cache[key]
        return None

    def set(self, key: str, val: Any, ttl_seconds: float) -> None:
        self._cache[key] = (time.monotonic() + ttl_seconds, val)

    def clear(self) -> None:
        self._cache.clear()


def _format_error(err: CotApiError, hint_symbol: str | None = None) -> dict[str, Any]:
    """Map CotApiError to a clear, actionable error envelope for the LLM."""
    hint = "An error occurred while calling the COT Bias Quant API."
    if isinstance(err, AuthenticationError):
        hint = (
            "API key missing, invalid, or expired. Please set the COT_API_KEY environment "
            "variable with a valid Quant tier key from COT Bias Terminal."
        )
    elif isinstance(err, PermissionDeniedError):
        hint = "Permission denied. Quant tier subscription is required to access the API and MCP server tools."
    elif isinstance(err, NotFoundError):
        target = f"'{hint_symbol}' " if hint_symbol else ""
        hint = (
            f"Asset {target}not found in CFTC COT universe. Call 'list_markets' to check "
            "supported symbols (e.g., 'ES', 'NQ', 'GC', 'CL', '6E', 'ZB')."
        )
    elif isinstance(err, RateLimitExceededError):
        retry_sec = getattr(err, "retry_after", 60)
        hint = (
            f"API quota or rate limit exceeded. Please wait {retry_sec}s before retrying. "
            "Quant tier allows up to 2,000 requests/day."
        )
    elif isinstance(err, ServerError):
        hint = "COT Bias API backend service is temporarily unavailable. Please retry shortly."

    return {
        "error": {
            "code": err.code or err.__class__.__name__,
            "status_code": err.status_code,
            "message": str(err.message),
            "hint": hint,
            "retry_after": getattr(err, "retry_after", None),
        }
    }


def create_server(
    api_key: str | None = None,
    base_url: str = DEFAULT_BASE_URL,
    enable_cache: bool = True,
) -> MCPServer:
    """Build and configure the COT Bias MCPServer instance."""
    server = MCPServer(
        name="cotbias-mcp",
        version="0.2.1",
        instructions=(
            "COT Bias MCP Server provides quantitative CFTC Commitments of Traders (COT) "
            "data, institutional positioning regimes, and AI macro attributions across "
            "Commodities, Equities, FX, and Fixed Income. Use 'list_markets' to explore "
            "tracked contracts, 'get_market_snapshot' for full asset synthesis, and "
            "'scan_markets' to screen for institutional extremes and crowdedness."
        ),
    )

    cache = TTLCache() if enable_cache else None

    # Lazy client initialization
    _client: AsyncCotClient | None = None

    def get_client() -> AsyncCotClient:
        nonlocal _client
        if _client is None:
            _client = AsyncCotClient(
                api_key=api_key or os.getenv("COT_API_KEY"),
                base_url=base_url,
                timeout=15.0,
            )
        return _client

    # --------------------------------------------------------------------------
    # TOOLS
    # --------------------------------------------------------------------------

    @server.tool(
        name="list_markets",
        description=(
            "List all CFTC COT tracked futures/options contracts with symbol, sector "
            "(Equity, FX, Commodity, Rates), available report types, and options support."
        ),
    )
    async def list_markets(sector: str | None = None) -> dict[str, Any]:
        cache_key = f"markets:{sector or 'all'}"
        if cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return {**cached, "cached": True}

        try:
            client = get_client()
            markets = await client.markets.list(sector=sector)
            data = [m.model_dump() for m in markets]
            result = {
                "sector_filter": sector,
                "total_markets": len(data),
                "markets": data,
                "cached": False,
            }
            if cache:
                cache.set(cache_key, result, ttl_seconds=300.0)
            return result
        except CotApiError as e:
            sys.stderr.write(f"[cotbias-mcp] list_markets error: {e}\n")
            return _format_error(e)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[cotbias-mcp] list_markets unexpected error: {e}\n")
            return {"error": {"code": "UNEXPECTED_ERROR", "message": str(e)}}

    @server.tool(
        name="get_ai_inference",
        description=(
            "Fetch the current week's institutional positioning regime and AI macro attribution "
            "for a market symbol (e.g. 'ES', 'GC', 'CL', '6E'). Returns AI bias score, momentum, "
            "crowdedness risk, smart money divergence, dumb money index, and qualitative attribution."
        ),
    )
    async def get_ai_inference(symbol: str) -> dict[str, Any]:
        clean_sym = symbol.strip().upper()
        cache_key = f"inference:{clean_sym}"
        if cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return {**cached, "cached": True}

        try:
            client = get_client()
            inference = await client.inference.get(clean_sym)
            result = {**inference.model_dump(), "cached": False}
            if cache:
                cache.set(cache_key, result, ttl_seconds=300.0)
            return result
        except CotApiError as e:
            sys.stderr.write(f"[cotbias-mcp] get_ai_inference error for {clean_sym}: {e}\n")
            return _format_error(e, hint_symbol=clean_sym)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[cotbias-mcp] get_ai_inference unexpected error for {clean_sym}: {e}\n")
            return {"error": {"code": "UNEXPECTED_ERROR", "message": str(e)}}

    @server.tool(
        name="get_timeseries",
        description=(
            "Fetch historical COT weekly positioning time series for a market symbol. "
            "Returns open interest, commercial/non-commercial net contracts, % of OI, "
            "52-week COT index, 3-year Z-score, and hedging pressure. "
            "Lookback defaults to 26 weeks (max 156) to preserve LLM token context."
        ),
    )
    async def get_timeseries(
        symbol: str,
        contract_type: str = "futopt",
        lookback_weeks: int = 26,
        report: str = "legacy",
    ) -> dict[str, Any]:
        clean_sym = symbol.strip().upper()
        clamped_lookback = min(max(1, lookback_weeks), 156)
        cache_key = f"ts:{clean_sym}:{contract_type}:{clamped_lookback}:{report}"
        if cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return {**cached, "cached": True}

        try:
            client = get_client()
            ts = await client.timeseries.get(
                clean_sym,
                contract_type=contract_type,  # type: ignore[arg-type]
                lookback_weeks=clamped_lookback,
                report=report,  # type: ignore[arg-type]
                as_dataframe=False,
            )
            rows = [
                {
                    "report_date": r.report_date,
                    "open_interest": r.open_interest,
                    "delta_oi": r.delta_open_interest,
                    "commercial_net": r.commercial_net,
                    "commercial_net_pct_oi": r.commercial_net_pct_oi,
                    "noncommercial_net": r.noncommercial_net,
                    "noncommercial_net_pct_oi": r.noncommercial_net_pct_oi,
                    "cot_52w_commercial": r.cot_52w_commercial,
                    "z_score_156w_commercial": r.z_score_156w_commercial,
                    "dumb_money_index": r.dumb_money_index,
                    "smart_money_divergence": r.smart_money_divergence_index,
                    "hedging_pressure": r.commercial_hedging_pressure,
                }
                for r in ts.data  # type: ignore[union-attr]
            ]
            result = {
                "symbol": clean_sym,
                "contract_type": contract_type,
                "report": report,
                "count": len(rows),
                "data": rows,
                "cached": False,
            }
            if cache:
                cache.set(cache_key, result, ttl_seconds=3600.0)
            return result
        except CotApiError as e:
            sys.stderr.write(f"[cotbias-mcp] get_timeseries error for {clean_sym}: {e}\n")
            return _format_error(e, hint_symbol=clean_sym)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[cotbias-mcp] get_timeseries unexpected error for {clean_sym}: {e}\n")
            return {"error": {"code": "UNEXPECTED_ERROR", "message": str(e)}}

    @server.tool(
        name="scan_markets",
        description=(
            "Screen across all CFTC tracked markets using institutional classification filters. "
            "Filters: ai_bias_score ('Strongly Bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly Bearish'), "
            "crowdedness_risk ('High Liquidation Risk', 'High Squeeze Risk', 'Balanced'), "
            "momentum ('New Longs (OI Expanding)', 'Short Covering (OI Contracting)', etc.), "
            "cot_positioning ('Convergence', 'Divergence')."
        ),
    )
    async def scan_markets(
        ai_bias_score: str | None = None,
        crowdedness_risk: str | None = None,
        momentum: str | None = None,
        cot_positioning: str | None = None,
    ) -> dict[str, Any]:
        cache_key = f"scan:{ai_bias_score}:{crowdedness_risk}:{momentum}:{cot_positioning}"
        if cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return {**cached, "cached": True}

        try:
            client = get_client()
            resp = await client.screener.scan(
                ai_bias_score=ai_bias_score,
                crowdedness_risk=crowdedness_risk,
                momentum=momentum,
                cot_positioning=cot_positioning,
                as_dataframe=False,
            )
            raw = [r.model_dump() for r in resp.results]  # type: ignore[union-attr]
            result = {
                "total_matches": resp.total_matches,  # type: ignore[union-attr]
                "results": raw,
                "cached": False,
            }
            if cache:
                cache.set(cache_key, result, ttl_seconds=300.0)
            return result
        except CotApiError as e:
            sys.stderr.write(f"[cotbias-mcp] scan_markets error: {e}\n")
            return _format_error(e)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[cotbias-mcp] scan_markets unexpected error: {e}\n")
            return {"error": {"code": "UNEXPECTED_ERROR", "message": str(e)}}

    @server.tool(
        name="get_market_snapshot",
        description=(
            "Composite tool for comprehensive market positioning analysis. Fetches current week's "
            "AI inference, macro rationale, flow summary, plus the latest 4-week COT trend in a single "
            "token-efficient call."
        ),
    )
    async def get_market_snapshot(symbol: str) -> dict[str, Any]:
        clean_sym = symbol.strip().upper()
        inf_task = get_ai_inference(clean_sym)
        ts_task = get_timeseries(clean_sym, lookback_weeks=4)
        inf_res, ts_res = await asyncio.gather(inf_task, ts_task)

        if "error" in inf_res:
            return inf_res

        return {
            "symbol": clean_sym,
            "inference": {k: v for k, v in inf_res.items() if k != "cached"},
            "recent_positioning_trend": ts_res.get("data", []),
            "cached": inf_res.get("cached", False) and ts_res.get("cached", False),
        }

    # --------------------------------------------------------------------------
    # RESOURCES
    # --------------------------------------------------------------------------

    @server.resource("cot://markets", mime_type="application/json")
    async def get_markets_resource() -> str:
        """Resource providing the full universe of tracked CFTC COT markets in JSON format."""
        res = await list_markets()
        return json.dumps(res, indent=2)

    # --------------------------------------------------------------------------
    # PROMPTS
    # --------------------------------------------------------------------------

    @server.prompt(
        name="cot-macro-briefing",
        description="Generate a weekly macro positioning briefing across Equities, Commodities, and Rates.",
    )
    def cot_macro_briefing() -> str:
        return (
            "You are an institutional macro quantitative analyst specializing in CFTC Commitments of Traders (COT) flows.\n"
            "1. Call 'scan_markets' to discover contracts with 'High Liquidation Risk' and 'High Squeeze Risk'.\n"
            "2. Identify the top 3 extreme positioning shifts across Equities (ES/NQ), Commodities (GC/CL), and Rates (ZB/ZN).\n"
            "3. Summarize the commercial vs non-commercial flow dynamics and highlight where Dumb Money is trapped or where Smart Money is aggressively diverging."
        )

    @server.prompt(
        name="cot-market-deep-dive",
        description="Conduct an institutional deep-dive on a specific symbol (e.g. 'GC', 'ES', 'CL', '6E').",
    )
    def cot_market_deep_dive(symbol: str) -> str:
        return (
            f"Perform an institutional CFTC COT positioning deep-dive for {symbol.upper()}.\n"
            f"1. Call 'get_market_snapshot' for symbol '{symbol.upper()}'.\n"
            "2. Evaluate the regime status, momentum classification, and crowdedness risk.\n"
            "3. Review the commercial hedging pressure and historical percentile.\n"
            "4. Conclude with a probabilistic market outlook and key inflection levels based on positioning vulnerability."
        )

    return server


def main() -> None:
    """Entry point for cotbias-mcp executable."""
    parser = argparse.ArgumentParser(description="COT Bias MCP Server - Model Context Protocol for Quant Tier COT Data")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
        help="Transport mode (default: stdio)",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host for network transports")
    parser.add_argument("--port", type=int, default=8000, help="Port for network transports")
    parser.add_argument("--no-cache", action="store_true", help="Disable in-memory quota preservation cache")
    args = parser.parse_args()

    if not os.getenv("COT_API_KEY"):
        sys.stderr.write(
            "[cotbias-mcp] WARNING: COT_API_KEY environment variable is not set.\n"
            "[cotbias-mcp] Tool calls will return authentication errors until COT_API_KEY is configured.\n"
        )

    server = create_server(enable_cache=not args.no_cache)

    if args.transport == "stdio":
        server.run(transport="stdio")
    elif args.transport == "streamable-http":
        server.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        server.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
