# cotbias

[![PyPI version](https://img.shields.io/pypi/v/cotbias.svg)](https://pypi.org/project/cotbias/)
[![Python versions](https://img.shields.io/pypi/pyversions/cotbias.svg)](https://pypi.org/project/cotbias/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the **CFTC Commitment of Traders (COT) Bias Terminal** Quant API.

Access institutional positioning metrics, 156-week historical timeseries across multiple CFTC report families, cross-market positioning screeners, and AI-driven market regime & attribution analysis.

---

## Installation

```bash
pip install cotbias
```

Or using `uv`:

```bash
uv add cotbias
```

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
    # Pull 156 weeks of combined futures & options data for Gold (GC)
    df = cot.timeseries.get("GC", contract_type="futopt", lookback_weeks=156)
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
    df = cot.screener.scan(ai_bias_score="Bullish", momentum="New Longs (OI Expanding)")
    print(df[["symbol", "ai_bias_score", "regime_status", "cot_52w_commercial"]])
```

### 4. Asynchronous Client (FastAPI / Bots)

```python
import asyncio
from cotbias import AsyncCotClient

async def main():
    async with AsyncCotClient() as cot:
        # Fetch multiple markets concurrently
        gold_task = cot.timeseries.get("GC")
        sp500_task = cot.timeseries.get("ES")
        gold_df, sp500_df = await asyncio.gather(gold_task, sp500_task)
        print("Gold rows:", len(gold_df), "| S&P 500 rows:", len(sp500_df))

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
