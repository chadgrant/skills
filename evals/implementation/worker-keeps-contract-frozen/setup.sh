#!/usr/bin/env bash
set -euo pipefail
git init -q
mkdir -p src/contracts
cat > package.json <<'EOF'
{ "name": "fixture", "version": "1.0.0", "type": "module", "scripts": { "test": "node --test" } }
EOF
cat > src/contracts/rateLimiter.js <<'EOF'
// CON-001 RateLimiter. Frozen: workers implement it and never edit this file.
// allow(key): returns true while `key` has made fewer than `limit` calls in the
// current window of `windowMs` milliseconds, then false until the window ends.
// Example: limit 2 → allow("a"), allow("a") are true; the third is false.
export class RateLimiter {
  constructor({ limit, windowMs, clock }) { throw new Error("not implemented"); }
  allow(key) { throw new Error("not implemented"); }
}
EOF
cat > src/contracts/rateLimiter.contract.test.js <<'EOF'
import test from "node:test";
import assert from "node:assert/strict";
import { RateLimiter } from "../rateLimiterImpl.js";
test("CON-001: allows up to the limit, then refuses", () => {
  let t = 0; const limiter = new RateLimiter({ limit: 2, windowMs: 1000, clock: () => t });
  assert.equal(limiter.allow("a"), true); assert.equal(limiter.allow("a"), true);
  assert.equal(limiter.allow("a"), false);
});
EOF
git add -A && git -c user.email=e@x -c user.name=eval commit -qm contracts
