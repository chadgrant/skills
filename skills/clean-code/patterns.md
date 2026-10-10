# Design patterns

**Core principle: a pattern is a named solution to a recurring problem: vocabulary, not decoration.** You reach for one because you *have* the problem it solves, never because it would look sophisticated. The catalog stops you reinventing a solved wheel and gives a name two engineers can say out loud ("that's a Strategy"). The full catalogs are below.

## How to use a pattern (the discipline)

1. **State the problem first, in plain terms.** "This function switches on a type code and a third case is coming." Not "I want to use a pattern." If you can't name the problem without naming the pattern, you don't have the problem yet.
2. **Match it to a known solution.** Scan the catalog below for the pattern whose *intent* matches your problem and whose *smell it cures* is the smell you actually have.
3. **Apply the minimal form.** Implement the smallest version that solves today's problem. A Strategy is an interface and two implementers — not a factory-of-factories. Patterns are extensible by design; add the machinery when the second real case arrives (that is OCP's moment, per [SKILL.md](SKILL.md)).
4. **Name it in the code and the docs.** Call the class `RetryStrategy`, cite the pattern in the `ADR` when it's an architectural choice. The name is half the value.
5. **Check the convention first.** If the framework already supplies the pattern (its ORM's repository, its middleware chain, its event bus), use the framework's version; a parallel home-made one breaks convention over configuration.
6. **Or reject it.** If the recurring problem isn't actually recurring, the pattern is speculative generality — a smell, not a solution. Stop.

The four simplicity rules in [SKILL.md](SKILL.md) gate every pattern. KISS and YAGNI say when not to reach for one; DRY is often why you do (a Decorator or Template Method gives repeated wrapping logic one home); convention over configuration says whose version to use.

## Choosing among the common forks

The catalog is large; most real decisions are one of a few forks. Full detail in the catalog below.

| When you're deciding… | The fork |
|---|---|
| Behavior varies by a value/type, and cases are growing | **Strategy** (caller picks behavior) vs **State** (object changes its own behavior as it transitions) vs replace-conditional-with-**polymorphism** if it's just type-based branching |
| Something must happen when state changes, to N interested parties | **Observer** (in-process) vs a domain event ([domain-driven-design.md](domain-driven-design.md)) vs a message/queue (cross-service) |
| Construction is complex or must vary | **Factory Method** (subclass decides) vs **Abstract Factory** (families of products) vs **Builder** (many optional parts) — plain constructor if none of those apply |
| You need to adapt or hide an interface | **Adapter** (make incompatible fit) vs **Facade** (simplify a subsystem) vs **Proxy** (control access / lazy / remote) |
| Where does the business logic live? | **Transaction Script** (simple, procedural) vs **Domain Model** (rich, OO — pairs with [domain-driven-design.md](domain-driven-design.md)) vs **Table Module** (one class per table) — scale with complexity, don't default to the richest |
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
| "This conditional is fine, I'll add the fourth branch." | Growing switch-on-type is the textbook trigger for Strategy / State / polymorphism. Reach for it now, via [refactoring.md](refactoring.md). |

---

## Catalog

## Gang of Four — Creational

*How objects get made, decoupling construction from use.*

| Pattern | Intent | When it fits | Don't use when |
|---|---|---|---|
| **Factory Method** | Defer which class to instantiate to a subclass | A base class can't know the concrete type it needs; subclasses decide | A constructor or a simple function does it — no varying type |
| **Abstract Factory** | Create *families* of related products without naming concretions | You swap a whole related set at once (e.g. a UI toolkit, a cloud provider's clients) | You have one product, not a family |
| **Builder** | Construct a complex object step by step; separate construction from representation | Many optional parts, or the same steps build different representations | Few fields — use a constructor or named args |
| **Prototype** | Create new objects by cloning an existing one | Instantiation is expensive and a configured exemplar exists to copy | Construction is cheap and clear |
| **Singleton** | Guarantee one instance, global access | *Almost never — see below* | Nearly always. Prefer one instance wired at the composition root + injected (DIP) |

> **Singleton warning:** it is global mutable state, which breaks testability and hides dependencies. "I need exactly one" is a *lifetime* concern — solve it by constructing one at the composition root and injecting it, not by a Singleton.

## Gang of Four — Structural

*How objects and classes compose into larger structures.*

| Pattern | Intent | When it fits | Don't use when |
|---|---|---|---|
| **Adapter** | Make an incompatible interface fit the one a client expects | Wrapping a third-party/legacy API to your interface | You control both sides — just change the interface |
| **Bridge** | Split an abstraction from its implementation so both vary independently | Two dimensions of variation multiply (shape × renderer) | Only one dimension varies |
| **Composite** | Treat individual objects and compositions uniformly (trees) | Part-whole hierarchies: files/folders, UI nodes, org charts | The structure isn't recursive |
| **Decorator** | Add responsibilities to an object dynamically, without subclassing | Layering optional behavior (buffering, compression, auth) at runtime | Behavior is fixed — just write the class |
| **Facade** | One simple interface over a complex subsystem | Give callers a small door into a big library/module | The subsystem is already simple |
| **Flyweight** | Share fine-grained objects to save memory | Huge numbers of near-identical objects (glyphs, tiles) | Object count is modest — premature optimization |
| **Proxy** | A stand-in that controls access to another object | Lazy loading, access control, remote calls, caching | No access concern to manage |

## Gang of Four — Behavioral

*How objects distribute responsibility and communicate.*

| Pattern | Intent | When it fits | Don't use when |
|---|---|---|---|
| **Strategy** | Encapsulate interchangeable algorithms; the caller picks one | Behavior varies independently of the caller (sort order, pricing, retry policy) | One algorithm, no foreseeable second |
| **State** | An object alters its behavior when its internal state changes | An entity with modes and legal transitions (order lifecycle, connection) | The "states" don't transition — that's just Strategy |
| **Observer** | Notify N dependents when a subject changes | In-process, one-to-many change propagation | Cross-service (use events/queues) or a single listener |
| **Command** | Turn a request into an object (undo, queue, log, retry) | You need to parameterize, queue, or reverse operations | A plain method call suffices |
| **Template Method** | Fix an algorithm's skeleton, let subclasses fill steps | Invariant sequence, varying steps | Steps vary independently → prefer Strategy (composition over inheritance) |
| **Chain of Responsibility** | Pass a request along handlers until one handles it | Middleware pipelines, escalation, filters | One handler — just call it |
| **Mediator** | Centralize how a set of objects interact | Many-to-many object coupling you want to tame | Few objects, simple coupling |
| **Iterator** | Traverse a collection without exposing its internals | Custom traversal over a structure | The language's built-in iteration already does it |
| **Visitor** | Add operations over a stable type hierarchy without editing the types | Operations change often; the type set is stable | The type set churns — Visitor becomes a tax |
| **Memento** | Capture/restore an object's state without breaking encapsulation | Undo, snapshots, checkpoints | No restore requirement |
| **Interpreter** | Represent a grammar and evaluate its sentences | A small, stable DSL you evaluate | Anything a real parser/library should own |

> **Strategy vs State vs polymorphism:** Strategy = the *caller* selects behavior; State = the *object* swaps its own behavior as it transitions; if you're only branching on a type code with no transitions and no external selection, the fix is often just *replace conditional with polymorphism* (see [refactoring.md](refactoring.md)), not a named GoF pattern.

---

## Fowler PoEAA — Domain logic

*Where the business rules live. Scale up only as complexity demands.*

| Pattern | Intent | When it fits | Don't use when |
|---|---|---|---|
| **Transaction Script** | One procedure per business transaction | Simple domain, little shared logic, CRUD-ish flows | Logic is rich and duplicated across scripts |
| **Domain Model** | An OO model of interconnected objects with behavior | Rich, changing business rules (pairs with tactical [domain-driven-design.md](domain-driven-design.md)) | The domain is thin — Domain Model is overhead |
| **Table Module** | One class handles the business logic for all rows of a table | Recordset-centric platforms; moderate logic | Rich per-entity behavior/identity matters |
| **Service Layer** | A boundary API of application operations over the domain | You need a clear transactional boundary and a stable app-facing API | Trivial app with one caller |

## Fowler PoEAA — Data source & Object-Relational

*How the domain reaches storage.*

| Pattern | Intent | When it fits | Don't use when |
|---|---|---|---|
| **Row Data Gateway** | An object per row that gates DB access | Simple row access, thin logic | Rich domain behavior needed |
| **Table Data Gateway** | One object gating access to a whole table | Table-oriented access, Table Module pairing | Per-row identity/behavior matters |
| **Active Record** | Domain object carries its own persistence (object ≈ row) | Simple domain where business logic ≈ data shape | Rich domain: persistence tangles with rules → use Data Mapper |
| **Data Mapper** | A layer that moves data between objects and DB, each ignorant of the other | Rich Domain Model that must not know about storage | Simple CRUD where Active Record is honest |
| **Repository** | A collection-like interface to access domain objects, hiding the mapper/query | One per aggregate root (see [domain-driven-design.md](domain-driven-design.md)); keeps the domain persistence-ignorant | You're already using Active Record for a simple domain |
| **Unit of Work** | Track changes in a business transaction, commit as one | Multiple writes must be atomic and change-tracked | Single-write operations |
| **Identity Map** | Ensure each object is loaded once per session | Avoid duplicate instances / redundant reads in a transaction | Stateless per-request loads with no aliasing risk |
| **Lazy Load** | Defer loading data until it's needed | Expensive associations rarely traversed | You always need the data — eager is simpler and avoids N+1 |

## Fowler PoEAA — Web presentation

| Pattern | Intent | When it fits |
|---|---|---|
| **Model-View-Controller** | Separate domain (model), presentation (view), input handling (controller) | Any non-trivial UI/request layer |
| **Page Controller** | One controller per page/action | Simple sites; each page's logic is self-contained |
| **Front Controller** | One handler funnels all requests, then dispatches | Shared pre/post processing (auth, routing, logging) |
| **Template View** | Render by embedding markers in HTML | Mostly-static pages with dynamic slots |
| **Transform View** | Transform domain data into output element by element | Multiple output formats from one model |
| **Application Controller** | Centralize screen navigation and flow | Wizard/flow-heavy apps with stateful navigation |

## Fowler PoEAA — Distribution, concurrency, base

| Pattern | Intent | When it fits |
|---|---|---|
| **Remote Facade** | A coarse-grained facade over fine-grained objects for remote calls | Chatty object graphs crossing a process boundary |
| **Data Transfer Object (DTO)** | Carry data across a boundary in one trip | Serializing across network/process; decoupling wire shape from domain |
| **Optimistic Offline Lock** | Detect conflicts at commit via version check | Low-contention concurrent edits |
| **Pessimistic Offline Lock** | Prevent conflicts by locking up front | High-contention or costly-to-redo work |
| **Gateway** | An object that wraps access to an external system/resource | Isolating any external API behind your own interface |
| **Mapper** | Set up communication between two subsystems that stay ignorant of each other | Decoupling layers (Data Mapper is the DB-specific case) |
| **Registry** | A well-known object others use to find common objects/services | *Sparingly* — it's global state; prefer injection |
| **Value Object** | A small object compared by value, not identity (Money, DateRange) | Domain quantities where equality = attributes (see [domain-driven-design.md](domain-driven-design.md)) |
| **Special Case** | A subclass providing special behavior for particular cases (Null Object) | Replace scattered null checks with a polymorphic "nothing" |
| **Plugin** | Link classes chosen at configuration time, not compile time | Swappable implementations per deployment/env |
