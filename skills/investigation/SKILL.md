---
name: investigation
description: Trace unfamiliar code, explain a design decision, or diagnose a reproducible failure before choosing a fix. Use for substantial how/why/root-cause questions; simple lookups and already-understood fixes need no investigation workflow.
---

# Investigation

Answer a bounded question with evidence. Start with the observed behavior, expected behavior, relevant revision/environment, and what remains unknown. Reuse existing maps and reports; do not inventory the whole repository.

## Choose the evidence

| Question | Start here | Stop when |
|---|---|---|
| How does it work? | Public entry point → transformations → state changes → observable result | The causal path and important failure branches are explained with locations |
| Why this design? | Current constraints, tests, comments, then targeted history (`git log -S`, blame, linked ADRs) | Evidence distinguishes recorded intent from your inference; missing rationale stays unknown |
| Why is it failing? | Smallest reproducer, actual error, relevant inputs and environment | One hypothesis explains the failure and a discriminating check supports it, or a precise blocker prevents confirmation |

Search narrowly, then expand along demonstrated dependencies. Use history, logs, issues, or external docs only when they can resolve the question. Do not read every evidence category by default. Redact secrets from captured diagnostics.

For debugging, rank plausible causes and test one discriminating hypothesis at a time. Record the command, result, and implication; reject a hypothesis when evidence contradicts it. After three failed hypotheses or a material scope change, reassess the map and report the missing evidence instead of repeating the same attempt.

Investigation does not imply permission to repair code, restart shared services, or mutate production data. Use isolated reproductions within the task's authorization. Delegated investigators keep the worker's file/service boundaries. For authorized substantial parallel discovery, prefer Forks with inherited context under [delegation.md](../implementation/delegation.md); a short trace needs no agents.

## Result and handoff

Lead with the answer and confidence, followed by the causal path or supported hypothesis, evidence locations, rejected alternatives that matter, and remaining unknowns. Distinguish observed behavior, inferred intent, and recommended change.

Return the result directly for a standalone question. For a delivery task, write to the supplied report path and return one line with the conclusion and path. Preserve the revision and existing requirement/task IDs; [handoffs.md](../implementation/handoffs.md) defines the shared evidence fields.

An authorized, understood fix continues through [implementation](../implementation/SKILL.md). A decision that changes requirements or contracts goes to [planning](../planning/SKILL.md). Use [verification](../verification/SKILL.md) when proving the result requires driving the running system. Do not turn an explanation-only request into implementation.
