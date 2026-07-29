---
name: model-routed-delivery
description: Use when delivering a large multi-task build end to end — a whole project, milestone, or migration — mostly autonomously. This is the execution layer of the pipeline (plan → execute → implement): a planner rates every task's difficulty and routes it to a model tier (easy→small, medium→mid, hard→top); a top-tier orchestrator/observer (Fable) then runs waves of subagents on disjoint file paths, verifying each task is green *and* clean (an independent uncle-bob-clean-code quality pass over the diff, not just passing tests) before committing it, keeping a live ledger, and looping until everything is green. Each worker builds its task by following the clean-implementation skill; this skill owns the fleet (routing, waves, verification, commits, ledger), not how a single task is written. High-blast-radius waves run in isolated git worktrees rather than relying on disjointness discipline; a worker stuck past its debug ceiling escalates to a higher tier rather than looping. Requires a spec/PRD to exist first.
---

# Model-routed delivery

Announce at the start: **"Using model-routed-delivery: plan → rate & route → orchestrate waves → quality-gate → loop."**

You are running a **fleet**, not typing code. There are two roles, and keeping them separate is the whole point:

- **Planner** — decomposes the work into a task DAG and, for each task, assigns a **difficulty** (Easy / Medium / Hard) and the **model tier** that difficulty routes to. Its output is a written plan where every task names its files, the interface it produces, its verify step, and its model.
- **Orchestrator / observer — run this role on the top tier (Fable).** It is the session itself. It does **not** grind low tasks by hand; it dispatches each task to its routed model, **observes** (adversarially reviews) the critical ones, verifies every result, commits, updates the ledger, and re-plans. Put the strongest model here on purpose — judgement, verification, and review are the load-bearing links, not the typing.

**This skill owns the fleet, not the keystrokes.** *How* a single worker builds its one task — verify-first, clean code, UI via Impeccable, staying in its lane, reporting back — is the **`clean-implementation`** skill's job, and every dispatched worker follows it (Phase 3, step 2). This skill routes, dispatches, verifies, commits, and loops; it does not restate the worker's build doctrine. That seam is deliberate: it lets the worker be a Claude Code subagent today or a fully autonomous "dark factory" node later, without changing the floor manager.

## Phase 0 — Clarify before you plan

Do **not** plan on assumptions. Grill the requester with the questions whose answers *change the plan*: fail modes, tenancy, scope boundaries, environment ceilings, the decisions that fork the architecture. Get the decisions on the record. A wrong assumption multiplied across 80 tasks is 80 wrong tasks. (If a brainstorming/PRD skill exists, run it first and treat its output as the spec.)

## Phase 1 — Plan (the Planner)

Write a plan doc (`IMPLEMENTATION.md`, or `docs/plans/<date>-<name>.md`) containing:

- **Header**: one-sentence goal; a 2–3 sentence architecture; the stack + global constraints copied verbatim from the spec; and the milestone list (M0…Mn), each with an exit criterion.
- **Per task**: a stable id; exact **file paths** (create / modify / test); the **interface it produces** (later tasks depend on these — write the signatures down); its **verify step** (the exact build/test that proves it); its **difficulty**; its **routed model**; and — for high-blast-radius tasks — an **`isolate`** flag (build it in a dedicated worktree — see the iron rules).
- Each task is the **smallest unit that carries its own verify cycle** and that a reviewer could accept or reject on its own. Fold setup/config into the deliverable task; split only where a reviewer could reject the pieces independently.
- **Disjointness is a planning constraint**: partition tasks so the tasks in any one wave touch **non-overlapping files**. Design the seams (interfaces) so parallel agents never share a file.
- No "TBD", no "similar to task N". Undefined detail is a plan failure a subagent cannot recover from — it will guess, and guess wrong.
- **Refactoring is a legitimate task type.** A "reduce burden" task — rework a smell into a simpler or more reusable shape via `refactoring` — carries a verify step of *behavior unchanged (tests green) and the target smell gone*. Schedule debt as its own task/commit (two hats); never fold a refactor into a feature task's diff.

## Phase 2 — Rate & route

Rate each task on its **hardest aspect** (not the average), then route:

| Difficulty | Signal | Model tier |
|---|---|---|
| **Easy** | Mechanical, single-file, pattern-following, well-specified, reversible | small (fast/cheap) |
| **Medium** | Multi-file, some design judgement, integrates 2–3 components, moderate blast radius | mid |
| **Hard** | Security / money / auth / data-integrity / tenancy; concurrency or ordering; novel algorithm; a decision many tasks depend on; high blast radius | top (Fable) |

Concrete mapping today: **Easy → Haiku, Medium → Opus, Hard → Fable.** Use **unversioned family names** — "Opus" always resolves to the current Opus, so the mapping doesn't rot when a new version ships; pin a version only to reproduce a specific run. (**Sonnet is parked**: its new tokenizer plus on-by-default thinking put its *effective* cost above Opus on many tasks right now — bring it back to the mid tier when that flips.) Express it as tiers so it ages as models change. Anything on the security/money/auth/data-integrity spine is **Hard regardless of size**, and is additionally flagged **`observe`** — it gets an adversarial review pass (Phase 3, step 4) even if a mid-tier agent writes the first draft. The **same high-blast-radius judgment** that sets `observe` also marks the task **`isolate`** — record it here so Phase 3 dispatches it in its own worktree from a decision made once, not re-derived at dispatch time. One blast-radius assessment, both mitigations.

## Phase 3 — Orchestrate the waves (this is where Fable observes)

Loop until the ledger is all-green:

1. **Pick a wave** — 3–4 *ready* tasks whose file paths are disjoint. Respect the DAG: never start a task whose interface dependency hasn't landed.
2. **Dispatch** each task to its routed model as a subagent, **all in one message** so they run in parallel. Give each agent: its files, the interface it must produce, its exact verify command, the plan's global constraints, and the instruction to **build the task by following the `clean-implementation` skill** (that skill is the worker's operating manual — verify-first, clean code, Impeccable for UI, stay in its lane, never commit, report the interface back). Repeat the "never `git commit`" and disjoint-files rules explicitly in the brief; do not assume.
3. **Verify on completion — green *and* clean.** For each returned task, run its verify step **yourself** (scope to the touched packages — the tree may be transiently red from other in-flight agents; run the full suite once the wave lands). Then run a **quality pass over the task's diff** — `uncle-bob-clean-code`'s design + readability passes plus its "don't over-apply" check (its design pass now spans the dependency rule, pattern-appropriateness via `design-patterns`, and domain-model soundness via `domain-driven-design`) — **independent of the worker's self-review**, exactly as you don't trust its word on tests. A task is eligible to commit only when it is both functionally green and clean: no bloat, no needless abstraction, patterns only where the problem demands them. Over-engineered or verbose code that passes its test is a defect, not a pass — **send it back to the worker to refactor** (via `refactoring`, under `clean-implementation`'s receive-review doctrine — the same handoff as an observe finding in step 4); escalate per step 6 only if it can't come back clean.
4. **Observe the critical ones** — for every `observe`-flagged task, run an **adversarial review** before you trust it: a fresh agent (or several) told to *refute* the implementation, name the inputs that break it, prove the invariant holds. This is the observer half of the job and it is where the real bugs surface — in practice this is what caught the genuine security bugs. **Send confirmed findings back to the task's worker under `clean-implementation`'s receive-review doctrine** — the worker verifies each finding, fixes the root, and pushes back on wrong notes with evidence. Don't rubber-stamp the reviewer's suggested patch; a refutation is a claim to adjudicate, not a diff to apply.
5. **Commit** each verified task (**orchestrator only** — see iron rules), one commit per task, then **update the ledger**.
6. **Handle escalations, then re-plan.** Any task that can't be made to pass — ending red, *or* green but unable to reach the quality bar — enters the same escalation decision, whether the worker reported hitting its debug ceiling (per `clean-implementation`) or your own verify (step 3) or observe (step 4) caught what the worker missed. Do **not** re-dispatch the same brief at the same tier and expect a different result. Escalate deliberately: **bump the task up a model tier**, split it into smaller verifiable units, or fix the plan when the interface itself was wrong. Re-plan when a task reveals new work, then go again.

## The iron rules (learned the hard way — do not skip)

- **Disjoint paths, one agent per file.** Agents are *not* path-isolated — symlinked/aliased directories are the same physical files. If two agents can touch one file, they will clobber each other. Serialize them or re-seam the work.
- **Isolate high-blast-radius waves for real; don't just promise disjointness.** A wave shares one working tree, so a misbehaving agent can stray out of its lane and corrupt the run. Dispatch each `isolate`-flagged task (Phase 2) in its own git worktree (`isolation: "worktree"` on the Agent tool) so edits physically can't collide, then verify and integrate. It costs setup + disk per agent — that's why it's a flag, not the default. Isolation is a wall; disjointness is a promise.
- **Only the orchestrator commits. Subagents NEVER `git commit`.** Say this to every subagent explicitly.
- **Use `general-purpose` + a `model:` override for tier workers — NOT a fork.** A fork inherits your context *and your commit authorization* and will make rogue commits. A fresh `general-purpose` agent obeys "don't commit".
- **Verify before you commit.** Never commit on a subagent's word that tests pass — run them yourself. A green tree is the only proof.
- **The ledger is the source of truth.** Keep a `STATUS.md`: active wave, done tasks, follow-ups, incidents, decisions. Update it every wave — it's how you and the next context window know where you are.
- **Watch for zombie agents.** A subagent can die silently with zero disk output. On a quiet stretch, disk-check; if a task wrote nothing, re-dispatch it fresh — safe, because nothing was written, so nothing clobbers.
- **Batch commits; push once per milestone.** Every push burns CI runs. Commit locally per task; push once when a milestone is green (or when the user asks). Don't push per task.
- **Fail-mode per class, decided up front.** Which components fail-closed (spend, auth, model governance, budgets, safety) vs fail-open (soft quotas, rate limits). Put it in the plan so every agent implements the right one.
- **Honest environment ceiling.** If a task needs something the sandbox lacks (real cloud, signing certs, live services), "done" means code-complete + tested-with-fakes + a runbook — say exactly that; never imply production-verified.

## Phase 4 — Quality gate

Per-task quality gating (Phase 3, step 3) catches *local* bloat; this milestone pass catches the *cross-task* kind that no single worker can see. Before declaring a milestone done, run the cleanup + review skills over the accumulated diff: **`/simplify`** — the anti-verbosity pass (dedup, dead code, shared-helper consolidation; parallel builds solve the same concern several ways and this is where you collapse that) — then **`/code-review`** (correctness, plus SOLID/design and pattern-appropriateness). Fix what's real, note what's deferred and why, keep the tree green *and* clean, *then* push.

## Red flags — stop if you catch yourself thinking…

| Rationalization | Reality |
|---|---|
| "I'll just write this task myself, it's quick." | You're the orchestrator. Route it. Your job is judgement + verification, not typing. |
| "The subagent said tests pass, I'll commit." | Verify yourself. Subagents are optimistic. |
| "Two agents on adjacent code, probably fine." | It is not fine. Disjoint or serialize. |
| "This one's Hard but small — send it to the mid tier." | Route on the hardest aspect. Security-small is still Hard. |
| "I'll fork myself for speed." | Forks commit. Use `general-purpose` + a model override. |
| "I'll push after each task so it's saved." | Git holds it locally. Push once per milestone — save the CI runs. |
| "It builds, ship it." | `observe`-flagged tasks get an adversarial review *first*. |
| "The diff is huge, skip the review." | Big refactors hide subtle regressions. Run the quality gate. |
| "Tests pass — commit the task." | Green isn't good. Quality-pass the diff yourself (design + readability + over-apply) before committing — don't trust the worker's word on quality any more than on tests. |
| "Task failed — re-dispatch the same brief and hope." | Same brief, same tier, same result. Escalate — don't re-run and hope. |
| "The reviewer refuted it — apply their patch and commit." | A refutation is a claim to adjudicate, not a diff to apply — route it back through the worker. |
| "Disjoint paths are enough for this risky wave." | High blast radius → isolate. A shared tree is a broken promise waiting to happen. |

---

*The middle of a three-skill pipeline: **`requirements-driven-planning`** (produces the routed plan this skill consumes) → **`model-routed-delivery`** (this skill — routes, dispatches, verifies, commits, loops) → **`clean-implementation`** (each worker's build doctrine, which in turn composes **`uncle-bob-clean-code`**).*

*Inspired by the structure and discipline of [obra/superpowers](https://github.com/obra/superpowers) (brainstorm-before-code, plans as small verifiable tasks, fresh-agent review, `using-git-worktrees` for real isolation, `receiving-code-review` for adjudicating critique). This skill adds the difficulty→model routing table and the top-tier orchestrator/observer running a wave loop over a fleet.*
