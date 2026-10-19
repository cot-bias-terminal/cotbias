# Multi-Market Screener

The **Screener endpoint** (`client.screener.scan()`) enables quantitative scanning across all 60+ tracked futures markets across Equities, Fixed Income, FX, and Commodities.

Instead of inspecting contracts one by one, the screener lets you filter the global market universe by institutional positioning regimes, asymmetric squeeze setups, and open interest momentum.

---

## ⚡ Quick Example

```python
from cotbias import CotClient

with CotClient() as client:
    # Scan for contracts with High Squeeze Risk
    squeeze_candidates = client.screener.scan(
        crowdedness_risk="High Squeeze Risk",
        as_dataframe=True,
    )

print(squeeze_candidates[["symbol", "ai_bias_score", "regime_status", "momentum"]])
```

---

## 🛠 Filter Parameters

```python
client.screener.scan(
    ai_bias_score: str | None = None,
    crowdedness_risk: str | None = None,
    momentum: str | None = None,
    cot_positioning: str | None = None,
    as_dataframe: bool = True,
)
```

| Parameter | Type | Description |
|---|---|---|
| `ai_bias_score` | `str | None` | Filter by directional rating: `'Strongly Bullish'`, `'Bullish'`, `'Neutral'`, `'Bearish'`, `'Strongly Bearish'`. |
| `crowdedness_risk` | `str | None` | Filter by structural positioning risk: `'High Liquidation Risk'`, `'High Squeeze Risk'`, `'Balanced'`. |
| `momentum` | `str | None` | Filter by flow momentum: `'New Longs (OI Expanding)'`, `'Short Covering (OI Contracting)'`, `'New Shorts (OI Expanding)'`, `'Long Liquidation (OI Contracting)'`. |
| `cot_positioning` | `str | None` | Filter by alignment: `'Convergence'` or `'Divergence'`. |
| `as_dataframe` | `bool` | Return results as a Pandas DataFrame (`True`, default) or :class:`~cotbias.models.screener.ScreenerResponse` (`False`). |

---

## 🎯 High-Probability Scanning Recipes

### Recipe 1: Short Squeeze Candidates
Look for markets where speculators are crowded short and early short covering has begun:

```python
from cotbias import CotClient

with CotClient() as client:
    df = client.screener.scan(
        crowdedness_risk="High Squeeze Risk",
        as_dataframe=True,
    )

print(f"Found {len(df)} potential short squeeze setups:")
for _, row in df.iterrows():
    print(f"👉 {row['symbol']}: Driver: {row['primary_driver']}, Flow: {row['momentum']}")
```

### Recipe 2: Institutional Accumulation Breakouts
Look for bullish bias combined with fresh capital entering the market:

```python
from cotbias import CotClient

with CotClient() as client:
    df = client.screener.scan(
        ai_bias_score="Bullish",
        momentum="New Longs (OI Expanding)",
        as_dataframe=True,
    )

print(df[["symbol", "regime_status", "cot_52w_commercial"]])
```

### Recipe 3: Exhausted Speculative Rallies (Liquidation Risks)
Identify overheated bull markets vulnerable to sudden liquidation:

```python
from cotbias import CotClient

with CotClient() as client:
    df = client.screener.scan(
        crowdedness_risk="High Liquidation Risk",
        as_dataframe=True,
    )

print("Vulnerable Markets:")
print(df[["symbol", "primary_driver", "momentum"]])
```

---

## 🧩 Working with Typed Response Models

When integrating into automated microservices, set `as_dataframe=False`:

```python
from cotbias import CotClient
from cotbias.models import ScreenerResponse

with CotClient() as client:
    response: ScreenerResponse = client.screener.scan(
        ai_bias_score="Strongly Bullish",
        as_dataframe=False,
    )

print(f"Total Matches: {response.total_matches}")
for item in response.results:
    print(f"- {item.symbol}: {item.regime_status} ({item.primary_driver})")
```
