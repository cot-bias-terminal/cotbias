# Markets Catalog

The **Markets endpoint** (`client.markets.list()`) provides the official catalog of all futures and options contracts tracked in the COT Bias Terminal universe.

Use this endpoint to discover supported asset tickers, CFTC commodity codes, sector classifications, and supported report types.

---

## ⚡ Quick Example

```python
from cotbias import CotClient

with CotClient() as client:
    # List all tracked FX contracts
    fx_markets = client.markets.list(sector="FX")

for market in fx_markets:
    print(f"{market.symbol:<6} | {market.name:<25} | CFTC #{market.cftc_code}")
```

---

## 🛠 Parameters Reference

```python
client.markets.list(sector: str | None = None) -> list[MarketMetadata]
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sector` | `str | None` | `None` | Filter by asset class sector: `'Equity'`, `'Commodity'`, `'FX'`, or `'Rates'`. If omitted, returns the entire catalog. |

---

## 📦 Output Structure (`MarketMetadata`)

Each returned item is an instance of :class:`~cotbias.models.markets.MarketMetadata`:

| Field | Type | Description | Example |
|---|---|---|---|
| `symbol` | `str` | Standard ticker symbol. | `'ES'` |
| `name` | `str` | Full descriptive contract name. | `'E-MINI S&P 500'` |
| `cftc_code` | `str` | Official CFTC commodity classification code. | `'13874+'` |
| `sector` | `str` | Asset sector (`'Equity'`, `'Commodity'`, `'FX'`, `'Rates'`). | `'Equity'` |
| `report_type` | `str` | Primary default report classification. | `'legacy'` |
| `has_options` | `bool` | Whether combined futures + options reports are available. | `True` |
| `available_reports` | `list[str]` | List of CFTC report families published for this asset. | `["legacy", "tff"]` |

---

## 💡 Practical Examples

### 1. Catalog Summary by Sector
Count how many contracts are tracked per sector:

```python
from collections import Counter
from cotbias import CotClient

with CotClient() as client:
    all_markets = client.markets.list()

counts = Counter(m.sector for m in all_markets)
print(f"Total Tracked Contracts: {len(all_markets)}")
for sector, count in counts.items():
    print(f"  {sector}: {count} contracts")
```

### 2. Validating Symbol Input
Check if a ticker is supported before making timeseries or inference calls:

```python
from cotbias import CotClient


def is_valid_cot_symbol(client: CotClient, symbol: str) -> bool:
    valid_symbols = {m.symbol.upper() for m in client.markets.list()}
    return symbol.upper() in valid_symbols


with CotClient() as client:
    print(is_valid_cot_symbol(client, "ES"))  # True
    print(is_valid_cot_symbol(client, "AAPL"))  # False (single-stock equity, not CFTC futures)
```

### 3. Iterating Over an Entire Sector
Fetch current AI bias scores for all contracts in a specific sector:

```python
from cotbias import CotClient

with CotClient() as client:
    commodities = client.markets.list(sector="Commodity")
    for market in commodities[:5]:
        regime = client.inference.get(market.symbol)
        print(f"{market.name:<24} ({market.symbol}): {regime.ai_bias_score}")
```
