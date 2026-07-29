---
name: domain-driven-design
description: Use when modeling a non-trivial business domain — deciding what the objects are, where the consistency boundaries lie, how services are carved, and what language the code and the stakeholders share. Applies Eric Evans' Domain-Driven Design: strategic design (ubiquitous language, bounded contexts, context mapping, core vs supporting vs generic subdomains) and tactical design (entities, value objects, aggregates and their invariants, repositories, factories, domain services, domain events). Use it when a Domain Model (see design-patterns) is the right choice and you need to shape it well. Triggers: "domain model", "DDD", "bounded context", "aggregate", "entity vs value object", "ubiquitous language", "where's the consistency boundary", "how do I carve these services", "repository per aggregate".
---

# Domain-driven design

Announce at the start: **"Using domain-driven-design: speak the domain's language → draw the bounded contexts → model aggregates around invariants → keep the domain pure."**

**Core principle: the model and the language are the same artifact.** The names in the code are the names the domain experts use — if the business says "policy" and the code says "record", the model has already failed. DDD is how you turn a tangled business into a model that protects its own rules and can be reasoned about a piece at a time. It pays off when the domain is **rich and changing**; for thin/CRUD domains it is overhead (use a Transaction Script per `design-patterns` and move on).

This composes with the canon: a DDD **Domain Model** is built from Fowler enterprise patterns (`design-patterns`: Repository, Value Object, Service Layer, Data Mapper), its objects obey **SOLID** and clean-code rules (`uncle-bob-clean-code`), and you **`refactoring`** your way toward richer aggregates as understanding deepens. Full detail in [reference.md](reference.md).

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

## Don't over-apply

| Temptation | Reality |
|---|---|
| Full DDD on a CRUD app | If the domain is thin, DDD is ceremony. Transaction Script + Active Record is honest. Reserve DDD for rich, changing core domains. |
| One giant "God" aggregate | Aggregates are consistency boundaries, not object dumps. Small, invariant-scoped, referenced by id. |
| One canonical enterprise-wide model for everything | That's the road to a big ball of mud. Multiple bounded contexts with explicit mappings beat one model serving every master. |
| Anemic domain model (data bags + service does everything) | If entities have no behavior and services hold all logic, you have a Transaction Script wearing a Domain Model costume. Put behavior on the model — or admit it's a Transaction Script. |
| Rich Domain Model on a *generic* subdomain | Buy/adopt generic subdomains (auth, billing). Model only the core. |

## Red flags — stop if you catch yourself thinking…

| Rationalization | Reality |
|---|---|
| "This transaction updates five aggregates atomically." | One transaction, one aggregate. Use domain events + eventual consistency across them. |
| "The entities are just data; the service has the logic." | Anemic model. Behavior belongs on the aggregate that owns the invariant. |
| "The domain object can call the ORM/HTTP directly, it's simpler." | The domain depends on nothing. Invert it — I/O lives outside and points in. |
| "Let me name it what the framework calls it." | Name it what the domain experts call it. The ubiquitous language is the model. |

---

*A recognition-and-decision layer distilled from **Eric Evans**' *Domain-Driven Design* (and Vernon's *Implementing DDD*). It builds on `design-patterns` (Domain Model, Repository, Value Object, Service Layer are its substrate), obeys `uncle-bob-clean-code` (SOLID + the dependency rule keep the domain pure), and is shaped over time via `refactoring`. Its ubiquitous language and context map belong in the PRD/ERD produced by `requirements-driven-planning`. Full detail in [reference.md](reference.md).*
