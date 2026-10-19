---
status: stub
---

# In-Memory Caching & Quota Protection

How `cotbias-mcp` protects your daily 2,000 requests/day API quota and accelerates agent responses using smart in-memory TTL caching.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Overview
Because CFTC Commitment of Traders data is published weekly on Fridays, frequent queries during an interactive AI conversation do not need to constantly hit the live backend API.

The MCP server maintains an internal in-memory cache:
- **Inference & Screener**: 5-minute TTL.
- **Timeseries & Markets Catalog**: 1-hour TTL.
- **In-flight Deduplication**: Simultaneous identical queries share the same upstream request.

## Roadmap & Upcoming Content
- [ ] Cache key structure and normalization.
- [ ] Cache hit headers and latency benefits.
- [ ] Disabling or tuning cache durations.
