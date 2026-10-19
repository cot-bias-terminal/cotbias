# In-Memory Caching & Quota Protection

The **COT Bias MCP Server** incorporates a built-in, thread-safe in-memory Time-to-Live (TTL) cache to safeguard your daily 2,000 requests/day Quant API quota and drastically reduce latency during interactive agent conversations.

---

## 🎯 Why Caching Matters for AI Agents

CFTC Commitment of Traders reports are published **once per week** (typically Friday afternoons at 3:30 PM Eastern Time). 

When you converse with an AI agent (such as Claude Desktop or Cursor), the model often queries the same asset multiple times across a conversational turn (e.g. asking for an overview, then asking about momentum, then asking for a trading idea).

Without caching, a 10-turn conversation about Gold would execute 10 separate HTTP requests against your daily API allowance. With caching, only the first call hits the backend API—subsequent turns return in **sub-millisecond time** from local memory.

---

## ⏱ TTL Duration Policy

| Endpoint / Tool | TTL Duration | Rationale |
|---|---|---|
| `get_ai_inference` | 5 minutes (300s) | Captures real-time updates while protecting multi-turn dialogs. |
| `scan_markets` | 5 minutes (300s) | Preserves quota during multi-step screener evaluation. |
| `get_timeseries` | 1 hour (3,600s) | Historical weekly timeseries data is static throughout the week. |
| `get_market_snapshot` | 5 minutes (300s) | Balances fresh commentary with token and quota efficiency. |
| `list_markets` | 1 hour (3,600s) | Contract metadata and sector classifications are static. |

---

## 🔍 Inspecting Cache Hits

Every JSON response returned by the MCP server includes a top-level `"cached"` boolean flag:

```json
{
  "symbol": "GC",
  "ai_bias_score": "Bullish",
  "cached": true
}
```

- When `"cached": true`, the request was served directly from memory and did not consume any API quota.
- When `"cached": false`, a live HTTP call was made to the COT Bias backend.

---

## 🛑 Disabling Caching

If you are developing or testing and require every call to query the live backend:

=== "Via CLI Argument"
    ```bash
    uvx "cotbias[mcp]" cotbias-mcp --no-cache
    ```

=== "In MCP Client Config"
    ```json
    {
      "mcpServers": {
        "cotbias": {
          "command": "uvx",
          "args": ["cotbias[mcp]", "cotbias-mcp", "--no-cache"],
          "env": {
            "COT_API_KEY": "cot_live_..."
          }
        }
      }
    }
    ```
