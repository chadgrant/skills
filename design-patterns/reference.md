# Design patterns reference — GoF + Fowler PoEAA

Distilled recognition tables. For each pattern: its **intent**, **when it fits**, and **when not to** reach for it. This is vocabulary for problems you *have* — read alongside `SKILL.md`'s "don't over-apply" discipline.

---

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

> **Strategy vs State vs polymorphism:** Strategy = the *caller* selects behavior; State = the *object* swaps its own behavior as it transitions; if you're only branching on a type code with no transitions and no external selection, the fix is often just *replace conditional with polymorphism* (see `refactoring`), not a named GoF pattern.

---

## Fowler PoEAA — Domain logic

*Where the business rules live. Scale up only as complexity demands.*

| Pattern | Intent | When it fits | Don't use when |
|---|---|---|---|
| **Transaction Script** | One procedure per business transaction | Simple domain, little shared logic, CRUD-ish flows | Logic is rich and duplicated across scripts |
| **Domain Model** | An OO model of interconnected objects with behavior | Rich, changing business rules (pairs with tactical `domain-driven-design`) | The domain is thin — Domain Model is overhead |
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
| **Repository** | A collection-like interface to access domain objects, hiding the mapper/query | One per aggregate root (see `domain-driven-design`); keeps the domain persistence-ignorant | You're already using Active Record for a simple domain |
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
| **Value Object** | A small object compared by value, not identity (Money, DateRange) | Domain quantities where equality = attributes (see `domain-driven-design`) |
| **Special Case** | A subclass providing special behavior for particular cases (Null Object) | Replace scattered null checks with a polymorphic "nothing" |
| **Plugin** | Link classes chosen at configuration time, not compile time | Swappable implementations per deployment/env |

---

## How this catalog connects to the rest of the canon

- **`uncle-bob-clean-code`** — most GoF patterns are OCP/DIP made concrete; the "don't over-apply" table there and in this skill's `SKILL.md` govern all of the above. A pattern that violates SOLID is misapplied.
- **`domain-driven-design`** — Domain Model, Repository, Value Object, and Service Layer are the enterprise-pattern substrate of tactical DDD. Read that skill for how they carve a domain.
- **`refactoring`** — you rarely install a pattern up front; you *refactor toward* it under green tests when the recurring problem finally recurs (rule of three). Smell → refactoring → pattern is the usual path.
