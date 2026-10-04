---
name: domain-driven-design
description: Use when modeling a non-trivial business domain: what the objects are, where the consistency boundaries lie, how services are carved, and what language the code and stakeholders share. Triggers: "domain model", "DDD", "bounded context", "aggregate", "entity vs value object", "ubiquitous language", "repository per aggregate".
---

# Domain-driven design

Announce at the start: **"Using domain-driven-design: speak the domain's language → draw the bounded contexts → model aggregates around invariants → keep the domain pure."**

**Core principle: the model and the language are the same artifact.** The names in the code are the names the domain experts use — if the business says "policy" and the code says "record", the model has already failed. DDD is how you turn a tangled business into a model that protects its own rules and can be reasoned about a piece at a time. It pays off when the domain is **rich and changing**; for thin/CRUD domains it is overhead (use a Transaction Script per `design-patterns` and move on). Full detail in [reference.md](reference.md).

## Strategic design — carve the space before modeling

Do this first; tactical modeling inside the wrong boundary is wasted.

1. **Forge the ubiquitous language.** Capture the exact nouns and verbs the domain experts use. Use them verbatim in class, method, and event names. One term, one meaning — *within a context* (see below). A glossary in the PRD/ERD is where this lives (`requirements-driven-planning`).
2. **Draw bounded contexts.** A bounded context is where a term has one precise meaning and the model is internally consistent. "Customer" in Sales ≠ "Customer" in Support — those are two models in two contexts, not one shared class forced to serve both. **A bounded context is the unit that maps cleanly to a service/module boundary** — this is where microservice seams actually come from.
3. **Map the contexts.** Name the relationship between each pair of contexts so integration is deliberate, not accidental — see the context-mapping table in [reference.md](reference.md) (Shared Kernel, Customer/Supplier, Conformist, **Anticorruption Layer**, Open Host Service, Published Language, Separate Ways). An **Anticorruption Layer** is the default when integrating a legacy or third-party model you don't want leaking into yours.
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
| **Domain Event** | Something meaningful that happened in the domain (`OrderPlaced`) | Past tense; how aggregates/contexts stay decoupled (vs an in-process Observer per `design-patterns`) |

**The aggregate is the load-bearing decision.** Get consistency boundaries right and the rest follows; get them wrong and you fight the model forever.

- **One transaction, one aggregate.** A single business transaction should modify one aggregate. Need to touch several? Use **domain events + eventual consistency** between them, not a giant transaction.
- **Keep aggregates small.** Large aggregates lock more, load more, and conflict more. Reference other aggregates **by id**, not by holding the object.
- **Invariants define the boundary.** The aggregate is exactly the set of objects that must be consistent together at all times. If a rule doesn't need immediate consistency, it doesn't belong inside the boundary.

## Keep the domain pure (dependency rule)

The domain model depends on **nothing** — no framework, no ORM, no HTTP, no clock. Persistence, transport, and I/O sit *outside* and depend inward (this is Clean Architecture's dependency rule, `uncle-bob-clean-code`, and DIP). Application/Service Layer orchestrates; the domain holds the rules.

## Simplicity in the model

The four simplicity rules in `uncle-bob-clean-code` apply here with one twist each:

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

*Distilled from **Eric Evans**' *Domain-Driven Design* and Vernon's *Implementing DDD*. Related: `design-patterns` (Domain Model, Repository, Value Object, Service Layer are its substrate), `uncle-bob-clean-code` (the dependency rule keeps the domain pure), `refactoring` (how aggregates get richer over time), `requirements-driven-planning` (the glossary and context map live in the PRD/ERD). Full detail in [reference.md](reference.md).*
