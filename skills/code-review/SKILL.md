---
name: code-review
description: Review a PR, diff, branch, file, or dependency change, or audit a codebase. Report verified correctness, security, design, test, and maintenance findings within the requested scope.
---

# Code review

Announce the review scope. Read and report; do not edit reviewed code or shared instructions. The only shared-file exception is the stamp after a completed full review. Every finding needs a location and a breaking input or concrete cost; `clean` is a complete verdict.

## Choose scope and load only what it needs

| Input | Procedure |
|---|---|
| PR, diff range, branch, task IDs, or file list | Scoped review below |
| Explicit whole-codebase audit | [full-review.md](full-review.md) |
| No identifiable target | Establish the intended scope before starting a full audit |

A stale full-review stamp never expands a scoped review. The script `bash <skill directory>/scripts/review-stamp.sh status` reports freshness (14 days or 50 commits; absent means stale). Mention staleness once when relevant and continue. Only a user-requested full review may refresh it.

## Scoped review

1. Pin the file list from the brief or `git diff --name-only <range>`. These are the review targets.
2. Read the relevant requirements and contracts, then changed hunks and enough surrounding code to judge them; read an entire small file when useful. Open neighbors only to understand called interfaces. An incidental outside-scope blocker gets one line, no expanded investigation.
3. Apply [lenses.md](lenses.md) in order: spec, correctness, security, tests, reuse, design, dependencies, Twelve-Factor, readability. Use [clean-code](../clean-code/SKILL.md) as the standards; load its catalogs only for a specific design question. Open only needed checklist sections in [reference.md](reference.md).
4. Run relevant available checks within scope and budget. Verify blockers with a reproducer or a traced path, citing locations. Do not turn speculation into findings; identify checks you could not run.
5. Write the report to the brief's path (usually `.delivery/review-<id>.md`), returning only each task's verdict and the path. With no report path, return the report itself. Honor any time/tool budget; list unfinished coverage under `Unreviewed`.

Leave the full-review stamp unchanged.

## Report shape

1. **Verdict:** `clean` or `N blockers, N should-fix, N nits`.
2. **Lenses:** all nine, each with a finding count, `clean`, `n/a` with a reason, or `unreviewed`. Do not label an unchecked lens clean.
3. **Findings:** severity order, concise entries:
   `file:line · lens · principle/smell · breaking input or concrete cost · named fix`
4. **Coverage:** `Outside scope` for incidental findings; `Unreviewed` for gaps, unavailable checks, or exhausted budget. Full reviews also state whether a stamp was written.

| Severity | Criteria |
|---|---|
| Blocker | Wrong/missing required behavior, exploitable hole, data loss, leaked secret, high/critical vulnerable dependency, or a gate that passes broken code |
| Should-fix | Unjustified outdated/unneeded dependency, duplication, scope creep, or design/test/operations defect with a concrete maintenance cost |
| Nit | Readability |

For several tasks, repeat verdict, lenses, and findings per task. Explain missing requirements evidence instead of inventing a spec. All lenses are considered; not every lens must produce a finding.
