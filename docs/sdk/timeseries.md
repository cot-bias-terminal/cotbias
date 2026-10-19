# Timeseries Data Guide

The **Timeseries endpoint** (`client.timeseries.get()`) provides programmatic access to historical weekly positioning data published by the U.S. Commodity Futures Trading Commission (CFTC).

`cotbias` allows you to query up to **156 weeks (3 years)** of historical weekly data across multiple CFTC report families, returning either analysis-ready Pandas DataFrames or typed Pydantic models.

---

## ⚡ Quick Example

```python
from cotbias import CotClient

with CotClient() as client:
    # 52 weeks of E-mini S&P 500 combined positioning
    df = client.timeseries.get("ES", lookback_weeks=52, as_dataframe=True)

print(df[["commercial_net", "noncommercial_net", "cot_52w_commercial"]].tail())
```

---

## 🛠 Parameters Reference

```python
client.timeseries.get(
    symbol: str,
    contract_type: str = "futopt",
    lookback_weeks: int = 156,
    report: str = "legacy",
    as_dataframe: bool = True,
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `symbol` | `str` | *Required* | Market ticker symbol (e.g. `'ES'`, `'NQ'`, `'GC'`, `'CL'`, `'6E'`, `'ZB'`). Case-insensitive. |
| `contract_type` | `str` | `'futopt'` | Position breakdown: `'fut'` (Futures only), `'futopt'` (Combined Futures & Options), or `'opt'` (Options delta). |
| `lookback_weeks` | `int` | `156` | Number of weekly reports to retrieve (1 to 156 weeks). |
| `report` | `str` | `'legacy'` | CFTC report classification family: `'legacy'`, `'disaggregated'`, `'tff'`, or `'supplemental'`. |
| `as_dataframe` | `bool` | `True` | Return a DatetimeIndex-sorted Pandas DataFrame (`True`) or a typed Pydantic model (`False`). |

---

## 📊 CFTC Report Families

The CFTC categorizes market participants differently across four official report types:

### 1. Legacy Report (`report='legacy'`)
The historical benchmark report dividing participants into two primary groups:
- **Commercials**: Hedgers, producers, merchants, and swap dealers who use futures to hedge business risk.
- **Non-Commercials**: Speculators, hedge funds, commodity trading advisors (CTAs), and asset managers.
- **Non-Reportables**: Small retail retail traders below reportable CFTC position thresholds.

### 2. Disaggregated Report (`report='disaggregated'`)
Standard for physical commodities (Crude Oil, Gold, Corn, Wheat, Natural Gas):
- **Producer / Merchant / Processor / User**
- **Swap Dealers**
- **Managed Money** (Hedge funds, CTAs)
- **Other Reportables**

### 3. Financial Traders Report (`report='tff'`)
Standard for financial futures (Equities, FX, US Treasury bonds, Eurodollars):
- **Dealer / Intermediary** (Sell-side banks and market makers)
- **Asset Manager / Institutional** (Pension funds, mutual funds, insurance)
- **Leveraged Funds** (Hedge funds, proprietary trading desks)
- **Other Reportables**

### 4. Supplemental / CIT (`report='supplemental'`)
Tracks Index Trader activity across 12 selected agricultural and soft commodity contracts.

---

## 📐 Key Analytical Metrics

Every timeseries record includes computed quantitative indicators alongside raw position sizes:

### 1. 52-Week COT Index (`cot_52w_commercial`)
Normalizes current commercial net positioning against its 52-week rolling minimum and maximum:

$$\text{COT Index} = \frac{\text{Net Position}_t - \text{Min}_{52w}}{\text{Max}_{52w} - \text{Min}_{52w}} \times 100$$

- **Values > 80**: Commercials are holding historically heavy net-long hedges (historically bullish signal for the underlying asset).
- **Values < 20**: Commercials are holding historically heavy net-short hedges (historically bearish/crowded signal).

### 2. 3-Year Rolling Z-Score (`z_score_156w_commercial`)
Measures how many standard deviations the current positioning deviates from its 3-year mean:

$$Z = \frac{\text{Net Position}_t - \mu_{156w}}{\sigma_{156w}}$$

- **$Z > +2.0$**: Extreme bullish institutional accumulation.
- **$Z < -2.0$**: Extreme bearish institutional distribution.

### 3. Hedging Pressure (`commercial_hedging_pressure`)
The ratio of commercial short positions to total commercial participation, indicating whether producers are aggressively locking in forward sales.

### 4. Top-4 Concentration Ratio (`conc_top4_net_short`)
Percentage of total open interest controlled by the 4 largest net-short institutional traders. Extreme values (> 40%) indicate vulnerability to short squeeze dynamics.

---

## 📈 Working with Pandas DataFrames

When `as_dataframe=True` (default), the returned DataFrame is automatically:
1. Converted to a `pd.DatetimeIndex` on `report_date`.
2. Sorted chronologically in ascending order (oldest to newest).

```python
import matplotlib.pyplot as plt
from cotbias import CotClient

with CotClient() as client:
    df = client.timeseries.get("GC", lookback_weeks=104, as_dataframe=True)

# Plot Gold Commercial vs Non-Commercial positioning
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(df.index, df["commercial_net"] / 1000, label="Commercials (k contracts)", color="#e74c3c")
ax1.plot(df.index, df["noncommercial_net"] / 1000, label="Speculators (k contracts)", color="#2ecc71")
ax1.set_ylabel("Net Positioning (Thousands)")
ax1.axhline(0, color="gray", linestyle="--", alpha=0.6)
ax1.legend(loc="upper left")
ax1.set_title("Gold (GC) Institutional COT Positioning")
plt.tight_layout()
plt.show()
```

---

## 🧩 Working with Pydantic Models

If you prefer strongly typed objects for strict serialization, pass `as_dataframe=False`:

```python
from cotbias import CotClient
from cotbias.models import TimeseriesResponse

with CotClient() as client:
    res: TimeseriesResponse = client.timeseries.get("CL", lookback_weeks=12, as_dataframe=False)

print(f"Contract: {res.symbol} | CFTC #{res.cftc_code}")
print(f"Total Weeks: {res.count}")

latest_week = res.data[-1]
print(f"Date: {latest_week.report_date}")
print(f"Speculator Net: {latest_week.noncommercial_net:,} contracts")
```
