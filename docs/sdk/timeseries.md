---
status: stub
---

# Timeseries Data Guide

Fetch up to 156 weeks of historical positioning data across four CFTC report families: Legacy, Disaggregated, Financial Traders (TFF), and Commodity Index (CIT).

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Quick Reference

```python
from cotbias import CotClient

client = CotClient()
# Returns a Pandas DataFrame with 52 weeks of historical metrics
df = client.timeseries.get("ES", lookback_weeks=52, as_dataframe=True)
```

## Roadmap & Upcoming Content
- [ ] CFTC Report Family distinctions (Legacy vs Disaggregated vs TFF vs CIT).
- [ ] Key metrics deep-dive: COT Index (26w, 52w), 3-year Z-scores, concentration ratios, and hedging pressure.
- [ ] Pydantic models vs Pandas DataFrames.
- [ ] Contract types (Combined vs Futures-only).
- [ ] Pagination and lookback limits.
