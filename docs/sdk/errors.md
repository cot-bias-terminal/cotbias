# Error Handling

When an API call cannot be fulfilled, the `cotbias` SDK converts raw HTTP responses into clean, strongly typed Python exceptions.

All client exceptions inherit from :class:`~cotbias.exceptions.CotApiError`, allowing you to catch errors at either a granular or general level.

---

## 🌳 Exception Hierarchy

```text
Exception
 └── CotApiError (Base exception for all API failures)
      ├── AuthenticationError      (HTTP 401 - Invalid/missing API key)
      ├── PermissionDeniedError    (HTTP 403 - Tier access denied)
      ├── NotFoundError            (HTTP 404 - Unknown market or resource)
      ├── RateLimitExceededError   (HTTP 429 - Rate limit / quota exhausted)
      └── ServerError              (HTTP 5xx - Upstream server error)
```

---

## 🛠 Exception Descriptions

| Exception Class | HTTP Status | Common Cause | Recommended Action |
|---|---|---|---|
| `AuthenticationError` | 401 | Missing, malformed, or expired `COT_API_KEY`. | Verify the key in environment variables or client constructor. |
| `PermissionDeniedError` | 403 | Account does not have Quant Tier API privileges. | Upgrade account tier at [cot-bias-terminal.com](https://cot-bias-terminal.com). |
| `NotFoundError` | 404 | Symbol or report family not found in the COT universe. | Call `client.markets.list()` to check valid symbols. |
| `RateLimitExceededError` | 429 | Exceeded 2,000 requests/day quota or burst limit. | Inspect `e.retry_after` or wait for daily reset. |
| `ServerError` | 500+ | Temporary backend maintenance or database timeout. | Handled automatically by retry middleware. |

---

## 🔍 Inspecting Error Attributes

All `CotApiError` exceptions provide rich attributes for logging and alerting:

```python
from cotbias import CotClient
from cotbias.exceptions import CotApiError, RateLimitExceededError

with CotClient() as client:
    try:
        data = client.inference.get("NONEXISTENT_TICKER")
    except RateLimitExceededError as e:
        print(f"Rate limited! Wait {e.retry_after} seconds.")
        print(f"Error code: {e.code}")
    except CotApiError as e:
        print(f"API Error ({e.status_code}): {e.message}")
        print(f"Machine code: {e.code}")
        print(f"Raw response: {e.response_body}")
```

---

## 🛡 Production Error Handling Pattern

Here is a recommended pattern for automated production trading services:

```python
import logging
import time
from cotbias import CotClient
from cotbias.exceptions import (
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    RateLimitExceededError,
    ServerError,
    CotApiError,
)

logger = logging.getLogger("trading_bot")


def fetch_market_safe(client: CotClient, symbol: str):
    try:
        return client.inference.get(symbol)
    except AuthenticationError:
        logger.critical("FATAL: Invalid COT_API_KEY. Shutting down worker.")
        raise
    except PermissionDeniedError:
        logger.error("Subscription lacks Quant Tier API access.")
        return None
    except NotFoundError:
        logger.warning("Market '%s' not tracked in CFTC universe. Skipping.", symbol)
        return None
    except RateLimitExceededError as e:
        logger.warning("Daily quota reached. Sleeping for %d seconds...", e.retry_after)
        time.sleep(e.retry_after)
        return None
    except ServerError as e:
        logger.error("Upstream COT Bias server error after all retries: %s", e)
        return None
    except CotApiError as e:
        logger.error("Unexpected API error: %s", e)
        return None
```
