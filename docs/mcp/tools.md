# MCP Tools Reference

The **COT Bias MCP Server** (`cotbias-mcp`) exposes five high-level tools, one resource catalog, and two guided prompt templates designed specifically for LLM context windows.

---

## 🛠 Available Tools

### 1. `get_market_snapshot` (Recommended)
**Description**: Single-call comprehensive synthesis of an asset's current weekly AI positioning regime, macro narrative attribution, capital flow summary, and the latest 4-week COT trend.

- **Parameters**:
  - `symbol` (`string`, *required*): Asset ticker symbol (e.g. `'ES'`, `'GC'`, `'CL'`, `'6E'`).
- **Best For**: General questions about a market where the agent needs both qualitative rationale and quantitative trends in a single compact tool call.

---

### 2. `get_ai_inference`
**Description**: Current week's institutional positioning regime and AI macro attribution.

- **Parameters**:
  - `symbol` (`string`, *required*): Market symbol (e.g. `'GC'`).
- **Response Fields**:
  - `ai_bias_score`: `'Strongly Bullish'`, `'Bullish'`, `'Neutral'`, `'Bearish'`, `'Strongly Bearish'`
  - `regime_status`: `'Bullish Alignment'`, `'Transitioning'`, etc.
  - `primary_driver`: Dominant participant group.
  - `momentum`: Open interest dynamics (`'New Longs'`, `'Short Covering'`).
  - `crowdedness_risk`: Squeeze vs Liquidation assessment.
  - `smart_money_divergence`: Smart vs dumb money accumulation.
  - `dumb_money_index`: Speculator crowd sentiment index.
  - `qualitative_attribution`: Macro commentary breakdown.

---

### 3. `get_timeseries`
**Description**: Historical weekly CFTC positioning data across Legacy, Disaggregated, TFF, or Supplemental reports.

- **Parameters**:
  - `symbol` (`string`, *required*): Market symbol.
  - `contract_type` (`string`, optional, default `'futopt'`): `'fut'` (Futures only), `'futopt'` (Combined), or `'opt'` (Options delta).
  - `lookback_weeks` (`integer`, optional, default `26`, max `156`): Number of weekly records to retrieve. Defaults to 26 weeks to preserve LLM token context.
  - `report` (`string`, optional, default `'legacy'`): CFTC report family.

---

### 4. `scan_markets`
**Description**: Screen across all 60+ tracked futures markets by positioning classifications and squeeze risks.

- **Parameters**:
  - `ai_bias_score` (`string`, optional): Filter by directional bias.
  - `crowdedness_risk` (`string`, optional): Filter by risk (e.g. `'High Squeeze Risk'`).
  - `momentum` (`string`, optional): Filter by flow dynamics (e.g. `'New Longs (OI Expanding)'`).
  - `cot_positioning` (`string`, optional): Filter by alignment (`'Convergence'`, `'Divergence'`).

---

### 5. `list_markets`
**Description**: List all tracked futures and options contracts with symbols, CFTC commodity codes, and supported report types.

- **Parameters**:
  - `sector` (`string`, optional): Filter by sector (`'Equity'`, `'Commodity'`, `'FX'`, `'Rates'`).

---

## 📦 Resources

- **`cot://markets`**: JSON catalog of all tracked markets, updated dynamically from the API.

---

## 📝 Prompt Templates

MCP clients supporting prompts can trigger pre-engineered analytical workflows:

### 1. `cot-macro-briefing`
Instructs the agent to scan the entire futures universe for extreme squeeze risks and liquidation setups across Equities, Commodities, and Rates, followed by an institutional macro commentary.

### 2. `cot-market-deep-dive`
- **Arguments**: `symbol`
- Conducts an end-to-end positioning evaluation for the specified asset, inspecting commercial hedging pressure, multi-week momentum, and structural inflection levels.
