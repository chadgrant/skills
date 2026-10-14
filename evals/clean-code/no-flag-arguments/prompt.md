---
description: A dry-run requirement must become two functions or a separate mode object, never a boolean flag parameter; magic numbers get names.
tags: [smoke, clean-code]
max_turns: 8
allowed_tools: [Skill, Read]
---

Write a TypeScript function that applies a 15% gold-member discount to an order total and saves the new total with `orderRepository.save(order)`. It also needs a dry-run mode that computes the total without saving. Reply with just the code.
