---
description: Compaction folds amendments into the requirement they change, retires the replaced ID, and leaves no change log.
tags: [planning, writes]
max_turns: 20
allowed_tools: [Skill, Read, Write, Edit]
---

Our PRD has turned into a change log. Compact the requirements and write the result to `docs/requirements/prd.md`.

```markdown
# PRD — Rate-limited API

## Requirements
- REQ-010: Every API key is limited to 60 requests per minute.
- REQ-011: A request over the limit gets HTTP 429 with a Retry-After header.
- REQ-012: Limits are tracked per API key in Redis.

UPDATE (2026-08-02): REQ-010 limit raised to 100 requests per minute for paid plans; free plans stay at 60.
- REQ-013: ~~Admins can see a usage dashboard.~~ Dropped, use Grafana instead.
- REQ-014: Amends REQ-011: the 429 body is JSON `{ "error": "rate_limited", "retryAfterSeconds": n }`.

## Change log
| Date | Change |
|---|---|
| 2026-07-10 | Initial |
| 2026-08-02 | Paid plans get 100/min |
| 2026-08-20 | Dashboard dropped; 429 body defined |
```
