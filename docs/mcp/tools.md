---
status: stub
---

# MCP Tools Reference

Complete parameter schemas, argument validation, and JSON response formats for all tools exposed by `cotbias-mcp`.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Available Tools Summary

1. `get_market_snapshot(symbol: str)`: Synthesized market summary (AI bias, macro attribution, flow, 4-week COT trend).
2. `get_ai_inference(symbol: str)`: Full institutional positioning regime and AI rationale.
3. `get_timeseries(symbol: str, contract_type: str = "combined", lookback_weeks: int = 26, report: str = "legacy")`: Historical positioning data.
4. `scan_markets(ai_bias_score: Optional[str], crowdedness_risk: Optional[str], momentum: Optional[str], cot_positioning: Optional[str])`: Cross-asset screener.
5. `list_markets(sector: Optional[str])`: Catalog of tracked contracts and sectors.

## Roadmap & Upcoming Content
- [ ] Schema specifications for every parameter.
- [ ] Sample JSON responses returned to the LLM.
- [ ] Token efficiency guidelines.
