# Configuration & Advanced Options

This guide covers all client initialization options, environment variable defaults, enterprise network proxies, and custom SSL setups.

---

## 🌍 Environment Variables

You can configure global defaults for `cotbias` through environment variables:

| Environment Variable | Default Value | Description |
|---|---|---|
| `COT_API_KEY` | *None* | Your Quant Tier API key for authentication. |
| `COT_API_BASE_URL` | `https://api.cot-bias-terminal.com/v1` | Root API endpoint URL. |
| `COT_TIMEOUT_SEC` | `15.0` | Default socket timeout in seconds. |
| `COT_MAX_RETRIES` | `3` | Maximum automatic retries on transient errors. |

---

## 🛠 Client Constructor Arguments

Both `CotClient` and `AsyncCotClient` accept identical keyword arguments:

```python
from cotbias import CotClient

client = CotClient(
    api_key="cot_live_...",
    base_url="https://api.cot-bias-terminal.com/v1",
    timeout=20.0,
    max_retries=5,
    transport=None,
)
```

| Argument | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str | None` | `None` | API key. Falls back to `COT_API_KEY` in environment. |
| `base_url` | `str` | `DEFAULT_BASE_URL` | Base endpoint URL. Falls back to `COT_API_BASE_URL`. |
| `timeout` | `float` | `DEFAULT_TIMEOUT_SEC` | Socket connection and read timeout in seconds. |
| `max_retries` | `int` | `DEFAULT_MAX_RETRIES` | Number of retry attempts for 5xx/network errors. |
| `transport` | `httpx.BaseTransport | None` | `None` | Custom HTTP transport (sync) or `AsyncBaseTransport` (async). |

---

## 🏢 Enterprise Networking & Proxies

### 1. HTTP/HTTPS Corporate Proxies

If your trading environment operates behind a corporate forward proxy, pass a custom `httpx.HTTPTransport`:

=== "Synchronous Client"
    ```python
    import httpx
    from cotbias import CotClient

    proxy_transport = httpx.HTTPTransport(
        proxy="http://proxy.corporate.internal:8080",
        http2=True,
    )

    client = CotClient(transport=proxy_transport)
    ```

=== "Asynchronous Client"
    ```python
    import httpx
    from cotbias import AsyncCotClient

    async_proxy_transport = httpx.AsyncHTTPTransport(
        proxy="http://proxy.corporate.internal:8080",
        http2=True,
    )

    client = AsyncCotClient(transport=async_proxy_transport)
    ```

### 2. Custom SSL Certificates / Internal CA

To trust private enterprise root certificates:

```python
import httpx
from cotbias import CotClient

custom_ssl_transport = httpx.HTTPTransport(
    verify="/etc/ssl/certs/corporate-internal-ca.pem",
    http2=True,
)

client = CotClient(transport=custom_ssl_transport)
```

---

## 🔒 Custom Request Headers

The client automatically sets `Accept: application/json` and sends a descriptive `User-Agent` (`cotbias-python/<version>`). All requests include `X-API-Key`.
