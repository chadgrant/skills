---
name: clean-implementation
description: Use when you are the worker building one task from a plan or a dispatched brief. Triggers: "implement TASK-###", "build this task", "you are the worker", "the test is failing", "address the review". Not for planning or orchestrating waves.
---

# Clean implementation

Announce: **"Using clean-implementation: read the brief → verify-first → write it clean → prove it green and clean → report."**

**Core principle: one task, done well and proven.** You are a worker. Someone above you decomposed the work, routed this task to you, and will verify, commit, and integrate it. Build exactly what the brief says, make its verify step pass, and report truthfully. Doing more, touching more, or claiming more is a defect.

Pipeline position: `requirements-driven-planning` → `model-routed-delivery` → **this skill**. The layer above owns routing, waves, commits, and the ledger.

## The brief

Confirm you have all of these before typing:

- **Task id and goal**
- **Files**: your lane, disjoint from every other worker's by design
- **Interface to produce**: a promise later tasks build on; match it exactly
- **Verify step**: the exact command that proves the task done
- **Difficulty / `observe`**: `observe` means a dedicated adversarial review; other Hard tasks are reviewed with their wave. Either way, write code that survives a reviewer trying to break it.
- **Global constraints**: stack, fail-mode, Impeccable for UI, Twelve-Factor for services, copied verbatim from the plan

A brief may bundle several Easy tasks in one lane. Build and verify each in turn and report per task.

Missing or ambiguous? Two cases:
- A gap that doesn't change the interface or observable behavior: take the smallest defensible interpretation, mark it `⚠` in your report, and continue.
- A gap that does (an unspecified interface, or two readings that produce different behavior): ask the orchestrator before building. Never invent an interface the plan didn't specify.

## Build loop

1. **Read the contract.** Your lane's files and the interfaces of the tasks you depend on. Not the whole tree.
2. **Verify-first.** Write the failing test from the verify step before the implementation; make it fail for the right reason, then pass. When the verify step is only a build, lint, or type-check (scaffolding, config, wiring), there is no test to write first: build it and run the verify step.
   - **Coverage**: your tests cover at least 90% of the lines in your lane's files, through assertions on behavior. A test that executes code without asserting on it is a defect, and so is excluding a file from coverage; exclusions belong to the plan.
   - **Real backing services**: code that talks to a database, queue, or cache is tested against the real one from the plan's Compose file. Don't mock it or swap in an in-memory substitute.
   - **End-to-end**, when your task is an e2e scenario: drive the public surface with the plan's driver (Playwright for browser UI, HTTP for an API, the built binary for a CLI) against the Compose stack. Never Playwright for something without a browser UI.
3. **Write it per `uncle-bob-clean-code`**, including its four simplicity rules: KISS (the simplest thing that passes the verify step), YAGNI (nothing the brief doesn't ask for), DRY (one home for each rule and constant), convention over configuration (the framework's and repo's standard layout, naming, and defaults before anything custom). For a design decision (how objects collaborate, how the domain is modeled) also use `design-patterns` and, for a rich domain, `domain-driven-design`. If the code you must change fights you, refactor first under green tests via `refactoring`, then add the feature; never both in one diff.
4. **UI → Impeccable.** Build user-facing surfaces with the [Impeccable](https://github.com/pbakaus/impeccable) skill against the style guide's `TOK-`/`CMP-` (`design-system/style-guide.md`). Wireframes give layout; the style guide gives visual language.
5. **Service → Twelve-Factor.** A deployable service (API, worker, consumer, scheduled job) follows the [Twelve-Factor App](https://12factor.net):
   - **II** dependencies declared in the manifest and lockfile; nothing relies on a host-installed tool
   - **III** config (URLs, credentials, flags, limits) read from the environment at startup, validated, fail fast if missing; no config in code, no per-environment files, no secrets in the repo. Convention over configuration keeps the list short: a setting exists only when deployments truly differ on it.
   - **IV** databases, queues, caches, third-party APIs are attached resources located by config
   - **VI** stateless and share-nothing; session, cache and upload state lives in a backing service
   - **VII** binds a port taken from config
   - **IX** fast startup; on `SIGTERM` stop accepting work, drain, close connections; jobs are safe to retry after a crash
   - **X** the same kinds of backing services in dev and test as in prod (a real Postgres in a container, not SQLite)
   - **XI** an unbuffered log stream to stdout; no log files or rotation in the app
   - **XII** migrations and one-off tasks are separate commands against the same code and config
   - **I** one codebase, **V** build / release / run kept separate, **VIII** scaling by process type: these belong to the repo and deploy pipeline; don't break them (for example, no config baked into a build artifact)

   A waived factor is an `ADR` in your brief; anything else you can't meet is a `⚠` in your report.
6. **Prove it green.** Run the exact verify step yourself. Red → the debug loop below.
7. **Prove it clean.** The static gate in your verify step covers format, lint, types, and complexity; spend this step on what tools can't see. Run `uncle-bob-clean-code`'s three review passes (correctness and security, design, readability) over your own diff, checking in particular for one thing per function, the four simplicity rules (KISS, YAGNI, DRY, convention over configuration), and patterns where the problem demands one and nowhere else. Code that passes its test but reads like a mess is not done. Fix, then re-verify.
8. **Report** (format below).

## Debug loop (a test went red)

1. **Reproduce on demand.** Can't reproduce → report it as flaky; never paper over it.
2. **Read the actual error** before guessing.
3. **One hypothesis at a time**, stated with its reason.
4. **Root cause, not symptom.** A swallowed exception, a `+1`, a masking retry are symptom patches; review will find what you buried.
5. **Minimal fix, then re-verify for the right reason**, not because you weakened the test.
6. **Ceiling.** Three or four hypotheses tested and still red, or the fix needs a file outside your lane: stop and report what you tried and ruled out. Escalation is not failure; a silent wrong fix is.

## Receiving review

1. **Reproduce each finding before touching code.** Reproducible → real; fix it. Not reproducible → report it as refuted, with the exact case you ran and its result.
2. **Fix real ones at the root** via the debug loop.
3. **Push back with evidence** (the failing case, the violated requirement), not deference.
4. **Never performatively agree.** Blind implementation is as much an abdication as ignoring the review.
5. **Report per finding**: fixed (with re-verify evidence) or refuted (with the proving case).

## Iron rules

- **Stay in your lane.** Need a file that isn't yours? Report it; don't touch it.
- **Shared files belong to the orchestrator.** Never create or edit `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, the plan, the root `README`, or any other file outside your lane, including to record a learning, a convention, or progress. Several workers run at once and overwrite each other there. Put what you'd have written under **Notes for shared docs** in your report; the orchestrator applies it. A documentation file you may edit is one your brief lists in your lane.
- **Never `git commit`.** Even when certain.
- **Run the verify step before reporting.** Report its actual result, not a claim.
- **Honest environment ceiling.** Can't fully exercise it? "Done" means code-complete + tested with fakes + a runbook for the real step.
- **Match conventions, not defects.** Naming and layout yes; blob functions and status-code returns no.
- **Don't fabricate.** Unknowns become `⚠` or a question, never a "sensible default".

## Report format

Write the report to the path in your brief (`.delivery/<task-id>.md`), about 25 lines per task with no pasted code or full logs, and return only one line per task: `TASK-### · green|red · <verify summary> · ⚠ <count> · notes <count> · <report path>`. The orchestrator pays for everything you return on every later turn, and opens the file only when the line says red, `⚠`, or notes. No path in the brief: return the report itself.

- **Task:** `TASK-###`, one line
- **Files changed:** a subset of your lane
- **Interface produced:** verbatim signatures
- **Verify:** the command, its exit status, and the summary lines of its output (pass/fail counts, line coverage for your lane's files), not "tests pass". Include failure output only for a failure you couldn't fix.
- **Quality:** the self-review outcome and what you refactored, one or two lines
- **Deviations / ⚠:** assumptions, unverifiable items (with the runbook for any real-environment step), differences from the brief
- **Notes for shared docs:** anything that belongs in `CLAUDE.md`, `AGENTS.md`, or docs outside your lane (a convention you established, a command, a gotcha, a doc that is now out of date), each as the target file and the exact text to add or change. Omit when there is nothing.
- **Review response** (only after a review): per finding, fixed with re-verify evidence, or refuted with the proving case

## Red flags

| Thought | Reality |
|---|---|
| "I'll fix this neighboring file while I'm here." | Another worker's lane. Report it. |
| "I'll note this convention in `CLAUDE.md` so others know." | Not your file. Put it under Notes for shared docs; the orchestrator writes it. |
| "It's right; I'll commit." | You never commit. |
| "Looks correct; report done without running it." | Unrun tests are not evidence. |
| "The brief didn't specify this interface, but this seems reasonable." | Flag `⚠` and ask. |
| "Small task, skip the clean-code discipline." | The quick version is the clean version. |
| "Green, done." | Green isn't clean. Three passes over your diff. |
| "Mock the database; it's faster." | Real database from the Compose file. Mocks pass on queries that fail in production. |
| "Add a few assertion-free tests to reach 90%." | Coverage counts only when the test would fail on wrong behavior. |
| "Can't reach the real service, but it basically works." | Code-complete + fakes + runbook. |
| "Freehand UI is faster than Impeccable." | Freehand UI is drift. |
| "Make it configurable in case someone needs it." | YAGNI. A setting nobody varies is code to maintain and a way to misconfigure. |
| "The framework's way is awkward; I'll wire my own." | Convention over configuration. Custom wiring is a `⚠` in your report, with the reason. |
| "Hardcode this URL for now, env vars later." | Config from the environment on day one. "Later" ships. |
| "Keep it in memory; there's one instance." | The second replica or the next restart breaks it. |
| "Run the migration on startup." | Separate command. Racing replicas corrupt schemas. |
| "Try a few things and see what turns it green." | Reproduce → one hypothesis → root cause. |
| "Fourth hypothesis in; one more should do it." | You hit your ceiling. Escalate. |
| "The reviewer said fix it, so fix it." | Reproduce it first. |
| "The reviewer's probably wrong; ignore it." | Reproduce it first. |

---

*Implementation end of the pipeline; composes `uncle-bob-clean-code`. Debug and review discipline condensed from [obra/superpowers](https://github.com/obra/superpowers).*
