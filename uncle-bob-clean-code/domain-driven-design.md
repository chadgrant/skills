# Domain-driven design

**Core principle: the model and the language are the same artifact.** The names in the code are the names the domain experts use — if the business says "policy" and the code says "record", the model has already failed. DDD is how you turn a tangled business into a model that protects its own rules and can be reasoned about a piece at a time. It pays off when the domain is **rich and changing**; for thin/CRUD domains it is overhead (use a Transaction Script per [patterns.md](patterns.md) and move on). Full detail in the detail below.

## Strategic design — carve the space before modeling

Do this first; tactical modeling inside the wrong boundary is wasted.

1. **Forge the ubiquitous language.** Capture the exact nouns and verbs the domain experts use. Use them verbatim in class, method, and event names. One term, one meaning — *within a context* (see below). A glossary in the PRD/ERD is where this lives (`planning`).
2. **Draw bounded contexts.** A bounded context is where a term has one precise meaning and the model is internally consistent. "Customer" in Sales ≠ "Customer" in Support — those are two models in two contexts, not one shared class forced to serve both. **A bounded context is the unit that maps cleanly to a service/module boundary** — this is where microservice seams actually come from.
3. **Map the contexts.** Name the relationship between each pair of contexts so integration is deliberate, not accidental — see the context-mapping table in the detail below (Shared Kernel, Customer/Supplier, Conformist, **Anticorruption Layer**, Open Host Service, Published Language, Separate Ways). An **Anticorruption Layer** is the default when integrating a legacy or third-party model you don't want leaking into yours.
4. **Rank subdomains.** **Core** (your competitive advantage — invest your best effort and modeling here), **Supporting** (needed but not differentiating), **Generic** (buy/adopt off the shelf — auth, billing). Don't lavish a rich Domain Model on a generic subdomain.

## Tactical design — model inside one context

| Building block | What it is | The rule that matters |
|---|---|---|
| **Entity** | An object defined by identity and continuity over time (a `User`, an `Order`) | Equality is by id, not attributes; it has a lifecycle |
| **Value Object** | An object defined by its attributes, no identity (`Money`, `DateRange`, `Address`) | **Immutable**; equality by value; prefer these — they carry no lifecycle burden |
| **Aggregate** | A cluster of entities/value objects treated as one consistency unit, with a single **root** | Outsiders reference only the root; **invariants inside the boundary are always consistent**; keep it small |
| **Repository** | A collection-like interface to load/save aggregates | **One per aggregate root**; the domain stays ignorant of storage (Data Mapper behind it) |
| **Factory** | Encapsulates complex creation of an aggregate/value object in a valid state | Use when a constructor can't guarantee a valid whole |
| **Domain Service** | A domain operation that isn't naturally a method on one entity/VO | Stateless; named in the ubiquitous language; not a dumping ground |
| **Domain Event** | Something meaningful that happened in the domain (`OrderPlaced`) | Past tense; how aggregates/contexts stay decoupled (vs an in-process Observer per [patterns.md](patterns.md)) |

**The aggregate is the load-bearing decision.** Get consistency boundaries right and the rest follows; get them wrong and you fight the model forever.

- **One transaction, one aggregate.** A single business transaction should modify one aggregate. Need to touch several? Use **domain events + eventual consistency** between them, not a giant transaction.
- **Keep aggregates small.** Large aggregates lock more, load more, and conflict more. Reference other aggregates **by id**, not by holding the object.
- **Invariants define the boundary.** The aggregate is exactly the set of objects that must be consistent together at all times. If a rule doesn't need immediate consistency, it doesn't belong inside the boundary.

## Keep the domain pure (dependency rule)

The domain model depends on **nothing** — no framework, no ORM, no HTTP, no clock. Persistence, transport, and I/O sit *outside* and depend inward (this is Clean Architecture's dependency rule, [SKILL.md](SKILL.md), and DIP). Application/Service Layer orchestrates; the domain holds the rules.

## Simplicity in the model

The four simplicity rules in [SKILL.md](SKILL.md) apply here with one twist each:

- **KISS / YAGNI**: use a tactical building block only where an invariant or the language calls for it. No aggregate, domain service, or event for a need the domain experts haven't stated.
- **DRY stops at the context boundary.** A rule has one home inside its bounded context. The same word modeled separately in two contexts is two models, not duplication; merging them "for DRY" couples the contexts.
- **Convention over configuration**: the ubiquitous language is the naming convention, and each building block sits where the codebase's layout puts that kind of object.

## Red flags: don't over-apply

| Thought | Reality |
|---|---|
| "Full DDD on this CRUD app." | A thin domain makes DDD ceremony. Transaction Script + Active Record is honest. Reserve DDD for rich, changing core domains. |
| "A rich Domain Model for auth / billing." | Generic subdomains are bought or adopted. Model only the core. |
| "One canonical enterprise-wide model for everything." | The road to a big ball of mud. Multiple bounded contexts with explicit mappings. |
| "One aggregate holds the whole order graph." | Aggregates are consistency boundaries, not object dumps. Small, invariant-scoped, referenced by id. |
| "This transaction updates five aggregates atomically." | One transaction, one aggregate. Domain events + eventual consistency across them. |
| "The entities are just data; the service has the logic." | Anemic model: a Transaction Script in a Domain Model costume. Put behavior on the aggregate that owns the invariant, or admit it's a Transaction Script. |
| "The domain object can call the ORM/HTTP directly." | The domain depends on nothing. I/O lives outside and points in. |
| "Name it what the framework calls it." | Name it what the domain experts call it. The ubiquitous language is the model. |

---

## Detail

## Strategic design

### Ubiquitous language
The shared vocabulary of domain experts and developers, used **verbatim** in code, tests, docs, and conversation. Every class, method, and event name is a term from it. When the language is fuzzy, the model is fuzzy. Capture it as a glossary in the PRD/ERD (`planning`). A term's meaning is only guaranteed *within one bounded context*.

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
- The domain talks to the repository interface; a Data Mapper / ORM lives behind it ([patterns.md](patterns.md)). The domain stays storage-ignorant.
- Repositories return fully-formed aggregates that already satisfy their invariants.

### Factory
Encapsulates the creation of a complex aggregate or value object **in a valid state** when a plain constructor can't express or guarantee it. Keep creation logic out of the aggregate's own responsibilities when it's complex.

### Domain service
A **stateless** operation expressing domain logic that doesn't naturally belong to a single entity or value object (e.g. a transfer between two accounts, a pricing calculation spanning several objects). Named in the ubiquitous language. Not a bucket for logic you were too lazy to put on the model — reach for it only when the operation genuinely spans aggregates or belongs to none.

### Application service vs domain service
- **Application service** (a.k.a. Service Layer, [patterns.md](patterns.md)) — orchestrates a use case: load aggregate(s) via repositories, invoke domain behavior, commit, dispatch events. Holds **no domain rules**; it's a thin coordinator and the transaction boundary.
- **Domain service** — holds domain rules that span entities. Lives *inside* the domain.

### Domain event
A record that **something meaningful happened** (`OrderPlaced`, `PaymentCaptured`). Named in the **past tense**. Uses:
- Decouple aggregates: aggregate A commits, publishes an event; aggregate B reacts in its own transaction (eventual consistency).
- Decouple bounded contexts: events cross context boundaries as integration messages.
- In-process one-to-many notification is an Observer ([patterns.md](patterns.md)); a domain event is the domain-meaningful, often persisted/published, version of that idea.

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

Dependencies point **inward** only. The domain model at the center depends on nothing external; infrastructure implements interfaces the domain/application declares (DIP, Clean Architecture — see [SKILL.md](SKILL.md)). This is what makes the domain testable without a database and stable against framework churn.
