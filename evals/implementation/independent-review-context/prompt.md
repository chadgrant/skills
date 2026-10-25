---
description: An independent review receives raw artifacts rather than the implementation narrative.
tags: [regression, implementation]
max_turns: 12
allowed_tools: [Skill, Read]
---

Use the implementation delegation guidance to plan a review handoff, without spawning agents. The implementation parent has a long narrative asserting that its retry implementation is correct. The host supports both inherited and fresh-context agents. The user requested an independent review. Available raw inputs: REQ-017, diff base..head, tests/retry.test.ts, and .delivery/verification/retry/results.txt. What context should the reviewer receive? Also describe the fallback if the host cannot provide fresh context.
