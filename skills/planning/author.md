# Author requirements and a routed plan

Read this for new work needing a document set.

### A0. Clarify

Time the planning in the delivery journal (`python3 <this skill's directory>/../implementation/scripts/journal.py`; see [journal.md](../implementation/journal.md) for event names): `begin run <YYYY-MM-DD-slug>` and write that id into the plan header, then `begin`/`end phase` around `clarify`, `docs`, and `plan`. The build continues the same run.

Ask only questions whose answers change the docs: the problem and for whom, success metrics, scope in/out, fail modes, tenancy, data sensitivity, environment ceilings, decisions that fork the architecture.

Work the open decisions as a tree, in **rounds**. A round is every question you can ask now without guessing at an answer you haven't heard. Number each question, give your recommended answer, and word it so "yes" accepts the recommendation; then wait. Each answer unblocks the next round. Find facts in the repo; delegate substantial discovery under [delegation.md](../implementation/delegation.md). Ask only unresolved material decisions and reuse answers already supplied.

### A1. Pick the doc set

Produce only what the request warrants. Confirm material scope choices still unresolved; briefly explain non-obvious omissions. A skipped DRD on a feature that stores user data is a red flag, not a shortcut.

| Doc | Produce when | Skip when |
|---|---|---|
| **PRD** (`templates/prd.md`) | **Always.** Every change has a why. | Never; scale it down to a few paragraphs for small work. |
| **ERD** (`templates/erd.md`) | A new external dependency, a new service/module boundary, a cross-cutting concern (security/observability/cost), or a rejected alternative worth recording | An obvious single-pattern change with no trade-off |
| **DRD** (`templates/drd.md`) | Work adds or changes persistent data: schemas, entities, relationships, PII/retention | No data-model change |
| **API contract** (`templates/api-contract.md`) | Work exposes or changes a service boundary or a public/consumed API | No API surface change |
| **User flows** (`templates/user-flows.md`) | A user-facing surface: screens, navigation, forms | Headless, CLI, or backend job |
| **Wireframes** (`templates/wireframes.md`) | Screens to lay out (usually whenever flows exist) | No UI, or a copy/style-only tweak |
| **Style guide** (`design-system/style-guide.md`) | Net-new visual language, or no design system exists yet | The org's design system covers it: reference it, list only net-new `CMP-` |
| **Release plan** (`templates/release-plan.md`) | Prod-facing deploy, migration, cutover, or rollback | Internal library / no-deploy change |
| **Observability** (`templates/observability.md`) | Runs as a live service with health to watch | Pure library, build-time, or one-shot |
| **User docs** (`templates/user-docs.md`) | End-user-visible behavior changes | Internal-only refactor |
| **Test & QA plan** (`templates/test-qa-plan.md`) | Non-trivial behavior or integration to verify beyond unit tests; anything with e2e tests | Trivial change covered by per-task `TEST-` |
| **Implementation plan** (`templates/implementation-plan.md`) | More than one obvious task | A single self-evident task |

Add by hand when warranted: a threat model for security / money / auth work; an RFC before the ERD on a contentious decision.

### A2. Write the docs

- Read only the selected templates and their matching sections in [reference.md](reference.md).
- Requirements go in `docs/requirements/`, the plan in `docs/plans/`; project conventions override. The style guide lives in `design-system/`, cross-project and long-lived, referenced not regenerated per feature.
- Every requirement, entity, decision, and task gets a spine ID as you write it. Use [document-rules.md](document-rules.md) for IDs, diagrams, and validation.
- **`docs/requirements/GLOSSARY.md`** is written first and kept current: each domain term, a one-line definition, and the synonyms to avoid. The docs, the plan, the code, and the tests use these words and no others. It is one short file because every worker and reviewer reads it; the PRD and ERD cite it and don't repeat it.

### A3. Build the routed plan

- **Contracts first.** For each milestone, list its `CON-###` contracts before its tasks: every interface, abstract class, protocol, and shared type that its tasks call across each other, each with its final file path, its members, and the behavior, errors, and invariants its doc comment will state, in the glossary's words. The ERD's design and the API contract feed these; the contracts are their code-level form. The first task of every milestone writes them as code, with stubs and contract tests.
- Decompose the rest into `TASK-###`s that **implement contracts**: each a cohesive group of `CON`s (a module, or one bounded context's part of the feature) built by one worker, sized so its context stays small: up to about 400 changed lines and one screen, endpoint group, or module. Exactly one task implements each `CON`; tasks depend on contracts, not on each other, so a milestone is usually one parallel wave. Never split by layer; the task count follows from the size. When a milestone has fewer than three independent tasks or is one tightly coupled piece, make it one task: a single agent wins on small work. Each task names the `REQ`s it satisfies, the `CON`s it implements and consumes, the hot files it touches, and a `TEST-###` verify step needing no human interpretation. Group the tasks into milestones, each a big feature that ends in one review.
- Rate each task on its hardest aspect and assign a tier per [routing.md](../implementation/routing.md); record tiers, not model names. Which model the top tier maps to is the user's call: `chadgrant:implementation` asks before using Fable and defaults to Opus. Flag `observe` only per its definition there (the true security/money spine). It should mark a small minority of tasks; a third or more flagged means re-rate.
- Add these **global constraints** once, under one heading in the plan; `chadgrant:implementation` points every brief at that heading, so they are written in one place and read from there:
  - **UI**: built with [Impeccable](https://github.com/pbakaus/impeccable) against the style guide's tokens and components.
  - **Services** (API, worker, consumer, scheduled job): follow the [Twelve-Factor App](https://12factor.net); `chadgrant:implementation`'s [services.md](../implementation/services.md) carries the checklist. Each service task names its config keys and env var names, backing services, port and health endpoints, and shutdown behavior; migrations and admin jobs are their own tasks. A deviation is an `ADR` the task cites.
  - **Current versions**: the stack's runtime, framework, and key libraries are the latest stable releases, looked up in their registries when the plan is written, not recalled. Write the versions into the plan. A deliberately older version is an `ADR` with the reason. Every dependency added during the build is also its latest stable release (the worker manual says how).
  - **Quality bar**: done means the `TEST-` is green **and** the code is clean per `chadgrant:clean-code`. Name the project's static gate command (format check, lint, type-check, complexity limit); every `TEST-` runs it alongside the task's tests. A `TEST-` that a bloated or over-engineered solution can still pass is not a complete acceptance criterion.
  - **Testing**: the plan names each command and tool; workers don't choose them. Two gates:
    - *Fast gate*: unit and other self-contained tests plus the static gate. No Docker or network services, so workers run it in parallel in their own worktrees.
    - *Full gate*: integration tests against the real backing services (a `compose.test.yaml` with health checks when the project uses Docker Compose; never a mock or in-memory substitute), at least 90% line coverage enforced by the coverage tool's fail-under threshold (exclusions listed in the plan), and end-to-end tests through the public surface. Pick the e2e driver by surface: browser UI → Playwright; HTTP API → requests against the running service; CLI → the built binary; library → none beyond tests of its public API. Only the orchestrator runs it, once per milestone.
    - The harness for both gates is an M0 task; each e2e scenario is a `TC-` built by the feature that needs it.
  - **Design**: per `chadgrant:clean-code`: known patterns (its `patterns.md`) over invention; rich domains via its `domain-driven-design.md`, whose glossary and bounded contexts go in the PRD/ERD and inform module boundaries; a refactoring (its `refactoring.md`) is a plannable task type with a behavior-unchanged verify.
  - **Simplicity**: the four rules in `chadgrant:clean-code` bind the docs and the plan as well as the code. YAGNI: no requirement, entity, endpoint, or task without a stated need behind it; "future-proofing" is out of scope until someone asks for it. KISS: the ERD picks the simplest architecture that meets the PRD and records what it declined to add. DRY: each fact lives in one doc and the others cite its spine ID. Convention over configuration: the chosen stack's standard layout, naming, and tooling are the default; a deviation is an `ADR`.
- Set `max_parallel` explicitly (default 4, bounded by available capacity).
- Hand the plan to `chadgrant:implementation`. A single self-evident task needs neither a plan nor a handoff.

### A4. Traceability check

Run the applicable [traceability checks](document-rules.md#traceability-checklist), fix gaps, then hand off.
