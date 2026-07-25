---
doc: wireframes
title: <Feature / Project name>
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# Wireframes — <Feature / Project name>

> **Lo-fi wireframes & interaction spec** · **Related:** [PRD](./prd.md) · [User flows](./user-flows.md) · [Style guide](../../design-system/style-guide.md)
>
> **Fidelity:** lo-fi only — layout and priority, not final visual design. Visual language lives in the [style guide](../../design-system/style-guide.md); the UI is **built with the Impeccable skill** (see the plan's Global constraints). Don't push these past lo-fi.

## 1. Screens
<One wireframe per screen. Every screen derives from a step in a [user flow](./user-flows.md) — don't invent screens with no flow. Author each as an `.excalidraw` scene (clone `templates/diagram.excalidraw`) and label the boxes.>

### SCR-001: <screen name>
- **Satisfies:** REQ-…  ·  **Appears in:** FLOW-… *(an orphan screen with no flow is unreachable UI)*
- **Primary action:** <the one thing this screen is for.>
- **Key elements:** <the components on the screen; reference `CMP-` from the style guide, and flag any net-new component the style guide doesn't yet have.>

**Wireframe** (lo-fi; clone `templates/diagram.excalidraw`):
![wireframe: <name>](diagrams/wireframe-<name>.excalidraw.svg)
> *In plain terms: <what this screen shows and what the user does here>.*

#### Interaction spec *(optional — include for any interactive screen)*
<What each element does over time and in every state. This is what stops "what happens when it's slow / empty / clicked twice" from becoming bug tickets.>

| Aspect | Behavior |
|---|---|
| **States** | default · hover · focus · active · disabled · **loading · empty · error · success** |
| **Triggers → responses** | <e.g. "submit with invalid email → inline error under field, button stays disabled"> |
| **Transitions** | <what moves/animates and roughly how fast — not easing curves (that's hi-fi)> |
| **Async** | <loading/skeleton, optimistic update, retry, timeout> |
| **Keyboard / focus** | <tab order, enter-to-submit, escape — doubles as a11y annotation> |

> Every interactive screen must cover empty / error / loading (ties to the PRD's edge cases & states). No placeholders.
