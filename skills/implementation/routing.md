# Task routing

Read when assigning tiers or selecting a non-fork model. Use [delegation.md](delegation.md) to prefer Forks when compatible.

Rate on the **hardest aspect**, not the average.

| Difficulty | Signal | Tier | Plugin default |
|---|---|---|---|
| Easy | mechanical, single-file, pattern-following, reversible | small | Haiku |
| Medium | multi-file, some design judgment, integrates 2–3 components | mid | Opus |
| Hard | security / money / auth / data-integrity / tenancy; concurrency; novel algorithm; many tasks depend on it; high blast radius | top | Opus, or Fable where the user approved it below |

- These are plugin defaults, not a live price ranking. Honor user model choices and available models. Use unversioned aliases unless reproducing a run. Forks inherit the parent model; use a non-fork agent when the required tier/model differs.
- Security / money / auth / data-integrity is **Hard regardless of size**.
- **`observe`** marks the true spine only: key storage, credential or token minting, authn/authz decisions, money movement, tenancy isolation. "Hard" or "auth-adjacent" does not qualify. It adds a security reviewer at the milestone gate; it does not add a review per task.

## Fable authorization

Use Opus by default; use Fable only with recorded user authorization. Ask with the choices below and record the answer in the plan header and `STATUS.md`; it holds for the whole run, including later sessions.

| Answer | Top tier means |
|---|---|
| No Fable (the default when the user doesn't answer or can't be asked) | Opus for everything rated Hard, including `observe` tasks and their reviewers |
| Fable for `observe` only | Fable for `observe` tasks and their security reviewer; Opus for other Hard work |
| Fable for all Hard | Fable wherever the routing table says top tier |

Never dispatch a Fable agent without a recorded yes. An escalation that would reach Fable without one stops and asks.
