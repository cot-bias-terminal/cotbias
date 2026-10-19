---
status: stub
---

# Markets Catalog

Discover all tracked futures contracts, symbols, CFTC commodity codes, and supported report types.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Quick Reference

```python
from cotbias import CotClient

client = CotClient()
all_markets = client.markets.list()
energy_markets = client.markets.list(sector="Commodity")
```

## Roadmap & Upcoming Content
- [ ] Contract catalog mapping (`symbol` to CFTC code).
- [ ] Sector breakdowns: Equity, Commodity, FX, Rates.
- [ ] Determining supported report types per contract.
