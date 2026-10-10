---
doc: style-guide
title: <Org / Product> Design System
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# Style guide — <Org / Product> Design System

> **Cross-project design system** · **Related:** feature [wireframes](../docs/requirements/wireframes.md) & [user flows](../docs/requirements/user-flows.md) reference this doc.
>
> **This is a cross-project, long-lived asset — reference it, don't regenerate it.** It lives in `design-system/`, not a feature's `docs/requirements/`. A feature links here and records only the **net-new** `CMP-`/`TOK-` it introduces; it does not re-copy the system.
>
> **Implementation:** UI is built with the **Impeccable skill** (`github.com/pbakaus/impeccable`), which extends Anthropic's `frontend-design` skill with an anti-slop design vocabulary. This doc is the source of truth for tokens and components; Impeccable is how they get built.

## 1. Brand & voice
<Personality in a line or two; the tone rules the UI copy follows. Ref the PRD's users/personas.>

## 2. Design tokens
<The atoms. Prefer OKLCH for color (perceptual uniformity, accessible contrast). Every token gets a stable `TOK-` id so components and code reference it, not raw values.>

| ID | Token | Value | Used for |
|---|---|---|---|
| TOK-001 | `color.bg.default` | `oklch(…)` | page background |
| TOK-002 | `space.4` | `1rem` | default gutter |
| TOK-003 | `font.display` | `<family>` | headings |

## 3. Components
<The molecules. One `CMP-` per reusable component, its states, and the tokens it consumes. A feature's wireframes reference these; anything a feature needs that isn't here is flagged net-new and added.>

| ID | Component | States | Tokens used | Notes |
|---|---|---|---|---|
| CMP-001 | Button | default/hover/focus/active/disabled/loading | TOK-001, TOK-003 | primary / secondary variants |

## 4. Usage & layout
<Grid, spacing scale, breakpoints, do/don't rules. How the components compose into screens.>

## 5. Accessibility
<WCAG conformance target; contrast minimums (verifiable against the OKLCH tokens); focus-visible, motion-reduction, and keyboard rules every component must meet. Ref the PRD's a11y `NFR-`.>
