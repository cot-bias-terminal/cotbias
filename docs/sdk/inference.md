# AI Inference & Market Regimes

The **Inference endpoint** (`client.inference.get()`) provides current-week AI-synthesized market positioning regimes, quantitative bias ratings, participant flow attribution, and structural risk metrics.

Rather than looking at raw contract numbers in isolation, the inference engine synthesizes historical percentiles, multi-report participant shifts, open interest momentum, and macroeconomic catalysts into an actionable quantitative regime.

---

## ⚡ Quick Example

```python
from cotbias import CotClient

with CotClient() as client:
    regime = client.inference.get("GC")  # Gold

print(f"Market: {regime.symbol} ({regime.report_date})")
print(f"Bias Score: {regime.ai_bias_score}")
print(f"Regime Status: {regime.regime_status}")
print(f"Primary Driver: {regime.primary_driver}")
print(f"Momentum: {regime.momentum}")
print(f"Crowdedness Risk: {regime.crowdedness_risk}")
print(f"\nMacro Rationale:\n{regime.qualitative_attribution.macro_rationale}")
```

---

## 🔍 Core Output Schema

The method returns an :class:`~cotbias.models.inference.InferenceSchema` model containing the following fields:

### 1. `ai_bias_score` (Directional Classification)
A consolidated assessment of directional positioning pressure:
- **`'Strongly Bullish'`**: Concurrent speculative accumulation and commercial de-hedging at extreme historical percentiles.
- **`'Bullish'`**: Net positive positioning expansion supported by healthy open interest.
- **`'Neutral'`**: Balanced positioning without clear directional conviction.
- **`'Bearish'`**: Speculative de-risking or persistent commercial forward selling.
- **`'Strongly Bearish'`**: Extreme speculative crowding with elevated liquidation susceptibility.

### 2. `regime_status` (Structural Alignment)
The macro alignment between participant groups:
- **`'Bullish Alignment'`**: Speculators are net-long while commercials accommodate with disciplined hedge books.
- **`'Bearish Alignment'`**: Speculators are aggressively expanding short exposures.
- **`'Transitioning'`**: Early-stage regime rotation (e.g. initial short covering or long liquidation).
- **`'Neutral / Balanced'`**: Market positioning is near multi-year median levels.

### 3. `primary_driver` (Dominant Participant Group)
Identifies which market cohort spearheaded the largest week-over-week position shift:
- **`'Leveraged Funds'`** (Hedge funds, CTAs)
- **`'Asset Managers'`** (Real money, pension institutions)
- **`'Dealer'`** (Sell-side liquidity providers)
- **`'Commercials'`** (Physical producers/consumers)
- **`'Non-Reportables'`** (Retail traders)

### 4. `momentum` (Open Interest Dynamics)
Classifies the interaction between net positioning shifts and aggregate Open Interest (OI):
- **`'New Longs (OI Expanding)'`**: Aggressive fresh capital entering on the long side (strongest bullish momentum).
- **`'Short Covering (OI Contracting)'`**: Price appreciation driven by short-sellers closing positions rather than fresh buyers.
- **`'New Shorts (OI Expanding)'`**: Fresh capital entering to short the market (strongest bearish momentum).
- **`'Long Liquidation (OI Contracting)'`**: Price weakness driven by existing bulls abandoning positions.
- **`'Stagnant'`**: Negligible net shift in open interest or positioning.

### 5. `crowdedness_risk` (Asymmetric Risk Assessment)
- **`'High Liquidation Risk'`**: Speculative longs are near multi-year extremes. Any adverse price shock is vulnerable to cascading stop-outs.
- **`'High Squeeze Risk'`**: Speculative shorts are heavily crowded. An upside catalyst can trigger explosive short covering rallies.
- **`'Balanced'`**: Risk distribution is symmetrical.

### 6. `smart_money_divergence` & `dumb_money_index`
- **`smart_money_divergence`** (`'Aggressive'`, `'Conservative'`, `'Neutral'`): Measures whether commercial hedgers (the "smart money" with physical market knowledge) are taking positions opposite to retail/trend-following funds.
- **`dumb_money_index`** (`'Euphoria'`, `'Fear'`, `'Neutral'`): Sentiment index derived from small speculator positioning ratios.

### 7. `qualitative_attribution` (Macro Narrative)
Structured institutional commentary explaining the numbers:
```python
print(regime.qualitative_attribution.flow_dynamic_summary)
print(regime.qualitative_attribution.macro_rationale)
print(regime.qualitative_attribution.structural_vulnerability)
```

---

## 💡 Practical Trading Applications

### 1. Trend Following Confirmation
Filter technical breakout signals: only take long breakouts when `ai_bias_score` is `'Bullish'` or `'Strongly Bullish'`, and avoid initiating long trades when `crowdedness_risk` is `'High Liquidation Risk'`.

### 2. Contrarian Mean-Reversion
Screen for markets with extreme `smart_money_divergence == 'Aggressive'` and `dumb_money_index == 'Euphoria'`. These inflection points frequently precede major multi-week market turns.
