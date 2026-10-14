---
description: A scoped review covers the named file; a bug noticed in a neighbouring file gets at most one Outside scope line.
tags: [smoke, code-review]
max_turns: 10
allowed_tools: [Skill, Read]
---

Review only `src/cart/total.ts` from this change. `src/legacy/report.ts` is shown for context because total.ts calls it.

```ts
// src/cart/total.ts (this change)
import { roundCents } from "../legacy/report";

export function cartTotal(lines: { priceCents: number; qty: number }[]): number {
  return roundCents(lines.reduce((sum, l) => sum + l.priceCents * l.qty, 0));
}

// src/legacy/report.ts (unchanged, context only)
export function roundCents(n: number): number { return Math.round(n); }
export function buildReport(userInput: string, db: Db) {
  return db.query("SELECT * FROM reports WHERE owner = '" + userInput + "'");
}
```
