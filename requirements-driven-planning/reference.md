# Reference — section intent & anti-patterns

Per-section guidance for each document. Use this to fill the templates well, not just fully. Each doc ends with the **anti-patterns** that most often make that doc type useless — check your draft against them.

---

## PRD — product requirements ("what & why")

Reads like an evidenced narrative, not a feature list. It states the *problem* and lets the solution stay directional; the ERD owns the "how".

| Section | Intent |
|---|---|
| Summary | One paragraph: context and scope. A reader should grasp the whole in 30 seconds. |
| Problem statement | The customer pain, **quantified** with data. No problem, no PRD. |
| Goals & success metrics | Measurable outcomes / target KPIs. These become the plan's `TEST-` acceptance criteria. |
| Users / personas | Who this is for; validation, competitive context. |
| Proposed solution | Directional — mockups/wireframes/flows. The *what*, not the *how*. |
| Functional requirements `REQ-###` | Numbered, **testable**, one requirement each. The spine starts here. |
| Non-functional `NFR-###` | Performance, accessibility, security, legal/compliance budgets. |
| Edge cases & states | Empty / error / permission / offline boundaries. |
| Dependencies & risks | Blockers, downside risks, mitigations. |
| Release criteria | The gates that decide "ship / no-ship". |

**Anti-patterns:** prescribing the solution instead of stating the problem (over-specifying "how"); vacuous bullets that hide weak thinking; no data or metrics; skipping edge cases and downside risks; blank wireframes punted to design instead of doing the upfront thinking.

*Front-end variant:* Amazon working-backwards **PR/FAQ** — a customer-facing press release + FAQ written *before* code, as a forcing function for customer focus. Good when the value proposition itself is the risk.

---

## ERD — engineering requirements ("how we build it")

Architecture, infrastructure, code patterns, interfaces, and the trade-offs behind them. Link to code and schemas — don't paste them (pasted signatures rot).

| Section | Intent |
|---|---|
| Context & scope | The landscape and what's being built into it. |
| Goals & non-goals | Explicitly bound the problem. Non-goals prevent scope creep. |
| The design | Components, APIs, data flow, a system-context diagram, the patterns to follow, key trade-offs. |
| Alternatives considered | Options evaluated and **why rejected**. This is the section that carries the reasoning. |
| Cross-cutting concerns | Security, privacy, observability, cost, failure modes (fail-open vs fail-closed per component). |
| Decisions `ADR-###` | One decision each: *Title · Status · Context · Decision · Consequences* + alternatives. Never edit an accepted ADR — **supersede and link**. |

**Anti-patterns:** no *alternatives-considered* section (obscures the reasoning); an implementation manual with no rationale or trade-offs; excessive length (>~20 pages → decompose); pasting full signatures/schemas that will rot; writing a design doc when there are genuinely no trade-offs to weigh.

---

## DRD — data requirements ("the data model")

The data model, physical schema, and governance. The ER diagram and the data dictionary must describe the **same** thing.

| Section | Intent |
|---|---|
| Scope & owners | Domains/systems in scope; who owns the data. |
| Conceptual ER model `ENT-###` | Entities, relationships, **cardinality**. |
| Physical schema | Tables, keys, indexes, constraints. |
| Data dictionary | **Per field:** name, type, allowable values, description, nullability. |
| Classification & PII | Sensitivity per field (public / internal / confidential / restricted). |
| Lifecycle & lineage | Collection points, data flow, storage locations (incl. backups). |
| Retention & deletion | Retention periods, purge/anonymization rules, legal basis. |
| Access & security | Who can read/write; encryption, masking. |
| Migration / versioning | Schema-change and backfill strategy. |

**Anti-patterns:** ER diagram and data dictionary drifting out of sync; no per-field PII classification; retention/deletion left unspecified; a schema with no data dictionary (no field-level types or allowable values).

---

## API contract — the interface ("what callers can rely on")

Explains and pins the interface. The machine-readable spec (OpenAPI/AsyncAPI/proto) is authoritative; this doc makes it human-readable and traces it to requirements.

| Section | Intent |
|---|---|
| Overview & style | REST/GraphQL/gRPC/async, base URL, media types, versioning scheme. |
| Auth | Scheme, scopes/roles (ref `NFR-`). |
| Operations `API-###` | Per operation: method/path, request, response, errors — each citing the `REQ` it serves and the `ENT` it touches. |
| Schemas | Request/response models, linked back to DRD `ENT-`/data-dictionary (don't re-define types). |
| Error model | Uniform envelope, status-code conventions, retryable vs. terminal. |
| Compatibility & versioning | Breaking-change policy, deprecation window, consumer notification. |
| Rate limits & SLAs | For public/consumed APIs. |

**Anti-patterns:** prose-only "API" with no concrete request/response; no error model; no versioning/deprecation policy; endpoint list that drifts from the ERD/DRD; re-defining field types the DRD already owns.

## Test & QA plan — the proof ("how we know it works")

Sits above the per-task `TEST-` unit checks: scenario-level cases, non-functional testing, and the release gate.

| Section | Intent |
|---|---|
| Scope & objectives | What this proves; in/out of scope. |
| Test strategy | Levels (unit/integration/e2e/manual), tooling, environments, CI stage. |
| Test matrix `TC-###` | Each case verifies a `REQ`/`NFR` with an explicit pass condition. |
| Non-functional testing | Perf/load/security/a11y per `NFR-`, with targets. |
| Test data & fixtures | Synthetic/PII-safe data (ref DRD classification — never real PII in test envs). |
| Entry & exit criteria | When testing starts; the pass bar that gates release. |
| Risks & gaps | Known untested areas and accepted residual risk. |

**Anti-patterns:** restating requirements without saying *how* they're verified; no exit/release criteria; no non-functional coverage; real PII in test data; cases with no pass condition.

## Implementation plan — the execution DAG

The most rigid doc: an agent must execute each task with **no interpretation**. This is the input `multi-model-implementation` consumes.

| Section | Intent |
|---|---|
| Front matter & status | Goal, version, owner, status. |
| Introduction | The outcome in one paragraph. |
| Requirements & constraints | The `REQ-`/`NFR-` this plan satisfies + global constraints (version floors, naming/copy rules) copied verbatim. |
| Phases & tasks `TASK-###` | Phases (`GOAL-`) of atomic tasks. Tasks within a phase are parallelizable; cross-phase order is **declared**, forming the DAG. |
| Per task | Exact file paths, the interface it produces, `TEST-###` (automatic pass criteria), the `REQ` it cites, difficulty, and **model tier**. |
| Alternatives / dependencies / risks | Rejected approaches, external deps + ordering, risks & assumptions. |

**Anti-patterns:** ambiguous tasks requiring interpretation; tasks without file-path specificity; missing per-task verification; undeclared (hidden) ordering dependencies; placeholder text; a task that overlaps another wave's files (breaks parallel disjointness).

**Difficulty → model tier** (from `multi-model-implementation`): rate each task on its *hardest* aspect. Easy (mechanical, single-file, well-specified) → small tier. Medium (multi-file, some design judgement) → mid tier. Hard (security/money/auth/data-integrity, concurrency, novel algorithm, high blast radius, many tasks depend on it) → top tier; additionally flag **`observe`** (mandatory adversarial review) when the task sits on the security/money/auth/data-integrity spine. Security-small is still Hard. The concrete tier→model mapping lives in `multi-model-implementation`, not here — record tiers, not model names.

---

## Which diagram belongs where

Every diagram obeys the rules in SKILL.md → Diagrams (≤6 boxes, C4 split, ELI5 caption, ID-labeled boxes, Excalidraw source).

| Doc | Diagram(s) | Split rule when it grows |
|---|---|---|
| **PRD** | **User flow / journey** (happy path, ≤6 steps); optional **system-context** (who uses it, what it touches) | One flow per diagram — a branch becomes its own flow |
| **ERD** | **C4 Context → Container → Component** (each its own ≤6-box diagram); optional **sequence** for one key interaction | Drill down a C4 level rather than adding boxes |
| **DRD** | **ER diagram** (entities + relationships, ≤6 entities per view); optional **data-flow** (collect → store → delete) for the privacy/lifecycle story | Split the ER view by subdomain (e.g. billing vs. identity) |
| **API contract** | **Sequence diagram** for one key operation (client → service → store, ≤6 boxes) | One operation per diagram |

The ELI5 caption matters most on the DRD data-flow and the ERD Context diagram — those are what a non-engineer (or a five-year-old) should still follow.

## Cross-linking (the sync guarantee)

The shared ID namespace is what lets you *mechanically* prove nothing is orphaned:

- **`REQ-` is the origin.** PRD requirements are cited by ERD design sections, by DRD entities, and by each plan `TASK`.
- PRD **success metrics** ↔ plan **`TEST-`** / acceptance criteria.
- ERD **entities/APIs** ↔ DRD **tables/fields** ↔ plan **file paths**.
- PRD **`NFR-` + PII** ↔ ERD **cross-cutting concerns** ↔ DRD **classification/retention**.
- **`ADR-`** cited by ID from both the ERD and the tasks that implement the decision.

If every ID resolves both directions, the docs are in sync. Any dangling ID is drift — fix it in Path B re-sync.
