# Getting Started

Welcome to **cotbias**, the official Python client and Model Context Protocol (MCP) server for the [COT Bias Terminal](https://cot-bias-terminal.com) Quant API.

This guide walks you through account requirements, installation options, API key configuration, and your first request.

---

## 📋 Prerequisites

1. **Python 3.10 or higher**: Check your version with `python --version`.
2. **Quant Tier API Key**: Access to the programmatic API and MCP endpoints requires an active **Quant Tier** subscription from [COT Bias Terminal](https://cot-bias-terminal.com).

---

## 📦 Installation

Choose the installation option that best fits your workflow:

=== "Standard Python SDK (Batteries-Included)"
    Includes `pandas` and `httpx[http2]` for out-of-the-box quantitative analytics:
    ```bash
    pip install cotbias
    ```

=== "With MCP Server (For AI Agents)"
    Installs the Model Context Protocol server for Claude Desktop, Cursor IDE, or Cline:
    ```bash
    pip install "cotbias[mcp]"
    ```

=== "With Astral uv (Recommended for speed)"
    If you use `uv`:
    ```bash
    uv add cotbias
    # Or run the MCP server on-demand without installing into your local virtualenv:
    uvx "cotbias[mcp]" cotbias-mcp
    ```

---

## 🔑 Authentication

The client authenticates every request using the `X-API-Key` HTTP header.

### 1. Environment Variable (Recommended)

Set the `COT_API_KEY` environment variable in your terminal session or shell profile (`~/.zshrc`, `~/.bashrc`):

```bash
export COT_API_KEY="cot_live_your_actual_api_key_here"
```

If you use `.env` files in your project, load it using `python-dotenv`:

```python
from dotenv import load_dotenv
from cotbias import CotClient

load_dotenv()
# CotClient automatically reads COT_API_KEY from os.environ
client = CotClient()
```

### 2. Explicit Key Argument

Alternatively, pass the key directly when instantiating the client:

```python
from cotbias import CotClient

client = CotClient(api_key="cot_live_your_actual_api_key_here")
```

!!! tip "Security Best Practice"
    Never commit hardcoded API keys into version control. Use environment variables or secret managers (such as AWS Secrets Manager or GCP Secret Manager).

---

## 🛠 Client Lifecycle

### Using Context Managers (Recommended)

Both `CotClient` (synchronous) and `AsyncCotClient` (asynchronous) implement context managers. This ensures HTTP/2 connection pools and sockets are cleanly closed when done:

=== "Synchronous"
    ```python
    from cotbias import CotClient

    with CotClient() as client:
        snapshot = client.inference.get("ES")
        print(f"S&P 500 Bias: {snapshot.ai_bias_score}")
    # HTTP client connections are automatically closed here
    ```

=== "Asynchronous"
    ```python
    import asyncio
    from cotbias import AsyncCotClient


    async def main():
        async with AsyncCotClient() as client:
            snapshot = await client.inference.get("ES")
            print(f"S&P 500 Bias: {snapshot.ai_bias_score}")


    asyncio.run(main())
    ```

### Manual Connection Cleanup

If you maintain a long-running client instance (e.g. inside a Flask or FastAPI dependency container):

```python
client = CotClient()
try:
    data = client.markets.list()
finally:
    client.close()
```

---

## 🧪 Verifying Your Connection

Run this quick verification script to ensure your key and network connection are working properly:

```python
import os
from cotbias import CotClient
from cotbias.exceptions import AuthenticationError, PermissionDeniedError

try:
    with CotClient() as client:
        markets = client.markets.list(sector="Equity")
        print(f"✅ Success! Connected to COT Bias API. Found {len(markets)} equity contracts.")
        for m in markets[:3]:
            print(f"   - {m.symbol} ({m.name}): CFTC #{m.cftc_code}")

except AuthenticationError:
    print("❌ Authentication failed: Please verify your COT_API_KEY.")
except PermissionDeniedError:
    print("❌ Access denied: Your account requires an active Quant Tier subscription.")
except Exception as e:
    print(f"❌ Connection error: {e}")
```

---

## 🧭 Next Steps

- **[Timeseries Guide](sdk/timeseries.md)**: Query up to 156 weeks of historical positioning across Legacy, Disaggregated, and TFF reports.
- **[AI Inference Guide](sdk/inference.md)**: Interpret institutional market regimes, directional scores, and macro commentary.
- **[Multi-Market Screener](sdk/screener.md)**: Filter contracts by crowdedness risk, smart money accumulation, and momentum.
- **[MCP Server Setup](mcp/index.md)**: Connect COT positioning directly into Claude Desktop or Cursor IDE.
