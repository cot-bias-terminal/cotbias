# COT Bias MCP Server (`cotbias-mcp`)

The **COT Bias MCP Server** implements Anthropic's [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) to connect institutional CFTC Commitments of Traders (COT) positioning regimes directly into AI agents (Claude Desktop, Cursor, Cline, LibreChat, and other MCP clients).

---

## ⚡ Quickstart

### 1. Requirements
- A valid **Quant Tier** API key from [COT Bias Terminal](https://cot-bias-terminal.com).
- Python 3.10+ installed (`uv` or `pipx` recommended).

### 2. Claude Desktop Setup

Edit your Claude Desktop configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the `cotbias` server under `mcpServers`:

```json
{
  "mcpServers": {
    "cotbias": {
      "command": "uvx",
      "args": ["cotbias[mcp]", "cotbias-mcp"],
      "env": {
        "COT_API_KEY": "cot_live_YOUR_ACTUAL_API_KEY"
      }
    }
  }
}
```

Restart Claude Desktop. You will see a hammer icon 🔨 indicating the COT Bias tools are ready.

---

### 3. Cursor IDE Setup

In your project root, create or edit `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "cotbias": {
      "command": "uvx",
      "args": ["cotbias[mcp]", "cotbias-mcp"],
      "env": {
        "COT_API_KEY": "cot_live_YOUR_ACTUAL_API_KEY"
      }
    }
  }
}
```

---

## 🛠 Available Tools

| Tool | Parameters | Description |
|---|---|---|
| `get_market_snapshot` | `symbol` (e.g. `'ES'`, `'GC'`, `'CL'`, `'6E'`) | **Recommended**: Single call synthesizing the current week's AI regime, macro attribution, flow summary, and the latest 4-week COT trend. |
| `get_ai_inference` | `symbol` | Institutional positioning regime, AI bias score, momentum, crowdedness risk, dumb money index, and macro rationale. |
| `get_timeseries` | `symbol`, `contract_type`, `lookback_weeks` (default 26, max 156), `report` | Historical weekly positioning data (commercial/non-commercial net, % of OI, 52-week COT index, 3-year Z-score, hedging pressure). |
| `scan_markets` | `ai_bias_score`, `crowdedness_risk`, `momentum`, `cot_positioning` | Multi-market screener across all tracked commodities, equities, FX, and rates. |
| `list_markets` | `sector` (optional: `'Equity'`, `'Commodity'`, `'FX'`, `'Rates'`) | List all tracked contracts with symbols, CFTC codes, and report mappings. |

---

## 📦 Resources & Prompts

- **Resource `cot://markets`**: JSON catalog of all tracked markets.
- **Prompt `cot-macro-briefing`**: Guided prompt analyzing macro positioning shifts and institutional extremes across Equities, Commodities, and Rates.
- **Prompt `cot-market-deep-dive`**: Deep-dive analysis for a specific ticker symbol.

---

## 🛡 Quota & Performance Guardrails

1. **In-Memory TTL Caching**: The server automatically caches tool responses (5 minutes for inference/screener, 1 hour for timeseries) to prevent AI chat sessions from rapidly consuming your daily 2,000 requests/day quota on weekly COT data.
2. **Context-Optimized Payloads**: Timeseries queries default to 26 weeks and project core analytical fields to keep prompt token consumption minimal.
3. **Actionable Error Messages**: If your key is invalid or your daily quota is exhausted, tools return clean structured errors with hints rather than crashing the agent.
