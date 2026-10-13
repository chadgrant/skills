---
name: code-review
description: Use when reviewing code someone else wrote, or auditing a codebase: a finished feature or milestone diff; or a standalone "review this repo". Triggers: "code review", "review this", "audit the codebase", "thorough review", "security review", "is this ready to merge".
---

# Clean code review

Announce: **"Using code-review: fix the scope → run the gates → nine lenses, adversarially → verify findings → verdict."**

**Core principle: a review tries to break the code, not to approve it.** Every finding carries a `file:line` and either the input that breaks the code or the concrete cost of leaving it. A finding names a principle or smell and what it costs; taste and unevidenced suspicion are left out, and `clean` is a complete verdict. Every lens runs on every review, internal tools included. The reviewer reads and reports. It never edits the code under review, and never edits `CLAUDE.md`, `AGENTS.md`, or any other shared file; the one exception is the stamp line, written by whoever runs a full review.

Pipeline position: `chadgrant:implementation`'s orchestrator dispatches reviewers that follow this skill; its workers receive the findings. The standards are `chadgrant:clean-code`'s, including its pattern, domain-modeling, and refactoring files.

## Scope: decided by what you were handed

| You were handed | Mode | You review |
|---|---|---|
| A feature or milestone diff range, task ids, or a file list | **Scoped** | Exactly those files. Nothing else. |
| Nothing but the request to review (the skill run on its own) | **Full** | The entire codebase. |

The stamp is one line in the repo's `AGENTS.md`: `Last full review: <date> at commit <sha>`. Check it from the repo root with `bash <this skill's directory>/scripts/review-stamp.sh status`. It answers `fresh` or `stale` (14 days or 50 commits, whichever comes first; no stamp is stale).

**A stale stamp is a nag, not a trigger.** Whoever sees `stale` tells the user in one line that a full review is due and carries on with their own work. A full review runs only when the user asks for one.

## Scoped review

1. **Pin the lane.** The file list from the brief, or `git diff --name-only <range>`. That list is the whole review.
2. **Read every file in the lane in full**, not only the changed hunks. Open a neighboring file only to read an interface the lane calls or implements; neighbors are context, never review targets.
3. **Run the nine lenses** below over the lane. The spec for lens 1 is the requirements the feature satisfies.
4. **Write the report** in the shape below to the path in your brief (`.delivery/review-<id>.md`) and return only part 1, the verdict, per task, with the path. No path in the brief: return the report itself.

A scoped reviewer leaves the stamp alone. A blocker noticed outside the lane while reading an interface (an exploitable hole, data loss) gets one line under `Outside scope` and no further investigation.

## Full review

0. **Time it**: `python3 <this skill's directory>/../implementation/scripts/journal.py begin review full`, and `end review full blockers=<n> should_fix=<n> nits=<n>` after the report, so full reviews show up in the project's journal.
1. **Inventory.** `git ls-files`, minus vendored and generated code and lockfiles. Everything left is in scope: source, tests, migrations, CI config, Dockerfiles and Compose files, scripts. Partition it into units along component boundaries, each small enough to read completely (about 3,000 lines).
2. **Run the gates first.** The static gate, the full test suite with coverage, the stack's dependency audit and outdated check (see the dependencies lens), and a secret scan if one is installed. Their failures are findings; reviewers spend their attention on what tools can't see.
3. **Fan out in one message.** Top tier here means Opus unless the user has approved Fable: inside a delivery run, follow the answer recorded in the plan; standalone, ask once before fanning out, and use Opus if there's no answer.
   - One reviewer per unit, running a scoped review of that unit's files. Units holding spine code (authn/authz, money, tenancy, key or token handling) go to the top tier; the rest to the mid tier.
   - Three cross-cutting reviewers on the top tier, each reading across units: **architecture**, **security**, **operations**.
   - One **spec** reviewer on the mid tier when the repo has requirements docs: every requirement checked against the code. Without them, the report says `spec: no requirements docs`.
   - The four briefs are in [reference.md](reference.md).
   - Each writes its report to `.delivery/review-<unit>.md` and returns its verdict line.
   - No subagent tool: review the units yourself, one at a time, then the three cross-cutting reads.
4. **Consolidate.** A mid-tier agent merges the unit and cross-cutting reports into one report file: duplicates merged, a systemic smell reported once with its count and three exemplars. Read that file, not the individual reports.
5. **Adjudicate.** Verify each blocker yourself or with a fresh verifier: reproduce it with a failing test or command, or trace the path with `file:line` at each hop. A blocker that can't be verified is downgraded or dropped.
6. **Report** in the shape below.
7. **Stamp**, only when every unit was read: `bash <this skill's directory>/scripts/review-stamp.sh stamp`. A review that skipped units lists them under `Unreviewed` and writes no stamp.
8. **Hand off.** A mechanical finding with three or more occurrences is handed off as a lint rule or static-gate check plus the fixes, so tools catch it next time. The report goes to the user, who chooses what gets fixed; recommend the blockers and say roughly how much work the rest is. A full review of a living codebase always finds something, so the count alone is not a reason to fix everything. What the user picks becomes `TASK-`s (structural ones as their own refactoring tasks per `chadgrant:clean-code`'s `refactoring.md`).

## The nine lenses

Run them in this order. Checklists for lenses 3 to 8 are in [reference.md](reference.md).

1. **Spec.** Read the spec before the code, and quote its line in each finding. Three things: a requirement that is missing or partial; behavior nobody asked for (scope creep); a requirement that is implemented but wrongly. The interface produced matches the brief's signatures exactly. Names match `GLOSSARY.md`. Each implementation does what its contract's doc comment says, and its public surface is what the contract declares and no more. Code can pass every other lens and still be the wrong thing.
2. **Correctness.** For each path that takes input, name the input that breaks it: empty, null, boundary, huge, malformed, repeated, out of order, concurrent. Trace error paths, partial failures, resource and transaction lifetimes, retries and idempotency, time zones. Trace every flag combination end to end.
3. **Security.** Walk each trust boundary: who can reach this entry point, what they control, what it reaches. Injection, authn and authz on every entry point, tenancy isolation, secrets, unsafe deserialization, path traversal, SSRF, sensitive data in logs, fail-closed on spend, auth, and safety decisions.
4. **Tests.** The tests are evidence of TDD or they aren't: each behavior has a test that would fail if the behavior were wrong; tests go through the public interface; expected values come from an independent source; no assertion-free tests; 90% line coverage through behavior, with no unexplained exclusions; real backing services rather than mocks of them; one concept per test; FIRST.
5. **Reuse and duplication.** Duplicated code is the most common defect in agent-written code, because each agent writes fresh what already exists. Run the duplicate-code detector first when the stack has one (`jscpd` for JS/TS, `pylint --enable=duplicate-code` for Python, `dupl` for Go, PMD CPD for Java and C#); then look for what tools miss:
   - **Reinvented code.** New code that does what an existing function, module, framework feature, or standard library call already does. Search the codebase for it (similar names, the same signature, the same call sequence) before accepting the new code. A finding at the first occurrence, prescribed as "use `<existing>` at `file:line`".
   - **Repeated cross-cutting code.** Logging, retries, timing, caching, metrics, authorization checks, error translation, or transaction handling wrapped around business calls in more than one place. The concern is the same by definition, so the second occurrence is a finding: prescribe a **Decorator** around the interface (or the framework's middleware or interceptor, which is a Decorator the framework already ships). This is the most common reuse fix; look for it first.
   - **Duplicated logic.** The same rule, calculation, validation, mapping, or query in two or more places, in the change or between the change and the existing code. At the third occurrence, or at the second when both copies must change together, prescribe the extraction and its home (a function, a Value Object, a Template Method or Strategy for the varying part).
   - **Near-duplicates.** Copies that differ in a value or a step: prescribe the parameter, or the pattern that holds the varying step.
6. **Design.** Three checks, each ending in a named prescription:
   - **Prescribe the pattern.** Where the code has the problem a known pattern solves, say so in those words: "use a Decorator here", "this needs a Repository", "replace this switch with a Strategy". Cite the evidence (the occurrences, the growing conditional, the leaking type) and the `file:line` where the pattern goes. The evidence → pattern table is in [reference.md](reference.md); the catalogs are `chadgrant:clean-code`'s `patterns.md` and `domain-driven-design.md`.
   - **Simplicity**, per the four rules in `chadgrant:clean-code`. KISS: a layer or indirection a plain function would replace. YAGNI: an interface with one implementer, a pattern without its problem, a setting or hook with no caller. DRY: one rule or constant with several homes. Convention over configuration: a custom layout, wiring scheme, or home-made mechanism where the framework or repo has a standard one. A pattern to remove is prescribed the same way as a pattern to add.
   - **Structure.** The SOLID table and the Dependency Rule; an anemic model or a leaking aggregate.
7. **Dependencies.** In a scoped review, every dependency the change adds or changes; in a full review, all of them. Agents add old versions because they type the version they remember, so check each one against its registry, never from memory (commands per ecosystem in [reference.md](reference.md)):
   - **Not the latest stable release** when it was added: a should-fix, unless an `ADR` or the plan records why (a runtime that can't take it, a breaking change scheduled for later). In a full review, an existing dependency one or more major versions behind is a should-fix too.
   - **Known vulnerability**: high or critical is a blocker; anything lower is a should-fix with the fixed version named.
   - **Not needed**: the standard library, the framework, or a dependency already in the manifest does the job; or two dependencies do the same job.
   - **Unhealthy**: archived, deprecated, or no release in about two years; a pre-release or release candidate without a recorded reason; a version range where the stack expects an exact pin; a lockfile missing or out of sync with the manifest.
8. **Twelve-Factor** (deployable services only). Config from the environment, validated at startup; stateless processes; backing services attached by config; port from config; graceful `SIGTERM`; logs to stdout; migrations as separate commands; dev/test parity.
9. **Readability.** Names (the glossary's words where it has one), function size and single purpose, flag arguments, magic numbers, commented-out code, comments that restate the code.

## Report shape

The report is these parts, in this order, and nothing else:

1. **Verdict**, one line: `clean`, or `N blockers, N should-fix, N nits`.
2. **Lenses**, one line: each lens with its finding count or `clean`. All nine appear.
3. **Findings**, grouped by severity, each one line:
   `file:line · lens · principle or smell · the breaking input or the concrete cost · the fix, named (a refactoring, a pattern, a factor)`
4. **Outside scope** (scoped) or **Unreviewed** and the **stamp line** written (full).

| Severity | Means |
|---|---|
| Blocker | A dependency with a known high or critical vulnerability, a requirement missing or implemented wrongly, wrong behavior, an exploitable hole, data loss or corruption, a secret in the repo, a test gate that passes on broken code |
| Should-fix | A dependency not at its latest stable release, reinvented or duplicated code, scope creep, or a design, test, or Twelve-Factor defect that makes the next change harder or riskier |
| Nit | Readability |

A scoped report for several tasks repeats parts 1–3 per task.

---

*Review end of the pipeline; applies `chadgrant:clean-code` and the service and test gates from `chadgrant:implementation`. Checklists and cross-cutting briefs in [reference.md](reference.md).*
