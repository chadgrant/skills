# Reusable project verification

Read when authoring or updating repeatable runtime instructions. Inspect existing docs, scripts, tests, and package commands first. Extend the existing source of truth; otherwise use `docs/verification.md`. Create a project-local skill only when requested or the project already uses that convention, following the host's discovered skill directory. Do not install a global router or add dependencies just to wrap a working command.

Keep the recipe small and runnable by a fresh session. It must state:

| Part | Required detail |
|---|---|
| Target | App/surface, supported environment, build identity, prerequisites, permissions and unavailable boundaries |
| Launch | Exact working directory and commands, config variable names without secrets, isolated ports/data, migrations/seeds/auth, and a bounded usable-readiness check |
| Doctor | Read-only checks for the intended build, owned instance, readiness and auth; what a failure means |
| Journeys | Only relevant user paths: prerequisite state, real actions/selectors/commands, expected visible result and durable side effects; link existing requirement/test IDs |
| Evidence | Commands/results and action-plus-result artifacts, with a durable path separate from scratch data; redaction requirements |
| Cleanup | Exact owned resource identifiers, teardown on both failure and success, evidence-survival check, remaining-resource report |

Use stable semantic selectors and existing drivers. Do not create one file per feature unless the journeys are large enough to need separate references. Keep broad feature coverage in the existing test plan; a recipe that proves one journey must not claim all features passed.

Run the instructions end to end for one representative journey, including cleanup and checking the retained evidence. Check the failure cleanup path when adding lifecycle helpers. Helpers must have documented invocations and preserve failing exit statuses. If prerequisites prevent execution, mark the recipe **unverified** with the exact blocked step; never fill gaps with invented commands or silently repair unrelated startup defects.

Update only when app commands, journeys, or demonstrated failures make the recipe stale. Do not add standing rules or schedules from a single unexplained incident.
