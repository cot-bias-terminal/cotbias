---
status: stub
---

# AI Inference & Regimes

Extract AI-synthesized positioning regimes, directional bias scores, momentum indicators, crowdedness risks, and macro rationales.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Quick Reference

```python
from cotbias import CotClient

client = CotClient()
regime = client.inference.get("GC")  # Gold
print(regime.ai_bias_score, regime.cot_positioning_regime)
```

## Roadmap & Upcoming Content
- [ ] Interpretation of `ai_bias_score` (-100 to +100).
- [ ] Positioning regimes: Bullish Accumulation, Short Covering, Distribution, etc.
- [ ] Crowdedness risk score and dumb money index.
- [ ] Incorporating macro attribution commentary into quantitative models.
