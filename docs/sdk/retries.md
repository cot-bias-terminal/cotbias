# Retries & Resiliency

Network reliability is paramount when running automated trading bots and quantitative data feeds.

The `cotbias` SDK includes built-in retry middleware (`RetryTransport` and `AsyncRetryTransport`) with exponential backoff and randomized jitter to automatically absorb transient network interruptions without crashing your application.

---

## ⚡ Default Resiliency Behavior

By default, every instance of `CotClient` and `AsyncCotClient` is configured with:
- **`max_retries = 3`**: Up to three automatic retry attempts on transient failures.
- **`timeout = 30.0` seconds**: Per-request network timeout.
- **`http2 = True`**: Multiplexed HTTP/2 connection pooling.

```python
from cotbias import CotClient

# Customizing retry attempts and timeouts
client = CotClient(
    max_retries=5,  # Increase attempts for noisy cellular/satellite links
    timeout=10.0,  # Faster timeout threshold
)
```

To completely disable retries (e.g. for strict latency-sensitive dry runs):

```python
client = CotClient(max_retries=0)
```

---

## 🚦 Retriable vs Non-Retriable Status Codes

The SDK uses intelligent error classification to avoid useless retries that waste time and quota:

| HTTP Status / Condition | Retried? | Delay Logic | Rationale |
|---|---|---|---|
| **500, 502, 503, 504** | ✅ Yes | Exponential backoff + jitter | Upstream server glitch or brief redeployment restart. |
| **Network Timeout / Reset** | ✅ Yes | Exponential backoff + jitter | Transient packet loss or socket disconnect. |
| **Transient 429** (`Retry-After` $\le 10$s) | ✅ Yes | Respects `Retry-After` header | Short-term rate limit burst spike. |
| **Daily Quota 429** (`DAILY_LIMIT_EXCEEDED`) | ❌ No | Fails immediately | Quota exhausted until midnight UTC; retrying is futile. |
| **401 Unauthorized** | ❌ No | Fails immediately | Invalid or missing API key; retrying will never succeed. |
| **403 Forbidden** | ❌ No | Fails immediately | Insufficient tier access; requires subscription change. |
| **404 Not Found** | ❌ No | Fails immediately | Ticker symbol or report does not exist. |

---

## 📐 Exponential Backoff with Jitter

For retriable errors, the delay between attempts is calculated as:

$$\text{delay} = \text{backoff\_factor} \times 2^{\text{attempt} - 1} + \text{Uniform}(0, 0.1)$$

- **Attempt 1**: ~0.5s + jitter
- **Attempt 2**: ~1.0s + jitter
- **Attempt 3**: ~2.0s + jitter

The randomized **jitter** prevents "thundering herd" problems, where multiple concurrent processes hit an overloaded server simultaneously after a network blip.

---

## 🔍 Logging and Observability

The retry transport logs warnings to the standard `cotbias.retry` logger whenever an attempt is made:

```python
import logging
from cotbias import CotClient

# Enable retry logs in your console
logging.basicConfig(level=logging.INFO)
logging.getLogger("cotbias.retry").setLevel(logging.WARNING)

client = CotClient()
# If a transient error occurs, you will see:
# WARNING:cotbias.retry:Transient 503 received for https://api.cot-bias-terminal.com/timeseries/ES. Retrying in 0.54s (attempt 1/3)...
```
