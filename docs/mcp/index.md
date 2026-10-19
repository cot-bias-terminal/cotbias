# COT Bias MCP Server (`cotbias-mcp`)

The **COT Bias MCP Server** implements Anthropic's [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) to connect institutional CFTC Commitments of Traders (COT) positioning regimes directly into AI agents (Claude Desktop, Cursor, Cline, LibreChat, and other MCP clients).

---

## ⚡ Quickstart

### 1. Requirements
- A valid **Quant Tier** API key from [COT Bias Terminal](https://cot-bias-terminal.com).
- Python 3.10+ installed (`uv` or `pipx` recommended).

### 2. Client Configuration

Add the `cotbias` server to your client's configuration file (e.g. Claude Desktop or Cursor):

```json
--8<-- "docs/snippets/mcp-config.json"
```

For client-specific guides:
- [Claude Desktop Setup](claude-desktop.md)
- [Cursor IDE Setup](cursor.md)
- [Cline & Other MCP Clients](cline.md)

---

## 🛠 Available Tools

| Tool | Parameters | Description |
|---|---|---|
| `get_market_snapshot` | `symbol` (e.g. `'ES'`, `'GC'`, `'CL'`, `'6E'`) | **Recommended**: Single call synthesizing the current week's AI regime, macro attribution, flow summary, and latest 4-week COT trend. |
| `get_ai_inference` | `symbol` | Institutional positioning regime, AI bias score, momentum, crowdedness risk, dumb money index, and macro rationale. |
| `get_timeseries` | `symbol`, `contract_type`, `lookback_weeks` (default 26, max 156), `report` | Historical weekly positioning data (commercial/non-commercial net, % of OI, 52-week COT index, 3-year Z-score, hedging pressure). |
| `scan_markets` | `ai_bias_score`, `crowdedness_risk`, `momentum`, `cot_positioning` | Multi-market screener across all tracked commodities, equities, FX, and rates. |
| `list_markets` | `sector` (optional: `'Equity'`, `'Commodity'`, `'FX'`, `'Rates'`) | List all tracked contracts with symbols, CFTC codes, and report mappings. |

See [Tools Reference](tools.md) for in-depth parameter schemas and response formats.

---

## 📦 Resources & Prompts

- **Resource `cot://markets`**: JSON catalog of all tracked markets.
- **Prompt `cot-macro-briefing`**: Guided prompt analyzing macro positioning shifts and institutional extremes across Equities, Commodities, and Rates.
- **Prompt `cot-market-deep-dive`**: Deep-dive analysis for a specific ticker symbol.

---

## 🛡 Quota & Performance Guardrails

1. **In-Memory TTL Caching**: The server automatically caches tool responses (5 minutes for inference/screener, 1 hour for timeseries) to prevent AI chat sessions from rapidly consuming your daily 2,000 requests/day quota on weekly COT data. See [Caching & Quotas](caching.md).
2. **Context-Optimized Payloads**: Timeseries queries default to 26 weeks and project core analytical fields to keep prompt token consumption minimal.
3. **Actionable Error Messages**: If your key is invalid or your daily quota is exhausted, tools return clean structured errors with hints rather than crashing the agent. See [Troubleshooting](troubleshooting.md).
