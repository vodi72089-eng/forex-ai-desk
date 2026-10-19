---
name: ui-ux-pro-max
description: Use when choosing or extending a product design system, screen layout, component patterns, or interaction flow; create evidence-based, consistent UI decisions for this application.
---

# UI/UX Pro Max Skill

## Goal
Make the product easier to understand and operate, not merely more decorative. Use this skill for new screens, workflow changes, information architecture, visual hierarchy, and design-system decisions.

## Start with user intent
For the screen or feature, identify:
- The user's main goal.
- The most frequent action.
- The information needed before that action.
- The consequence of an error.
- What should happen when data is absent, invalid, delayed, or unavailable.

## Design-system procedure
1. Inspect the current project and reuse its existing patterns before introducing new ones.
2. Define tokens for background, surface, primary text, secondary text, border, primary action, success, warning, and error.
3. Define a compact spacing scale and a small type scale; apply them consistently.
4. Choose controls that match the task: buttons for actions, labels for state, tables for comparable records, and dialogs for confirmation.
5. Make the primary action prominent without making secondary actions invisible.
6. Keep navigation labels predictable and group related operations.
7. For numeric or financial information, include units, sign, timeframe, and source/context where relevant. Do not show false precision.
8. Validate keyboard operation, focus visibility, contrast, readable labels, and error recovery.
9. Check that the interface remains understandable when text is long, results are empty, or a provider is disconnected.

## Forex AI Desk requirements
- Clearly distinguish PDF parsing, heuristic checks, AI-generated commentary, and MetaTrader 5 connection status.
- Display whether a result is a suggestion, a detected rule, or a verified system state.
- Do not represent AI output as guaranteed financial advice or a live order.
- Make simulation/read-only status visible where relevant.
- Explain errors in plain French and offer a useful next step.
- Keep API keys and secrets out of the UI logs and repository.
- Use French interface language consistently unless a localization task requests otherwise.

## Avoid
- Adding a new UI framework or large dependency without a concrete need.
- Redesigning unrelated screens during a focused feature change.
- Using color alone for status.
- Hiding errors, silently swallowing failures, or displaying fake demo data as live data.
- Adding charts unless they answer a specific user question.

## Deliverable
For substantial UI changes, report the design decisions briefly, list changed files, and state which visual and functional checks were actually performed.
