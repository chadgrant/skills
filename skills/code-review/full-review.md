# Full codebase review

Read only for an explicitly requested whole-codebase review. Follow [SKILL.md](SKILL.md) for scope and reporting.

0. **Time it**: `python3 <this skill's directory>/../implementation/scripts/journal.py begin review full`, and `end review full blockers=<n> should_fix=<n> nits=<n>` after the report, so full reviews show up in the project's journal.
1. **Inventory.** `git ls-files`, minus vendored and generated code and lockfiles. Everything left is in scope: source, tests, migrations, CI config, Dockerfiles and Compose files, scripts. Partition it into units along component boundaries, each small enough to read completely (about 3,000 lines).
2. **Run the gates first.** The static gate, the full test suite with coverage, the stack's dependency audit and outdated check (see the dependencies lens), and a secret scan if one is installed. Their failures are findings; reviewers spend their attention on what tools can't see.
3. **Dispatch within available concurrency.** Batch independent reviewers; do not exceed the plan's cap or tool capacity. Use [routing.md](../implementation/routing.md) for tiers and [delegation.md](../implementation/delegation.md) for Forks and fallbacks; honor the recorded model choice.
   - One reviewer per unit, running a scoped review of that unit's files. Units holding spine code (authn/authz, money, tenancy, key or token handling) go to the top tier; the rest to the mid tier.
   - Three cross-cutting reviewers on the top tier, each reading across units: **architecture**, **security**, **operations**.
   - One **spec** reviewer on the mid tier when the repo has requirements docs: every requirement checked against the code. Without them, the report says `spec: no requirements docs`.
   - The four briefs are in [reference.md](reference.md).
   - Each writes its report to `.delivery/review-<unit>.md` and returns its verdict line.
   - No subagent tool: review the units yourself, one at a time, then the cross-cutting reads, including spec when requirements exist.
4. **Consolidate.** A mid-tier agent (or you, without delegation) merges the unit and cross-cutting reports into one report file: duplicates merged, a systemic smell reported once with its count and three exemplars. Read that file, not the individual reports.
5. **Adjudicate.** Verify each blocker yourself or with a fresh verifier: reproduce it with a failing test or command, or trace the path with `file:line` at each hop. A blocker that can't be verified is downgraded or dropped.
6. **Report** in the [report shape](SKILL.md#report-shape).
7. **Stamp**, only when every unit was read: `bash <this skill's directory>/scripts/review-stamp.sh stamp`. A review that skipped units lists them under `Unreviewed` and writes no stamp.
8. **Hand off.** A mechanical finding with three or more occurrences is handed off as a lint rule or static-gate check plus the fixes, so tools catch it next time. The report goes to the user, who chooses what gets fixed; recommend the blockers and say roughly how much work the rest is. Finding count alone is not a reason to fix everything; a clean review is valid. What the user picks becomes `TASK-`s (structural ones as their own refactoring tasks per `chadgrant:clean-code`'s `refactoring.md`).
