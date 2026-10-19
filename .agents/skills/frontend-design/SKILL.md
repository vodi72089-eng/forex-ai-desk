---
name: frontend-design
description: Use before creating or redesigning any user interface to define a deliberate visual direction, layout, typography, color system, and interaction hierarchy instead of producing generic AI-looking UI.
---

# Frontend Design Skill

## Trigger
Use this skill before building or substantially changing a screen, dashboard, form, navigation, visual component, or user-facing workflow. For this repository, apply the principles to the Python/Tkinter desktop app unless the project has explicitly moved to another UI framework.

## Required workflow
1. **Inspect first.** Read the existing UI code, identify the framework, existing styles, user tasks, and constraints. Preserve working behavior unless the request explicitly changes it.
2. **Define the design direction before coding.** Write down the primary user, main task, information hierarchy, visual tone, spacing scale, color roles, typography, and the one distinctive visual decision that fits the product.
3. **Design around the task.** Forex AI Desk is an analytical desktop tool. Prioritize strategy-import status, analysis results, agent responses, connection state, and update status. Avoid decorative trading imagery that competes with data.
4. **Use a consistent system.** Define reusable colors, type sizes, spacing, borders, states, and component patterns. Do not introduce arbitrary values screen by screen.
5. **Implement all states.** Include default, hover/focus where supported, disabled, loading, empty, success, and error states. Long-running analysis must not make the interface appear frozen.
6. **Check responsive behavior.** Respect the minimum window size; prevent clipped controls, overlapping labels, and unreadable result areas at smaller sizes.
7. **Verify visually.** Run the app when possible, inspect the actual rendered UI, compare it with the intended hierarchy, and fix visible defects before finishing.

## Visual quality rules
- Avoid generic template styling, gratuitous gradients, random accent colors, excessive cards, and decorative charts without a user task.
- Use clear typography, disciplined spacing, restrained color, and strong contrast.
- Use color semantically: neutral for normal content, one primary accent for actions, and distinct success/warning/error colors.
- Prefer readable tables, aligned numeric values, clear section headings, and concise status labels for analytical information.
- Never rely on color alone to communicate a result.
- Keep destructive or consequential actions visually distinct and require confirmation when appropriate.
- Do not imply a strategy is profitable or safe merely because the interface looks polished.

## Project-specific visual direction
Use a professional, calm trading-workstation aesthetic: deep blue-charcoal surfaces, near-white primary text, muted blue-grey secondary text, and a restrained teal or amber accent. Keep this as guidance, not a reason to rewrite every screen. Preserve the existing brand unless the user asks for a rebrand.

## Completion checklist
- The requested workflow still works.
- The visual hierarchy makes the next action obvious.
- Text and results are readable at the minimum supported window size.
- Loading, empty, error, and success states are understandable.
- No unsupported claims about live trading, profitability, or execution were added.
- Tests pass, or unrun checks are explicitly reported.
