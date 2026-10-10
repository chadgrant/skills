# Clean code review: checklists and briefs

Open the section the lens or the reviewer role calls for.

## Security lens

For each entry point (HTTP route, queue consumer, CLI argument, file import, webhook, scheduled job), answer: who can reach it, what do they control, what can it touch.

| Area | Look for |
|---|---|
| Injection | Queries, shell commands, templates, or paths built by concatenating input; missing parameterization; `eval` or dynamic import on input |
| Authentication | An entry point with no identity check; tokens or sessions that never expire or can't be revoked; credentials compared without constant time; home-grown crypto or password hashing |
| Authorization | Identity checked but ownership not (fetching a record by id without checking it belongs to the caller); checks in the UI or controller only, not where the data is loaded; role checks that default to allow |
| Tenancy | A query without the tenant predicate; tenant id taken from the request body instead of the authenticated identity; shared caches keyed without the tenant |
| Secrets | Keys, tokens, or passwords in code, config files, test fixtures, or git history; secrets written to logs, error messages, or URLs |
| Input and output | Missing validation at the boundary (type, length, range, format); unbounded sizes or page limits; output rendered without encoding; unsafe deserialization of untrusted bytes |
| Files and network | Path traversal through user-supplied names; SSRF through user-supplied URLs; uploads without type and size limits; TLS verification disabled |
| Failure mode | Spend, auth, governance, and safety decisions that fail open on error or timeout; exceptions swallowed around a security check |
| Data exposure | Personal or sensitive data in logs; over-wide API responses (whole records serialized); stack traces returned to clients |
| Dependencies | Audit-tool findings; unpinned or abandoned packages; a dependency pulled at build time from an unverified source |
| Concurrency | Check-then-act on balances, quotas, or uniqueness without a transaction or lock; non-idempotent handlers behind a retrying queue |

## Tests lens

| Look for | Why it's a finding |
|---|---|
| A behavior in the code with no test that would fail if it were wrong | Untested behavior is unproven behavior |
| Tests with no assertion, or asserting only "no exception" or that a mock was called | They raise coverage without checking anything |
| Coverage under 90% of lines, or files excluded without a recorded reason | The gate is the plan's; a quiet exclusion defeats it |
| A database, queue, or cache mocked or swapped for an in-memory substitute | Mocks pass on queries that fail in production |
| Tests that depend on order, wall-clock time, sleeps, or shared state | Flaky tests train people to ignore red |
| Several concepts in one test; setup that hides what's being tested | A failure doesn't say what broke |
| An e2e driver that doesn't fit the surface (Playwright without a browser UI) | Slow and proves the wrong thing |
| Tests mirroring the implementation line for line | They pin structure, so every refactoring breaks them |
| Error paths and boundaries untested while the happy path has five tests | The bugs live at the edges |

## Design lens: evidence → pattern to prescribe

A prescription needs evidence in the code today. State it as the finding: the evidence with its count, the pattern, and where it goes. All three are files in `chadgrant:clean-code`: catalogs and the "don't use when" column in `patterns.md`, domain building blocks in `domain-driven-design.md`, the steps to get there in `refactoring.md`.

| Evidence in the code | Prescribe |
|---|---|
| Logging, caching, retries, timing, metrics, or permission checks repeated inside several business methods, or wrapped around them by copy-paste | **Decorator** around the interface (or the framework's middleware or interceptor) |
| Queries or ORM calls scattered through services and controllers; the same query written more than once; business logic that can't be tested without a database | **Repository** per aggregate root (Data Mapper behind it) |
| A `switch` or `if` chain on a type code or mode, repeated in several places or about to gain a case | **Strategy**, or replace conditional with polymorphism |
| Behavior that depends on a status field, with the legal transitions checked by conditionals spread over several methods | **State** |
| A third-party SDK's types or errors appearing in business logic; calls to one external API from many places | **Adapter** or **Gateway** at the boundary; an **Anticorruption Layer** when it's another system's model |
| Callers that must make five calls in the right order to use a subsystem | **Facade** |
| A constructor with many optional or same-typed parameters; objects built half-valid and fixed up afterwards | **Builder**, or a **Factory** that returns only valid objects |
| `new ConcreteThing()` chosen by conditionals in several places | **Factory Method** |
| A method that directly calls every party interested in a change (send email, update stats, write audit) and grows with each new one | **Observer**, or a **Domain Event** |
| Requests passed through a hand-written sequence of checks, each able to stop the chain | **Chain of Responsibility** (the framework's middleware pipeline) |
| Operations that need to be queued, retried, logged, or undone, implemented as ad-hoc flags and parameters | **Command** |
| Several classes repeating the same algorithm skeleton with one or two steps different | **Template Method**, or **Strategy** for the varying step |
| The same `if (x == null)` guard before every use of a collaborator | **Null Object**, or an option type |
| Money, date ranges, emails, ids, or quantities passed as bare strings and numbers, validated again at each use | **Value Object** |
| The same three or four parameters travelling together through many signatures | **Parameter Object** (a refactoring; see `refactoring.md`) |
| Controllers holding business rules; the same use case implemented in an HTTP handler and a job | **Service Layer** |
| Several repositories saved in one use case with hand-managed transactions | **Unit of Work** |
| Entities that are bags of getters and setters while services hold all the rules | Move behavior onto the **aggregate** that owns the invariant |
| Global mutable state reached through a static accessor | Inject one instance from the composition root (remove the **Singleton**) |

**Patterns to remove** are prescribed the same way: an interface with one implementer and no test double → inline it; a Factory that only calls a constructor → call the constructor; a Strategy with one strategy → a function; an event with one in-process listener that must run synchronously → a method call; a Repository over a two-table CRUD app whose ORM already is one → use the ORM directly.

**Convention over configuration**: before prescribing a hand-built pattern, check whether the framework ships it. The prescription is then "use the framework's X", and a home-made parallel of something the framework provides is itself a finding.

**Severity**: should-fix when the evidence is costing something now (three or more occurrences, a conditional that grew in this diff, a bug traceable to the missing structure); a nit when it's a single mild instance.

## Twelve-Factor lens

Services only. A factor waived by an `ADR` is not a finding.

| Factor | Finding |
|---|---|
| II Dependencies | Reliance on a host-installed tool; a missing or uncommitted lockfile |
| III Config | A URL, credential, flag, or limit in code or a per-environment file; config read lazily instead of validated at startup |
| IV Backing services | A database, queue, or third-party API located by anything other than config |
| V Build, release, run | Config baked into the build artifact |
| VI Processes | Session, cache, or upload state held in process memory or on local disk |
| VII Port binding | A hardcoded port |
| IX Disposability | No `SIGTERM` handling; in-flight work dropped on shutdown; jobs unsafe to retry |
| X Parity | SQLite or an in-memory fake in dev or test where production runs something else |
| XI Logs | Writing or rotating log files; buffered output |
| XII Admin processes | Migrations run at application startup |

## Cross-cutting reviewer briefs (full review)

Each cross-cutting reviewer gets the unit map from the inventory and reads across units. Each returns findings in the skill's report shape.

**Architecture.** Draw the dependency graph between components from the imports. Report: policy depending on detail (domain code importing the framework, the ORM, or the transport); dependency cycles; a component with several unrelated reasons to change; the same concept implemented twice in different units; bounded contexts sharing a model or a table; a layer bypassed (a controller reaching the database around the service or repository); the same cross-cutting concern or structural problem solved differently in different units (convention over configuration: one way per codebase); machinery nothing uses (YAGNI). Prescribe the pattern or refactoring that resolves each, from the design-lens table above.

**Security.** List every entry point in the codebase, then walk the security lens table for each one end to end, across unit boundaries, following input from the boundary to every sink it reaches. Unit reviewers see one unit; this role finds the hole between two units that each look fine alone. Also read CI config, Dockerfiles, and Compose files for secrets, privileged containers, and unpinned base images.

**Operations.** For each deployable service, walk the Twelve-Factor lens table. Then check what the table doesn't: health and readiness endpoints, timeouts and retry limits on every outbound call, bounded queues and pools, and migrations that can run while the previous version is still serving.

## Unit reviewer brief (full review)

Give each unit reviewer: the unit's file list, the stack and global constraints from the plan or `AGENTS.md`, the instruction to follow `chadgrant:code-review` in scoped mode over exactly those files, and the report shape. Tell it to read every file in full and to return findings only.
