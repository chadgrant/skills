# Domain-driven design reference

Distilled from Evans' *Domain-Driven Design* and Vernon's *Implementing DDD*. Read alongside `SKILL.md`'s discipline and "don't over-apply" table.

---

## Strategic design

### Ubiquitous language
The shared vocabulary of domain experts and developers, used **verbatim** in code, tests, docs, and conversation. Every class, method, and event name is a term from it. When the language is fuzzy, the model is fuzzy. Capture it as a glossary in the PRD/ERD (`requirements-driven-planning`). A term's meaning is only guaranteed *within one bounded context*.

### Bounded context
A boundary within which a model is internally consistent and each term has one precise meaning. It is the honest unit of modularity — **the seam a service or module boundary should follow**. Trying to build one canonical model for the whole enterprise produces a "big ball of mud"; multiple bounded contexts with explicit mappings is the alternative.

### Context mapping — naming the relationship between two contexts

| Relationship | What it means | Reach for it when |
|---|---|---|
| **Shared Kernel** | Two teams share a small common model, changed only by agreement | Tight collaboration, a genuinely shared core sub-model |
| **Customer/Supplier** | Downstream (customer) needs drive upstream (supplier) priorities | Clear upstream/downstream with a cooperative upstream |
| **Conformist** | Downstream simply adopts the upstream model as-is | Upstream won't accommodate you and its model is acceptable |
| **Anticorruption Layer (ACL)** | A translation layer that keeps a foreign model from leaking in | Integrating legacy/third-party models you must not let corrupt yours — **the safe default** |
| **Open Host Service** | Upstream publishes a well-defined protocol for many consumers | Many downstreams integrate with one context |
| **Published Language** | A shared, well-documented interchange format (often with OHS) | Cross-context/cross-org integration needs a stable contract |
| **Separate Ways** | No integration; the contexts don't connect | Integration cost exceeds the value |

### Subdomain classification
- **Core domain** — the reason the software exists; your competitive edge. Put your best modeling effort here.
- **Supporting subdomain** — necessary, specific to you, but not differentiating. Model adequately.
- **Generic subdomain** — solved problems (auth, billing, notifications). Buy or adopt; don't hand-model.

---

## Tactical design

### Entity
Defined by **identity and continuity**, not attributes. Two entities with identical fields but different ids are different; the same id across time (with changing fields) is the same entity. Give it behavior that enforces its own rules — don't reduce it to a data bag.

### Value object
Defined **entirely by its attributes**, with **no identity**. `Money`, `DateRange`, `Color`, `Address`. Rules:
- **Immutable** — operations return new instances.
- **Equality by value** — two `Money(5, USD)` are equal.
- **Side-effect-free** — a `Money.plus(...)` returns a new `Money`.
- **Prefer them.** They carry no lifecycle or persistence-identity burden and make the model safer. Reach for a value object before an entity whenever identity doesn't matter.

### Aggregate & aggregate root
A cluster of entities and value objects that must stay **consistent as a unit**, with one **root entity** as the only external entry point.
- Outsiders hold references to the **root only**; internals are reached through it.
- **Invariants inside the boundary hold at all times** (end of every transaction).
- **Reference other aggregates by identity** (store their id), never by holding the object graph.
- **One transaction modifies one aggregate.** Cross-aggregate consistency is achieved with **domain events + eventual consistency**.
- **Keep it small** — large aggregates cause lock contention, over-fetching, and merge conflicts. When in doubt, smaller.

### Repository
A collection-like abstraction for retrieving and persisting **aggregates** (whole, via their root).
- **One repository per aggregate root.**
- The domain talks to the repository interface; a Data Mapper / ORM lives behind it (`design-patterns`). The domain stays storage-ignorant.
- Repositories return fully-formed aggregates that already satisfy their invariants.

### Factory
Encapsulates the creation of a complex aggregate or value object **in a valid state** when a plain constructor can't express or guarantee it. Keep creation logic out of the aggregate's own responsibilities when it's complex.

### Domain service
A **stateless** operation expressing domain logic that doesn't naturally belong to a single entity or value object (e.g. a transfer between two accounts, a pricing calculation spanning several objects). Named in the ubiquitous language. Not a bucket for logic you were too lazy to put on the model — reach for it only when the operation genuinely spans aggregates or belongs to none.

### Application service vs domain service
- **Application service** (a.k.a. Service Layer, `design-patterns`) — orchestrates a use case: load aggregate(s) via repositories, invoke domain behavior, commit, dispatch events. Holds **no domain rules**; it's a thin coordinator and the transaction boundary.
- **Domain service** — holds domain rules that span entities. Lives *inside* the domain.

### Domain event
A record that **something meaningful happened** (`OrderPlaced`, `PaymentCaptured`). Named in the **past tense**. Uses:
- Decouple aggregates: aggregate A commits, publishes an event; aggregate B reacts in its own transaction (eventual consistency).
- Decouple bounded contexts: events cross context boundaries as integration messages.
- In-process one-to-many notification is an Observer (`design-patterns`); a domain event is the domain-meaningful, often persisted/published, version of that idea.

### Module
Named packages that follow the ubiquitous language and group a cohesive slice of the model (low coupling between modules, high cohesion within). The package structure should read like the domain, not like technical layers.

---

## The layered / hexagonal arrangement (dependency rule)

```
  (outside)  UI / API / Messaging  ─┐
             Infrastructure (DB, ORM, HTTP clients, clock)  ─┐
             Application Services (use-case orchestration, tx boundary)  ─┐
  (inside)   Domain Model (entities, VOs, aggregates, domain services, events)
```

Dependencies point **inward** only. The domain model at the center depends on nothing external; infrastructure implements interfaces the domain/application declares (DIP, Clean Architecture — see `uncle-bob-clean-code`). This is what makes the domain testable without a database and stable against framework churn.

---

## How this connects to the rest of the canon

- **`design-patterns`** — Domain Model, Repository, Value Object, Service Layer, Data Mapper are Fowler enterprise patterns; DDD is their application to a rich domain.
- **`uncle-bob-clean-code`** — the dependency rule, SOLID, and clean-code discipline keep aggregates cohesive and the domain pure.
- **`refactoring`** — you discover aggregate boundaries and richer models over time; move toward them in small steps under green tests (rule of three, break-up-large-aggregate).
- **`requirements-driven-planning`** — the ubiquitous-language glossary and context map belong in the PRD/ERD; bounded contexts inform the service/module boundaries in the architecture doc.
