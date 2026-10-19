---
status: stub
---

# Retries & Timeouts

Understand `cotbias`'s built-in resiliency features: exponential backoff, jitter, and timeout configuration.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Quick Reference

```python
from cotbias import CotClient

# Customize retry count and timeout
client = CotClient(
    max_retries=5,
    timeout=15.0,
)
```

## Resiliency Policies
- **Automatic Retries**: By default, `cotbias` retries up to 3 times with exponential backoff on transient network timeouts and HTTP 5xx errors.
- **Client Errors**: HTTP 400, 401, 403, and 404 errors fail immediately with descriptive exceptions and are never retried.
- **Rate Limits (429)**: Quota-exhausted errors raise immediately, while transient rate spikes are handled gracefully.

## Roadmap & Upcoming Content
- [ ] Configuring `max_retries` and `timeout`.
- [ ] Jitter algorithms and backoff timing math.
- [ ] Custom HTTP transports.
