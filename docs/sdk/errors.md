---
status: stub
---

# Error Handling

Diagnose and handle API exceptions cleanly within your applications.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Exception Hierarchy

All exceptions inherit from `CotApiError`:

- `CotApiError`: Base exception for all API errors.
  - `AuthenticationError`: Raised on 401 Unauthorized (invalid or missing API key).
  - `PermissionDeniedError`: Raised on 403 Forbidden (insufficient subscription tier).
  - `NotFoundError`: Raised on 404 Not Found (invalid market symbol or missing report).
  - `RateLimitError`: Raised on 429 Too Many Requests.
  - `ServerError`: Raised on 5xx upstream server errors.

## Example Handling

```python
from cotbias import CotClient
from cotbias.exceptions import AuthenticationError, RateLimitError, CotApiError

client = CotClient()

try:
    data = client.inference.get("INVALID_TICKER")
except AuthenticationError:
    print("Invalid COT_API_KEY")
except RateLimitError as e:
    print(f"Rate limited: {e.message}")
except CotApiError as e:
    print(f"API Error ({e.status_code}): {e.message}")
```

## Roadmap & Upcoming Content
- [ ] Inspecting error responses and status codes.
- [ ] Handling rate limits and quota resets.
- [ ] Best practices for alerting and error logging.
