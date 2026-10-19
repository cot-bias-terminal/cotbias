# Changelog

All notable changes to the `cotbias` library are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.2] - 2026-10-19

### Added
- Comprehensive Google-style docstrings and type annotations across `CotClient`, `AsyncCotClient`, resources, models, exceptions, retry transports, and MCP server.
- MkDocs documentation suite hosted via GitHub Pages with auto-generated API references.
- Identity guardrails in pre-commit and GitHub Actions CI.

---

## [0.2.1] - 2026-10-19

### Changed
- Packaged `pandas` as a core dependency for out-of-the-box DataFrame support (`client.timeseries.get(..., as_dataframe=True)`).
- Made `mcp` an optional dependency (`pip install "cotbias[mcp]"`).

---

## [0.2.0] - 2026-10-19

### Added
- Official release of `cotbias` SDK and MCP Server.
- Synchronous and asynchronous API clients (`CotClient`, `AsyncCotClient`).
- Resource endpoints:
  - `client.timeseries`: 156-week positioning data across Legacy, Disaggregated, TFF, and CIT reports.
  - `client.inference`: AI market regimes, directional bias, and macro attribution.
  - `client.screener`: Cross-market positioning scans.
  - `client.markets`: Contract catalogs and CFTC code resolution.
- Enterprise reliability features:
  - Built-in `RetryTransport` with exponential backoff and jitter for transient 5xx and timeout errors.
  - Strict Pydantic models with `extra="allow"` to protect against upstream schema drift.
- Model Context Protocol (MCP) Server:
  - `cotbias-mcp` CLI entrypoint.
  - Tools: `get_market_snapshot`, `get_ai_inference`, `get_timeseries`, `scan_markets`, `list_markets`.
  - In-memory TTL caching (5m for inference/screener, 1h for timeseries).
  - Prompts and resources for Claude Desktop and Cursor IDE.
