---
description: A scoped review follows a changed wire contract into an unchanged consumer without auditing unrelated code.
tags: [regression, code-review]
max_turns: 12
allowed_tools: [Skill, Read]
---

Review this diff only. The public API contract promises `totalCents` as an integer; clients are independently deployed. No schema migration was approved.

```diff
// src/api/cart.ts, line 12
-return { totalCents: 1250 };
+return { total: 12.50 };
```

Unchanged consumer `clients/receipt.ts`, line 8:
```ts
export const receipt = (response) => `$${(response.totalCents / 100).toFixed(2)}`;
```

Unrelated unchanged `legacy/search.ts` concatenates user input into SQL. It is not reachable from this change. These snippets are the complete available evidence; do not invent executed tests.
