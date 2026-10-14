---
description: The reuse lens should prescribe a Decorator for the retry and timing code repeated around three calls, and the existing chunk() helper instead of the hand-written batching.
tags: [smoke, code-review]
max_turns: 10
allowed_tools: [Skill, Read]
---

Please review this change before I merge it. The first file is already in the repo; the second is new.

```ts
// src/utils/collections.ts (already in the repo)
export function chunk<T>(items: T[], size: number): T[][] {
  const out: T[][] = [];
  for (let i = 0; i < items.length; i += size) out.push(items.slice(i, i + size));
  return out;
}

// src/billing/invoiceService.ts (this change)
export class InvoiceService {
  constructor(private readonly api: BillingApi, private readonly log: Logger) {}

  async createInvoice(input: InvoiceInput): Promise<Invoice> {
    const started = Date.now();
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        const result = await this.api.createInvoice(input);
        this.log.info("createInvoice ok", { ms: Date.now() - started });
        return result;
      } catch (e) {
        this.log.warn("createInvoice failed", { attempt });
        if (attempt === 3) throw e;
      }
    }
    throw new Error("unreachable");
  }

  async voidInvoice(id: string): Promise<void> {
    const started = Date.now();
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        await this.api.voidInvoice(id);
        this.log.info("voidInvoice ok", { ms: Date.now() - started });
        return;
      } catch (e) {
        this.log.warn("voidInvoice failed", { attempt });
        if (attempt === 3) throw e;
      }
    }
  }

  async refundInvoice(id: string, cents: number): Promise<Refund> {
    const started = Date.now();
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        const refund = await this.api.refund(id, cents);
        this.log.info("refundInvoice ok", { ms: Date.now() - started });
        return refund;
      } catch (e) {
        this.log.warn("refundInvoice failed", { attempt });
        if (attempt === 3) throw e;
      }
    }
    throw new Error("unreachable");
  }

  batchIds(ids: string[]): string[][] {
    const batches: string[][] = [];
    for (let i = 0; i < ids.length; i += 50) batches.push(ids.slice(i, i + 50));
    return batches;
  }
}
```
