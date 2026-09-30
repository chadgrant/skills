---
name: design-patterns
description: Use when a recurring design problem appears while structuring code: a growing conditional, swappable behavior, complex construction, adapting an interface, or deciding where domain logic, data access, or the web layer lives. Triggers: "which pattern", "GoF", "PoEAA", "strategy vs state", "repository vs active record", "service layer".
---

# Design patterns

Announce at the start: **"Using design-patterns: name the problem → match a known pattern → apply its minimal form → or reject it if the problem isn't there."**

**Core principle: a pattern is a named solution to a recurring problem: vocabulary, not decoration.** You reach for one because you *have* the problem it solves, never because it would look sophisticated. The catalog stops you reinventing a solved wheel and gives a name two engineers can say out loud ("that's a Strategy"). This skill is the recognition layer; the full catalogs are in [reference.md](reference.md).

## How to use a pattern (the discipline)

1. **State the problem first, in plain terms.** "This function switches on a type code and a third case is coming." Not "I want to use a pattern." If you can't name the problem without naming the pattern, you don't have the problem yet.
2. **Match it to a known solution.** Scan [reference.md](reference.md) for the pattern whose *intent* matches your problem and whose *smell it cures* is the smell you actually have.
3. **Apply the minimal form.** Implement the smallest version that solves today's problem. A Strategy is an interface and two implementers — not a factory-of-factories. Patterns are extensible by design; add the machinery when the second real case arrives (that is OCP's moment, per `uncle-bob-clean-code`).
4. **Name it in the code and the docs.** Call the class `RetryStrategy`, cite the pattern in the `ADR` when it's an architectural choice. The name is half the value.
5. **Or reject it.** If the recurring problem isn't actually recurring, the pattern is speculative generality — a smell, not a solution. Stop.

## Choosing among the common forks

The catalog is large; most real decisions are one of a few forks. Full detail in [reference.md](reference.md).

| When you're deciding… | The fork |
|---|---|
| Behavior varies by a value/type, and cases are growing | **Strategy** (caller picks behavior) vs **State** (object changes its own behavior as it transitions) vs replace-conditional-with-**polymorphism** if it's just type-based branching |
| Something must happen when state changes, to N interested parties | **Observer** (in-process) vs a domain event (`domain-driven-design`) vs a message/queue (cross-service) |
| Construction is complex or must vary | **Factory Method** (subclass decides) vs **Abstract Factory** (families of products) vs **Builder** (many optional parts) — plain constructor if none of those apply |
| You need to adapt or hide an interface | **Adapter** (make incompatible fit) vs **Facade** (simplify a subsystem) vs **Proxy** (control access / lazy / remote) |
| Where does the business logic live? | **Transaction Script** (simple, procedural) vs **Domain Model** (rich, OO — pairs with `domain-driven-design`) vs **Table Module** (one class per table) — scale with complexity, don't default to the richest |
| How do objects reach the database? | **Active Record** (object = row, logic + persistence together; good for simple domains) vs **Data Mapper** + **Repository** (domain ignorant of storage; needed once the model is rich) |
| Structuring the web/request layer | **MVC** + **Page/Front Controller** + **Template View**; a **Service Layer** as the app's boundary API |

## Red flags: don't over-apply

Needless patterns are the most common way a codebase gets worse under the banner of "good design".

| Thought | Reality |
|---|---|
| "Add a pattern to make it extensible." / "The code looks too plain." | Extensible for *what*? Name the second real case. One implementer and no second case is speculative generality, not OCP. |
| "Abstract Factory / Builder for this two-field object." | A constructor is the pattern. Creational patterns are for construction that genuinely varies or is genuinely complex. |
| "A Singleton so everything can get at it." | Global mutable state with a nicer name; it wrecks testability. Inject it; wire one instance at the composition root. |
| "MVC + Service Layer + Repository on a 200-line CRUD app." | Enterprise patterns earn their keep at enterprise complexity. Transaction Script + Active Record is the honest choice. |
| "Active Record everywhere, it's simplest." | Until the domain gets rich and persistence tangles with business rules. Then Data Mapper + Repository. Match the pattern to the domain's complexity. |
| "A Visitor because there are a few types." | Visitor pays off when operations change often over a *stable* type hierarchy. If the types churn, it's a tax. |
| "It's basically a Strategy and a State and a Command…" | If three patterns 'basically' fit, you haven't named the problem. One problem, one pattern. |
| "This conditional is fine, I'll add the fourth branch." | Growing switch-on-type is the textbook trigger for Strategy / State / polymorphism. Reach for it now, via `refactoring`. |

---

*Distilled from the **Gang of Four** and **Fowler**'s *Patterns of Enterprise Application Architecture*. Related: `uncle-bob-clean-code` (patterns are SOLID made concrete), `domain-driven-design` (tactical DDD is enterprise patterns on a domain model), `refactoring` (how you move to a pattern under green tests). Catalogs in [reference.md](reference.md).*
