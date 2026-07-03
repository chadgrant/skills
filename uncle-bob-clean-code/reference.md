# Uncle Bob Reference — Clean Code and SOLID in Full

Distilled from Robert C. Martin's *Clean Code*, *The Clean Coder*, *Clean Architecture*, and *Agile Software Development: Principles, Patterns, and Practices*. Load this when you need the detail behind a rule in SKILL.md.

## Meaningful Names (Clean Code ch. 2)

- **Intention-revealing:** the name answers why it exists, what it does, how it's used. If a name needs a comment, the name failed.
- **Avoid disinformation:** don't call it `accountList` unless it's actually a List; avoid names that vary in small ways (`XYZControllerForEfficientHandlingOfStrings` vs `...StorageOfStrings`).
- **Meaningful distinctions:** `a1`/`a2`, `ProductInfo` vs `ProductData` — noise words distinguish nothing.
- **Pronounceable and searchable:** `generationTimestamp`, not `genymdhms`. Single-letter names are grep-proof.
- **No encodings:** no Hungarian notation, no `m_` prefixes, no `IShape` interface prefixes.
- **Classes: noun phrases** (`Customer`, `WikiPage`, `AddressParser`). Avoid `Manager`, `Processor`, `Data`, `Info` — they're signs the class has no single responsibility.
- **Methods: verb phrases** (`postPayment`, `deletePage`, `save`). Accessors `get`, mutators `set`, predicates `is`/`has`.
- **One word per concept:** pick `fetch` or `retrieve` or `get` for the codebase, then never mix them.
- **Solution-domain names first** (algorithm/pattern terms programmers know), problem-domain names when no technical term fits.

## Functions (Clean Code ch. 3)

- **Small.** Rarely 20 lines; often under 10. Blocks inside `if`/`else`/`while` should be one line — usually a function call.
- **Do one thing.** Test: can you extract another function from it with a name that isn't a restatement of its implementation? Then it does more than one thing.
- **One level of abstraction per function.** Don't mix `getHtml()` with `.append("\n")` in the same body. Code should read top-down like a set of TO paragraphs, each describing the level below.
- **Switch statements:** allowed once, in a low-level factory that creates polymorphic objects — never repeated across the codebase (that's an OCP/SRP violation).
- **Arguments:** zero is best, one and two fine, three needs justification. More than three: wrap them in an object — if they travel together they're a concept (`Circle(center, radius)` not `Circle(x, y, radius)`).
- **No flag arguments.** `render(true)` is a promise the function does two things. Write `renderForSuite()` and `renderForSingleTest()`.
- **No side effects.** `checkPassword()` that also initializes a session lies about what it does. If it must change state, the name must say so.
- **Command–query separation:** `set("username", "bob")` returning a boolean invites `if (set(...))` — is that "was it set?" or "did it succeed?" Do, or answer, never both.
- **No output arguments.** `appendFooter(report)` — is report the source or the target? Make it `report.appendFooter()`.
- **DRY:** duplication is the root of most evil in software. Every repeated block is a missed abstraction.

## Comments (Clean Code ch. 4)

- "Don't comment bad code — rewrite it." Comments are a compensation for failure to express intent in code, and they rot: code changes, comments don't.
- **Good comments:** legal headers, explanation of intent ("we sort here because the downstream API requires it"), warnings ("takes 20 min to run"), TODO with a plan, amplification of something that looks wrong but isn't, docs on public APIs.
- **Bad comments:** restating the code (`i++; // increment i`), journal entries, noise (`// default constructor`), position markers (`// ---- utilities ----`), closing-brace comments, attributions (git knows), HTML in comments.
- **Commented-out code: delete it, always.** Version control remembers. Others won't dare delete it, so it accumulates like sediment.

## Formatting (Clean Code ch. 5)

- **Vertical:** newspaper metaphor — high-level at top, detail below. Blank lines separate concepts; related lines stay dense. Declare variables near use; called functions below their callers.
- **Horizontal:** don't force readers to scroll sideways. Indentation reflects scope hierarchy — never collapse it to fit one line.
- **Team rules win:** whatever the codebase's formatter/config says, follow it. Consistency beats preference.

## Objects and Data Structures (Clean Code ch. 6)

- **Objects** hide data behind behavior; **data structures** expose data and have no behavior. Both are fine — hybrids are not.
- **Law of Demeter:** a method should talk only to its own fields, its parameters, objects it creates, and its immediate collaborators. `ctxt.getOptions().getScratchDir().getAbsolutePath()` is a train wreck — the caller knows three layers of structure it has no business knowing. Ask for what you need: `ctxt.createScratchFileStream(name)`.
- **Tell, don't ask:** instead of interrogating an object's state and deciding for it, tell it what to do.

## Error Handling (Clean Code ch. 7)

- **Exceptions, not return codes.** Return codes force the caller to check immediately and clutter the happy path; they're also ignorable — silently.
- **Write the try-catch-finally first** when code can fail: it defines a transactional scope.
- **Provide context:** every exception carries what operation failed and why.
- **Define exceptions by caller's needs** — wrap third-party APIs so one exception type represents "the port failed" rather than leaking vendor exception taxonomies.
- **Special Case pattern:** instead of null + if-checks, return an object that represents the empty case (`Collections.emptyList()`, a `NullEmployee` whose pay is zero).
- **Don't return null.** Every null return creates a landmine for callers; one missing check = NullPointerException in production.
- **Don't pass null.** No rational caller-side meaning; forbid it by policy and validate at boundaries.

## Boundaries (Clean Code ch. 8)

- Wrap third-party APIs in your own interface: you control the seam, tests get a fake for free, and vendor churn stays in one file.
- **Learning tests:** encode your understanding of a third-party library as tests, so upgrades tell you when behavior shifted.

## Unit Tests (Clean Code ch. 9)

- **Three Laws of TDD:** (1) write no production code except to pass a failing test; (2) write no more of a test than suffices to fail; (3) write no more production code than suffices to pass.
- **Tests are first-class code.** Dirty tests rot, then get deleted, then the production code they guarded rots too. Test code gets the same naming and decomposition standards.
- **One assert-concept per test.** BUILD-OPERATE-CHECK / Arrange-Act-Assert structure.
- **FIRST:** Fast (or nobody runs them), Independent (no ordering dependencies), Repeatable (any environment), Self-validating (boolean pass/fail, no log-reading), Timely (written just before the production code).

## Classes (Clean Code ch. 10)

- **Small, measured in responsibilities.** If you can't name the class without "And", "Manager", or "Processor", it has too many.
- **SRP:** one reason to change. Describe the class in ~25 words without "and/or/but".
- **Cohesion:** methods should use the class's variables. Low cohesion = classes hiding inside, trying to get out.
- **Organize for change:** isolate what varies. Depend on interfaces where change is expected.

## SOLID (Agile Software Development / Clean Architecture)

### SRP — Single Responsibility
A module has one, and only one, reason to change — one actor it answers to.
```python
# Violation: three actors (finance, DBA, ops) share one class
class Employee:
    def calculate_pay(self): ...
    def save(self): ...
    def report_hours(self): ...

# Fix: one class per responsibility, a facade if callers want one entry point
class PayCalculator: ...
class EmployeeRepository: ...
class HoursReporter: ...
```

### OCP — Open-Closed
Open for extension, closed for modification: add behavior by adding code, not by editing working code. The trigger is the *second* occurrence of a type-switch, not speculation about one.
```python
# Violation: every new customer tier edits this function (and its twin in invoicing, and…)
if cust.type == 'gold': total *= 0.85
elif cust.type == 'silver': total *= 0.90

# Fix: the policy varies, so make it a seam
DISCOUNTS = {'gold': 0.15, 'silver': 0.10}   # data-driven…
total *= 1 - DISCOUNTS.get(cust.type, 0)
# …or polymorphic (Strategy) when tiers grow behavior beyond a number
```

### LSP — Liskov Substitution
Any code holding a base-type reference must work, unsurprised, with every subtype. Subtypes may not strengthen preconditions, weaken postconditions, or throw where the base succeeds.
```python
# Violation: Square-extends-Rectangle — setWidth breaks area expectations.
# Violation: an override that raises for inputs the parent accepts.
# Fix: if it isn't substitutable, it isn't a subtype — compose instead.
```

### ISP — Interface Segregation
No client should depend on methods it doesn't use. Fat interfaces force recompiles/redeploys (and stub methods) on everyone.
```python
# Violation: Worker interface with work() + eat(); robots implement eat() as pass
# Fix: Workable, Feedable — clients depend only on what they call
```

### DIP — Dependency Inversion
High-level policy must not depend on low-level detail; both depend on abstractions. Details (DB, web, frameworks) point inward at the policy, never the reverse.
```python
# Violation: OrderService constructs its own PostgresClient and SmtpMailer
# Fix: OrderService takes repository/notifier abstractions in the constructor;
#      main() wires the concretions. Tests wire fakes.
```

## Code Smells (Clean Code ch. 17, selected)

**Rigidity** — one change forces a cascade of changes. **Fragility** — a change breaks unrelated parts. **Immobility** — you can't reuse a piece without dragging its world along. **Needless complexity** — abstraction with no current payoff. **Needless repetition** — the same code shape everywhere (missed abstraction). **Opacity** — code that resists understanding.

Function-level: too many arguments, output arguments, flag arguments, dead functions, duplicated switch chains, feature envy (method more interested in another class's data than its own), inappropriate static, misplaced responsibility, magic numbers, negative conditionals (`if (!buffer.shouldNotCompact())`).

## The Clean Coder — professional conduct

- Say no when the schedule demands broken code; offer what you CAN deliver instead.
- "Later" is a lie you tell yourself. QA is not your safety net.
- The Boy Scout Rule is continuous: every commit leaves the touched files slightly better — a rename, an extraction, a deleted dead line. Not a rewrite.

## Worked Example — before/after

```js
// BEFORE: one function, five jobs, unreadable at review speed
function handleOrder(o) {
  if (o != null && o.items != null && o.items.length > 0 && o.total > 0) {
    let d = 0;
    if (o.tier == 'gold') d = o.total * 0.15;
    else if (o.tier == 'silver') d = o.total * 0.1;
    else if (o.total > 100) d = o.total * 0.05;
    o.total = o.total - d;
    let r = 0.06;
    if (o.state == 'CA') r = 0.0825;
    else if (o.state == 'NY') r = 0.08875;
    o.tax = Math.round(o.total * r * 100) / 100;
    o.total = Math.round((o.total + o.tax) * 100) / 100;
    db.save(o);
    mailer.send(o.email, 'order confirmed', 'total is $' + o.total);
    return 0;
  } else { return -1; }
}
```

```js
// AFTER: reads like the spec; each function testable alone; same line count ±10%
const TIER_DISCOUNTS = { gold: 0.15, silver: 0.10 };
const STANDARD_DISCOUNT = 0.05;
const STANDARD_DISCOUNT_MINIMUM = 100;
const TAX_RATES = { CA: 0.0825, NY: 0.08875 };
const DEFAULT_TAX_RATE = 0.06;

async function processOrder(order) {
  validateOrder(order);
  const discounted = order.total - discountFor(order);
  const tax = roundToCents(discounted * taxRateFor(order.state));
  const total = roundToCents(discounted + tax);
  const processed = { ...order, tax, total };
  await db.save(processed);
  await sendConfirmation(processed);
  return processed;
}

function validateOrder(order) {
  if (!order?.items?.length) throw new Error('Order must contain items');
  if (!(order.total > 0)) throw new Error(`Order total must be positive, got ${order?.total}`);
}

function discountFor({ tier, total }) {
  const rate = TIER_DISCOUNTS[tier] ?? (total > STANDARD_DISCOUNT_MINIMUM ? STANDARD_DISCOUNT : 0);
  return total * rate;
}

function taxRateFor(state) { return TAX_RATES[state] ?? DEFAULT_TAX_RATE; }
function roundToCents(amount) { return Math.round(amount * 100) / 100; }
function sendConfirmation({ email, total }) {
  return mailer.send(email, 'order confirmed', `your order total is $${total.toFixed(2)}`);
}
```

What changed and which rule drove it: extraction to one-level-of-abstraction (`processOrder` reads as the spec); intention-revealing names replace `o`/`d`/`r`; magic numbers named; exceptions with context replace `-1`/`0`; input no longer mutated; the tier/state tables are OCP seams — the next tier is a data edit, not a logic edit. Note what did NOT happen: no classes, no interfaces, no Strategy pattern — the over-apply table applies.
