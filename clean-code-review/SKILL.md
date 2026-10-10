---
name: clean-code-review
description: Use when reviewing code someone else wrote, or auditing a codebase: a dispatched reviewer checking a task, wave, or feature diff; a milestone gate; a standalone "review this repo"; or a full-review stamp in AGENTS.md that has gone stale. Triggers: "code review", "review this", "audit the codebase", "thorough review", "security review", "is this ready to merge".
---

# Clean code review

Announce: **"Using clean-code-review: fix the scope → run the gates → six lenses, adversarially → verify findings → verdict."**

**Core principle: a review tries to break the code, not to approve it.** Every finding carries a `file:line` and either the input that breaks the code or the concrete cost of leaving it. A finding without evidence is an opinion; drop it. The reviewer reads and reports. It never edits the code under review, and never edits `CLAUDE.md`, `AGENTS.md`, or any other shared file; the one exception is the stamp line, written by whoever runs a full review.

Pipeline position: `implementation`'s orchestrator dispatches reviewers that follow this skill; its workers receive the findings. The standards are `uncle-bob-clean-code`'s, including its pattern, domain-modeling, and refactoring files.

## Scope: decided by what you were handed

| You were handed | Mode | You review |
|---|---|---|
| A task brief, task ids, a diff range, or a file list | **Scoped** | Exactly those files. Nothing else. |
| Nothing but the request to review (the skill run on its own) | **Full** | The entire codebase. |
| The start of a delivery run, or a milestone gate, where the stamp reads `stale` | **Full** | The entire codebase. |

The stamp is one line in the repo's `AGENTS.md`: `Last full review: <date> at commit <sha>`. Check it from the repo root with `bash <this skill's directory>/scripts/review-stamp.sh status`. It answers `fresh` or `stale` (14 days or 50 commits, whichever comes first; no stamp is stale).

## Scoped review

1. **Pin the lane.** The file list from the brief, or `git diff --name-only <range>`. That list is the whole review.
2. **Read every file in the lane in full**, not only the changed hunks. Open a neighboring file only to read an interface the lane calls or implements; neighbors are context, never review targets.
3. **Check the brief.** The interface produced matches the brief's signatures exactly, and the verify step would fail if the behavior were wrong.
4. **Run the six lenses** below over the lane.
5. **Write the report** in the shape below to the path in your brief (`.delivery/review-<id>.md`) and return only part 1, the verdict, per task, with the path. No path in the brief: return the report itself.

A scoped reviewer leaves the stamp alone. A blocker noticed outside the lane while reading an interface (an exploitable hole, data loss) gets one line under `Outside scope` and no further investigation.

## Full review

1. **Inventory.** `git ls-files`, minus vendored and generated code and lockfiles. Everything left is in scope: source, tests, migrations, CI config, Dockerfiles and Compose files, scripts. Partition it into units along component boundaries, each small enough to read completely (about 3,000 lines).
2. **Run the gates first.** The static gate, the full test suite with coverage, the stack's dependency audit (`npm audit`, `pip-audit`, `govulncheck`, `cargo audit`), and a secret scan if one is installed. Their failures are findings; reviewers spend their attention on what tools can't see.
3. **Fan out in one message.** Top tier here means Opus unless the user has approved Fable: inside a delivery run, follow the answer recorded in the plan; standalone, ask once before fanning out, and use Opus if there's no answer.
   - One reviewer per unit, running a scoped review of that unit's files. Units holding spine code (authn/authz, money, tenancy, key or token handling) go to the top tier; the rest to the mid tier.
   - Three cross-cutting reviewers on the top tier, each reading across units: **architecture**, **security**, **operations**. Their briefs are in [reference.md](reference.md).
   - Each writes its report to `.delivery/review-<unit>.md` and returns its verdict line.
   - No subagent tool: review the units yourself, one at a time, then the three cross-cutting reads.
4. **Consolidate.** A mid-tier agent merges the unit and cross-cutting reports into one report file: duplicates merged, a systemic smell reported once with its count and three exemplars. Read that file, not the individual reports.
5. **Adjudicate.** Verify each blocker yourself or with a fresh verifier: reproduce it with a failing test or command, or trace the path with `file:line` at each hop. A blocker that can't be verified is downgraded or dropped.
6. **Report** in the shape below.
7. **Stamp**, only when every unit was read: `bash <this skill's directory>/scripts/review-stamp.sh stamp`. A review that skipped units lists them under `Unreviewed` and writes no stamp.
8. **Hand off.** Blockers and should-fix findings become work for someone else: `TASK-`s in the pipeline (structural ones as their own refactoring tasks per `uncle-bob-clean-code`'s `refactoring.md`), or the list handed to the user when run standalone.

## Re-review (after a fix)

One round, on the small or mid tier. The scope is the original findings and the lines the fix changed (`git diff` of the fix), nothing else. For each finding: fixed, with the evidence, or still open. Then the six lenses over the changed lines only. A finding still open goes back as an escalation, not a third round.

## The six lenses

Run them in this order. Checklists for lenses 2 to 5 are in [reference.md](reference.md).

1. **Correctness.** For each path that takes input, name the input that breaks it: empty, null, boundary, huge, malformed, repeated, out of order, concurrent. Trace error paths, partial failures, resource and transaction lifetimes, retries and idempotency, time zones. Trace every flag combination end to end.
2. **Security.** Walk each trust boundary: who can reach this entry point, what they control, what it reaches. Injection, authn and authz on every entry point, tenancy isolation, secrets, unsafe deserialization, path traversal, SSRF, sensitive data in logs, fail-closed on spend, auth, and safety decisions.
3. **Tests.** The tests are evidence of TDD or they aren't: each behavior has a test that would fail if the behavior were wrong; no assertion-free tests; 90% line coverage through behavior, with no unexplained exclusions; real backing services rather than mocks of them; one concept per test; FIRST.
4. **Design.** Three checks, each ending in a named prescription:
   - **Prescribe the pattern.** Where the code has the problem a known pattern solves, say so in those words: "use a Decorator here", "this needs a Repository", "replace this switch with a Strategy". Cite the evidence (the occurrences, the growing conditional, the leaking type) and the `file:line` where the pattern goes. The evidence → pattern table is in [reference.md](reference.md); the catalogs are `uncle-bob-clean-code`'s `patterns.md` and `domain-driven-design.md`.
   - **Simplicity**, per the four rules in `uncle-bob-clean-code`. KISS: a layer or indirection a plain function would replace. YAGNI: an interface with one implementer, a pattern without its problem, a setting or hook with no caller. DRY: one rule or constant with several homes. Convention over configuration: a custom layout, wiring scheme, or home-made mechanism where the framework or repo has a standard one. A pattern to remove is prescribed the same way as a pattern to add.
   - **Structure.** The SOLID table and the Dependency Rule; an anemic model or a leaking aggregate.
5. **Twelve-Factor** (deployable services only). Config from the environment, validated at startup; stateless processes; backing services attached by config; port from config; graceful `SIGTERM`; logs to stdout; migrations as separate commands; dev/test parity.
6. **Readability.** Names, function size and single purpose, flag arguments, magic numbers, duplication, commented-out code, comments that restate the code.

## Report shape

The report is these parts, in this order, and nothing else:

1. **Verdict**, one line: `clean`, or `N blockers, N should-fix, N nits`.
2. **Lenses**, one line: each lens with its finding count or `clean`. All six appear.
3. **Findings**, grouped by severity, each one line:
   `file:line · lens · principle or smell · the breaking input or the concrete cost · the fix, named (a refactoring, a pattern, a factor)`
4. **Outside scope** (scoped) or **Unreviewed** and the **stamp line** written (full).

| Severity | Means |
|---|---|
| Blocker | Wrong behavior, an exploitable hole, data loss or corruption, a secret in the repo, a test gate that passes on broken code |
| Should-fix | A design, test, or Twelve-Factor defect that makes the next change harder or riskier |
| Nit | Readability |

A scoped report for several tasks repeats parts 1–3 per task.

## Red flags

| Thought | Reality |
|---|---|
| "While I'm here, this neighboring module also looks off." | Scoped means the lane. One `Outside scope` line for a blocker; otherwise leave it. |
| "The stamp is stale, so I'll widen this task review." | A dispatched reviewer stays in its lane. The orchestrator runs the full review at the start of a run or at the milestone gate. |
| "I'll sample a few files per package." | A full review reads every unit. Skipped units go under `Unreviewed` and there is no stamp. |
| "Mostly reviewed; stamp it." | The stamp says every unit was read. Otherwise it lies to the next fifty commits. |
| "This looks exploitable; report it as a blocker." | Reproduce it or trace it hop by hop first. |
| "Tests pass and coverage is 92%; the test lens is clean." | Read the assertions. Coverage counts executed lines, not checked behavior. |
| "It would be more flexible with a Strategy here." | Flexibility isn't evidence. Prescribe a pattern when the code shows its problem today; otherwise it's speculative generality. |
| "There's a smell here; I'll flag it and let the worker pick the fix." | Name the pattern or refactoring and where it goes. "Tangled" is not actionable; "extract a Repository for the six queries in `OrderService`" is. |
| "The duplication is small; no need to mention a pattern." | Three occurrences of the same wrapping logic is the evidence a Decorator needs. Prescribe it. |
| "I'd have written it differently." | Taste isn't a finding. Name the principle and the cost. |
| "Nothing serious; I'll list some nits so the review has content." | `clean` is a complete verdict. |
| "While re-reviewing, I'll take another full pass." | A re-review is the findings and the fix's lines. A fresh full pass restarts the round count. |
| "The fix is two lines; I'll just make it." | Reviewers don't edit. The finding goes to the worker. |
| "It's an internal tool; skip the security lens." | Internal tools hold credentials too. All six lenses, every time. |

---

*Review end of the pipeline; applies `uncle-bob-clean-code` and the service and test gates from `implementation`. Checklists and cross-cutting briefs in [reference.md](reference.md).*
