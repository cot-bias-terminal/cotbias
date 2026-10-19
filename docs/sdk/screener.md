---
status: stub
---

# Multi-Market Screener

Screen across 60+ commodities, equity indices, foreign exchange currencies, and interest rates using institutional positioning thresholds.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Quick Reference

```python
from cotbias import CotClient

client = CotClient()
# Screen for bullish markets with low crowdedness
results = client.screener.scan(
    ai_bias_score="Bullish",
    crowdedness_risk="Low",
)
```

## Roadmap & Upcoming Content
- [ ] Filter criteria: `ai_bias_score`, `crowdedness_risk`, `momentum`, `cot_positioning`.
- [ ] Sorting and batch analysis across asset classes.
- [ ] Working with screener results in automated trading pipelines.
