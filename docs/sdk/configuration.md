---
status: stub
---

# Configuration

Detailed reference for all client initialization parameters and environment variables.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `COT_API_KEY` | None | Quant Tier API authentication key. |
| `COT_API_URL` | `https://api.cot-bias-terminal.com` | Base URL for the COT Bias Terminal API. |
| `COT_TIMEOUT` | `30.0` | Default request timeout in seconds. |

## Client Parameters

Both `CotClient` and `AsyncCotClient` accept the following arguments:

- `api_key: Optional[str]`: API key (falls back to `COT_API_KEY`).
- `base_url: Optional[str]`: Base URL (falls back to `COT_API_URL`).
- `timeout: float`: Timeout in seconds (default `30.0`).
- `max_retries: int`: Maximum retry attempts for transient errors (default `3`).
- `http2: bool`: Enable HTTP/2 protocol support (default `True`).

## Roadmap & Upcoming Content
- [ ] Enterprise proxy configurations (`http_proxy`, `https_proxy`).
- [ ] Custom SSL context injection.
- [ ] Custom httpx client injection.
