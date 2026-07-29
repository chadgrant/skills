# uncle-bob

An [Agent Skill](https://agentskills.io) that makes coding agents write and review code the Uncle Bob way — Robert C. Martin's *Clean Code* and SOLID, plus *Clean Architecture* and McConnell's *Code Complete* construction discipline — applied automatically whenever an agent writes, modifies, or reviews code. It's the foundation of a **design canon** (see the collection's [top-level README](../README.md)); the sibling skills [`design-patterns`](../design-patterns/), [`domain-driven-design`](../domain-driven-design/), and [`refactoring`](../refactoring/) carry the design knowledge above unit-of-code altitude.

## What it does

- **When writing code:** small single-purpose functions, intention-revealing names, no flag arguments, exceptions over status codes, no magic numbers, no commented-out code, SOLID at genuine seams, Clean Architecture's dependency rule, and defensive-programming construction — plus a "don't over-apply" table so agents don't turn a 40-line feature into an enterprise class hierarchy.
- **When reviewing code:** three required passes in severity order — correctness & security, design (SOLID + architecture: dependency rule, missing/misapplied pattern, anemic domain model), readability — with each finding named by principle or smell and an explicit blockers / should-fix / nits verdict.
- **Composes the canon:** points to `design-patterns`, `domain-driven-design`, and `refactoring` when a design problem, domain-modeling need, or accumulated burden is above the clean-code layer.
- **Under pressure:** a rationalization table counters the classic excuses ("no time", "match the existing style", "don't gold-plate it", "just LGTM it") that make agents ship smells.

## Files

- [`SKILL.md`](SKILL.md) — the operative skill: rules, review passes, the design-canon composition, rationalization table, red flags
- [`reference.md`](reference.md) — the full teachings: *Clean Code* chapter by chapter, SOLID with examples, Clean Architecture (dependency rule, component principles), Construction (*Code Complete*), the smells catalog, and a worked before/after refactor

## Install

This skill lives in the [`chadgrant/skills`](https://github.com/chadgrant/skills) collection under `uncle-bob-clean-code/`. Clone the repo and copy that folder into your agent's skills directory.

**Claude Code — everywhere (all projects):**

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/uncle-bob-clean-code ~/.claude/skills/
```

**Claude Code — one project:**

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/uncle-bob-clean-code .claude/skills/
```

**Other agents:** any agent supporting the [Agent Skills spec](https://agentskills.io/specification) can use this — copy the `uncle-bob-clean-code/` folder into that agent's skills directory.

The skill triggers automatically on its description ("Use when writing, modifying, or refactoring code… or when reviewing code…"). To make it unconditional in Claude Code, add one line to `~/.claude/CLAUDE.md`:

```
Whenever you write, modify, or review code, apply the uncle-bob-clean-code skill.
```

## How it was built

Skill-TDD: baseline agents were run through pressure scenarios *without* the skill (they happily shipped one-blob functions with single-letter names when told "match our style, don't gold-plate it", and wrote reviews that caught bugs but skipped design entirely). The skill was written to counter those exact failures, then verified against the same scenarios and iterated until the loopholes closed.

## Attribution

Distilled from Robert C. Martin's *Clean Code*, *The Clean Coder*, *Clean Architecture*, and *Agile Software Development: Principles, Patterns, and Practices*. This is an independent summary for agent use; buy the books — they're worth it.
