# Claude Desktop Setup

Connect the **COT Bias MCP Server** directly into Anthropic's [Claude Desktop](https://claude.ai/download) to give Claude real-time institutional CFTC positioning intelligence, AI market regimes, and macro attribution.

---

## ⚡ Setup in 3 Minutes

### 1. Requirements
- [Claude Desktop](https://claude.ai/download) installed on macOS or Windows.
- Python 3.10+ and [`uv`](https://astral.sh/uv) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
- A **Quant Tier** API key from [COT Bias Terminal](https://cot-bias-terminal.com).

### 2. Configure Claude Desktop

Open your Claude Desktop configuration file:

=== "macOS"
    ```bash
    code ~/Library/Application\ Support/Claude/claude_desktop_config.json
    ```

=== "Windows"
    Open `%APPDATA%\Claude\claude_desktop_config.json` in your favorite editor.

Add the `cotbias` server under `mcpServers`:

```json
--8<-- "docs/snippets/mcp-config.json"
```

Replace `cot_live_YOUR_ACTUAL_API_KEY` with your actual Quant API key.

### 3. Restart Claude Desktop

Completely quit and restart Claude Desktop. 

Look for the **hammer icon (🔨)** at the bottom-right of the prompt input window. Clicking it should list the 5 COT Bias tools:
- `get_market_snapshot`
- `get_ai_inference`
- `get_timeseries`
- `scan_markets`
- `list_markets`

---

## 💬 Example Prompts to Try

Once connected, you can ask Claude natural language questions. Claude will automatically invoke the appropriate tool:

=== "Macro Briefing"
    > *"Give me a weekly macro briefing on institutional COT positioning across Equities, Commodities, and Rates."*
    
    Claude will call `scan_markets` and synthesize extreme positioning and squeeze risks.

=== "Ticker Deep-Dive"
    > *"What is the current institutional positioning regime in Gold (GC)? Are commercial hedgers accumulating or distributing?"*
    
    Claude will call `get_market_snapshot` or `get_ai_inference` for Gold.

=== "Squeeze Analysis"
    > *"Scan the futures universe for contracts with High Squeeze Risk and tell me which markets have speculative shorts trapped."*
    
    Claude will call `scan_markets(crowdedness_risk="High Squeeze Risk")`.

---

## 🛡 Quota Protection

Claude conversations often involve multi-turn questions about the same asset. 

The COT Bias MCP server includes an automatic **in-memory TTL cache** (5 minutes for regimes/screeners, 1 hour for timeseries), ensuring that multiple follow-up questions do not drain your 2,000 requests/day API quota.
