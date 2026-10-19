# cotbias

[![PyPI version](https://img.shields.io/pypi/v/cotbias.svg)](https://pypi.org/project/cotbias/)
[![Python versions](https://img.shields.io/pypi/pyversions/cotbias.svg)](https://pypi.org/project/cotbias/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Official Python SDK and Model Context Protocol (MCP) Server for the **CFTC Commitment of Traders (COT) Bias Terminal** Quant API.

Access institutional positioning metrics, 156-week historical timeseries across multiple CFTC report families, cross-market positioning screeners, and AI-driven market regime & attribution analysis directly in Python and in AI assistants (Claude Desktop, Cursor, Cline).

---

## Installation

### Python SDK (Batteries-included with Pandas)
```bash
pip install cotbias
```

### With Model Context Protocol (MCP) Server
For connecting into Claude Desktop, Cursor, or Cline:
```bash
pip install "cotbias[mcp]"
```

---

## 🤖 Model Context Protocol (MCP) Server

Connect your Quant API key directly into Claude Desktop or Cursor IDE:

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

See [docs/mcp.md](docs/mcp.md) for full configuration details, available tools (`get_market_snapshot`, `get_ai_inference`, `get_timeseries`, `scan_markets`, `list_markets`), and quota preservation caching.

---

## Quickstart

Get your API key at [cot-bias-terminal.com](https://cot-bias-terminal.com). Set it as an environment variable:

```bash
export COT_API_KEY="cot_live_..."
```

### 1. Fetch Positioning Timeseries into Pandas

```python
from cotbias import CotClient

with CotClient() as cot:
    # Pull 156 weeks of combined futures & options data for Gold (GC) as a Pandas DataFrame
    df = cot.timeseries.get("GC", contract_type="futopt", lookback_weeks=156, as_dataframe=True)
    print(df[["commercial_net", "cot_52w_commercial", "z_score_156w_commercial"]].tail())
```

### 2. AI Market Regime & Qualitative Attribution

```python
from cotbias import CotClient

with CotClient() as cot:
    inf = cot.inference.get("GC")
    print(f"Asset: {inf.symbol}")
    print(f"Bias: {inf.ai_bias_score} | Regime: {inf.regime_status}")
    print(f"Primary Driver: {inf.primary_driver} ({inf.momentum})")
    print(f"Macro Rationale: {inf.qualitative_attribution.macro_rationale}")
```

### 3. Cross-Market Positioning Screener

```python
from cotbias import CotClient

with CotClient() as cot:
    # Find all markets where AI bias is Bullish and smart money is entering new longs
    res = cot.screener.scan(ai_bias_score="Bullish", momentum="New Longs (OI Expanding)")
    for item in res.results:
        print(f"{item.symbol}: {item.ai_bias_score} ({item.regime_status})")
```

### 4. Automatic Retries & Network Resilience

The SDK automatically retries transient 5xx errors, network timeouts, and transient rate limits with exponential backoff and jitter:

```python
from cotbias import CotClient

# Default max_retries=3. Set to 0 to disable or adjust for custom pipelines
with CotClient(max_retries=5, timeout=20.0) as cot:
    markets = cot.markets.list()
```

### 5. Asynchronous Client (FastAPI / Bots)

```python
import asyncio
from cotbias import AsyncCotClient


async def main():
    async with AsyncCotClient() as cot:
        # Fetch multiple markets concurrently
        gold_task = cot.timeseries.get("GC")
        sp500_task = cot.timeseries.get("ES")
        gold_ts, sp500_ts = await asyncio.gather(gold_task, sp500_task)
        print("Gold rows:", gold_ts.count, "| S&P 500 rows:", sp500_ts.count)


asyncio.run(main())
```

---

## Error Handling

All API errors inherit from `CotApiError`:

```python
from cotbias import CotClient
from cotbias.exceptions import (
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitExceededError,
)

try:
    with CotClient() as cot:
        cot.timeseries.get("INVALID_TICKER")
except NotFoundError as e:
    print(f"Asset not found: {e.message}")
except RateLimitExceededError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds.")
except AuthenticationError as e:
    print("Invalid or missing API key.")
```

---

## License

MIT License. Developed for quantitative traders, portfolio managers, and market researchers.
