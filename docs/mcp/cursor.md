# Cursor IDE Integration

Integrating the **COT Bias MCP Server** with [Cursor](https://cursor.com) allows Cursor's AI (Chat, Composer, and Agent) to query real-time institutional positioning directly while you write code, backtest strategies, or conduct quantitative research.

---

## ⚡ Setup in 2 Steps

### 1. Configure `.cursor/mcp.json`

In the root of your workspace, create or edit `.cursor/mcp.json`:

```json
--8<-- "docs/snippets/mcp-config.json"
```

*(Alternatively, configure globally via **Cursor Settings** &rarr; **Features** &rarr; **MCP** &rarr; **Add New MCP Server**).*

### 2. Verify in Cursor Settings

1. Open **Cursor Settings** (`Cmd + ,` on macOS, `Ctrl + ,` on Windows).
2. Navigate to **Features** &rarr; **MCP**.
3. You will see `cotbias` listed with a **green status indicator**, showing 5 active tools.

---

## 💻 Workflow Examples in Cursor

### 1. Generating Backtest Code with COT Filters

In Cursor Composer (`Cmd + I` or `Ctrl + I`):

> *"Check the current COT positioning regime for E-mini S&P 500 (ES). Then write a Python script using pandas and backtrader that implements a trend-following strategy, using the COT 52-week index as a regime filter."*

Cursor will call `get_market_snapshot(symbol="ES")`, inspect the regime, and generate Python code with accurate positioning parameters.

### 2. Scanning for Trading Setups

In Cursor Chat (`Cmd + L`):

> *"Scan the market universe for any contracts where momentum is 'New Longs (OI Expanding)' and crowdedness is 'Balanced'. Return the findings in a markdown table."*

Cursor will call `scan_markets` and format the matched contracts directly in your chat.

### 3. Quantitative Timeseries Modeling

In Cursor Chat:

> *"Fetch 104 weeks of Gold (GC) timeseries data using cotbias and show me how to compute the correlation between commercial net positioning and next-month price returns."*
