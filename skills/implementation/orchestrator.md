# Orchestrator: deliver a multi-task plan

Own the plan, dispatch, verification, integration, and ledger. Workers implement tasks under [worker.md](worker.md). Follow the shared rules in [SKILL.md](SKILL.md), prefer Forks under [delegation.md](delegation.md), and use [routing.md](routing.md) when selecting tiers/models.

## Context and journal

- Keep source discovery and logs out of the main context unless needed for a decision. Do bounded searches directly; delegate substantial investigation, preferably to a Fork. Reuse inherited context and existing maps.
- Reports live in `.delivery/` in the main checkout. Add that directory to `.git/info/exclude` once and give workers absolute report paths. Read reports when their one-line result flags failure, findings, notes, or contract changes.
- Use quiet/failures-only gate output, or capture logs and print a bounded tail **while preserving the gate's exit status**. Batch independent checks.
- Record run/phase/task/gate/review events using [journal.md](journal.md); hooks already record tool and agent timing. Continue the run ID from the plan or `STATUS.md`.
- Update `STATUS.md` after each wave: run ID, plan path, active/next wave, task states, decisions, incidents, follow-ups. At a milestone boundary, leave enough context for a fresh session. Use a handoff at a wave boundary if context becomes unwieldy; do not rely on a fixed token-to-cost ratio.

## 0. Establish the inputs

Use the existing spec and routed plan. Resolve only material unanswered decisions: scope, fail modes, tenancy, environment limits, architecture forks. Ask independent questions together in numbered rounds with recommendations; find facts in the repo. Honor recorded model choices and Fable authorization from [routing.md](routing.md).

On an existing repo, ensure `AGENTS.md` has a current architecture note (about 60 lines): module locations, wiring/registration, hot files, test commands, fresh-worktree setup. Have an investigator propose changes; apply shared-file edits yourself.

Run `bash <skill directory>/../code-review/scripts/review-stamp.sh status`. If stale, mention once that a full review is due and continue. Never start a full audit without the user's request.

## 1. Validate the plan

Keep the plan at its existing path, otherwise `IMPLEMENTATION.md` or `docs/plans/<date>-<name>.md`. Check these fields; fill only actual gaps:

- **Header:** goal, architecture, stack, global constraints, run ID, `max_parallel` (default 4, bounded by available capacity), milestones and exit criteria. Keep shared constraints in one heading for briefs to reference.
- **Static gate:** format check, lint, types, complexity limit in one command; creating a missing gate is an M0 task.
- **Fast gate:** unit/self-contained tests plus static checks; no Docker or backing services. Each worker runs it, then you run it once on the merged wave.
- **Full gate:** integration against real backing services (Compose with health checks where used), coverage with a 90% fail-under threshold and explicit exclusions, and e2e through the public surface. Browser → Playwright; API → HTTP; CLI → built binary; library → public-API tests. Only you run this gate at milestone completion. M0 provides the harness; feature tasks own their scenarios.
- **Contracts:** each milestone lists `CON-###` entries before tasks: final file, members, behavior, errors, invariants, examples. One initial task writes contracts/stubs/tests; exactly one implementation task owns each contract.
- **Tasks:** stable ID, requirement IDs, contracts implemented/consumed, hot files, difficulty/tier, `observe`, deliverable, exact verify command. A task is a cohesive module or feature slice through its layers, usually at most about 400 changed lines; never split one feature by layer. Combine tiny coupled tasks.
- **Team size:** fewer than three independent implementation tasks, or one tightly coupled algorithm/state machine, goes to one worker that authors then implements contracts sequentially. Mark that contract-authoring role explicitly; implementation still respects the agreed contract. Otherwise, freeze contracts before parallel implementation.
- **Hot files:** identify registries, wiring, shared enums, migrations. Give each conflicting file one owner per wave; use separate waves or small M0 changes where necessary. Worktrees isolate edits but do not eliminate merge conflicts.
- **Constraints:** UI style guide/Impeccable, Twelve-Factor services, current dependency versions, and fail modes. Fail closed for spend/auth/governance/budgets/safety; document any fail-open soft quota/rate-limit policy. Follow the four simplicity rules in `clean-code`; each task needs a stated requirement. Refactoring tasks preserve behavior and have their own verification/commit.

No undefined placeholders or references such as “similar to task N.” Use [routing.md](routing.md) to rate the hardest aspect, including the narrow `observe` definition.

## 2. Write and freeze milestone contracts

1. Assign one contract author, preferably a Fork, with a model suitable for the milestone's risk. Write interfaces/protocols/traits and shared types at their final paths. Fully define data shapes; implementation stubs throw the language's not-implemented error.
2. Every member's doc comment specifies inputs, outputs, behavior, errors, invariants, and an example in glossary terms. A bare signature is incomplete.
3. Write contract tests against the public interface. Run them on stubs and confirm failure for the expected reason. Wire stubs into the composition root so the build/static gate passes. The contract task is the explicit exception to a green behavioral-test gate.
4. Inspect the contract diff against requirements, the glossary, and every consumer task. Commit contracts separately before parallel implementations start.
5. Freeze contracts and contract tests. On a worker's change request, assess and implement the correction as orchestrator or assign an explicit contract-author task. Merge it, mark affected implementations/consumers stale, notify active workers via `SendMessage`, and update pending briefs, `STATUS.md`, and `J note`. Repeated requests mean the plan needs refinement.

Workers coordinate through contracts, tests, the plan, and reports. Do not relay worker-to-worker conversation as a substitute for those artifacts.

## 3. Run waves

1. **Select:** at most `max_parallel` workers, including fix/conflict workers and Forks. Tasks depend on merged contracts; hold a task only for a real implementation/data dependency or shared-file conflict.
2. **Map:** reuse or prepare a map of about 40 lines per task: file ranges, existing helpers/components to reuse, tests, and wiring points. Batch related discovery; do not spawn a mapper for a trivial lookup.
3. **Dispatch together:** use [delegation.md](delegation.md). The brief includes task/goal, map, current integration SHA, `REQ`s, implemented/consumed `CON`s and contract tests, fast gate, pointers to global constraints/glossary, worker role, absolute report path, and one-line return. Include the short no-commit/no-Docker/no-shared-doc/no-contract-edit boundary. Prefer worktree-isolated Forks; use non-fork agents for required model/effort/tool differences. Do not paste already inherited specs.
4. **Integrate green tasks:** check actual gate evidence and `git diff --stat` for scope, commit on the worker branch, then merge in dependency order. If conflicted, resume the owning worker to merge the integration branch with `--no-commit`, resolve, and re-run the fast gate; you commit/merge afterward. Remove merged worktrees. Apply proposed shared-doc changes yourself, merging duplicates.
5. **Verify once:** run the fast gate on the merged tree. Red → identify the owning task and resume its worker; green → next wave. Full integration/e2e waits for the milestone.
6. **Escalate:** do not repeat an unsuccessful brief unchanged at the same tier. Correct a bad brief/contract, split an oversized task, or increase capability for a sound task the worker could not complete. Record new work in the plan. Before resubmitting a silent worker, inspect its state and journal: a task that never ran may be retried; partial work requires diagnosis.

## 4. Close the milestone

Run the full gate on the merged tree. Start backing services only for it and stop them afterward. Failures become owning-task fix work; apply the escalation rules instead of looping indefinitely. Simplify the accumulated diff (reuse, dead code, redundant abstractions), using `/simplify` if available; re-run affected checks after edits.

Review the feature once with `chadgrant:code-review` in scoped mode over `git diff <milestone-start>..HEAD`, using its `REQ`s as the spec. Use a mid-tier reviewer; add a top-tier security reviewer over `observe` files. Follow the Fork/fresh-context guidance in [delegation.md](delegation.md). Give each the changed-file list, an explicit budget (about 45 minutes by default), and **distinct** paths: `.delivery/review-<milestone>.md` and `.delivery/review-<milestone>-security.md`. Return verdict lines only.

Group blockers and should-fix findings by owner for one fix pass under [worker.md](worker.md). List nits without automatically fixing them. Re-run the full gate after fixes; unresolved findings are escalated or explicitly deferred in `STATUS.md`, never labeled resolved. No automatic second full review.

Compact requirements when due under [compact.md](../planning/compact.md), in a separate commit. A short retrospective may inspect reports and propose up to ten improvements: repeated mechanical findings → static checks; repeated discovery → architecture pointers; repeated assumptions → better briefs. Apply only supported changes and prune obsolete shared instructions.

Summarize gate evidence, deferrals, and useful journal totals. Refresh `STATUS.md` for the next milestone. Push once per milestone within the user's authorized delivery scope; do not infer deployment authorization from passing gates.
