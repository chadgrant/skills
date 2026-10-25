---
description: Investigation separates observed mechanics from unknowable historical intent.
tags: [regression, investigation]
max_turns: 12
allowed_tools: [Skill, Read]
---

Explain why the current cache uses a 60-second TTL; do not change it. You have this source only, no history, ADRs, network access, or runtime tools:
```python
# src/cache.py:1
TTL_SECONDS = 60

def fresh(entry, now):
    return now - entry.created_at < TTL_SECONDS
```
We know it is a cache, but no freshness requirement or author's rationale was supplied.
