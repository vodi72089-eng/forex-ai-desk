---
name: web-design-guidelines
description: Use as a final review checklist for user interfaces, including usability, accessibility, consistency, feedback, and performance; apply the same principles to desktop UI when relevant.
---

# Interface Guidelines Review Skill

## Review mode
Review the actual changed UI and related code. Prefer concrete findings with file names, line numbers when available, severity, user impact, and a proposed fix. Do not invent problems without evidence. Separate confirmed defects from suggestions.

## Checklist

### Usability and hierarchy
- Is the screen's purpose clear immediately?
- Is the primary action obvious and named with a verb?
- Are related controls grouped and consistently aligned?
- Are labels specific and free from unexplained jargon?
- Can users understand what will happen before they trigger an action?

### Feedback and states
- Do actions provide visible success or failure feedback?
- Are long-running tasks marked as loading, and can the user tell whether the app is still responsive?
- Are empty states helpful rather than blank?
- Do error messages explain the problem and the next safe step?
- Are unavailable actions disabled with a clear reason where practical?

### Accessibility
- Text is readable and contrast is sufficient.
- Controls have descriptive names and do not rely on icons alone.
- Keyboard navigation and visible focus are supported where the toolkit allows.
- Important status is communicated through text as well as color.
- Focus order follows the task sequence.
- The interface remains usable without relying on hover.

### Layout and consistency
- No clipped text, overlapping widgets, accidental horizontal overflow, or inconsistent spacing.
- Shared controls use the same labels, sizing, and state conventions.
- Long PDF paths, AI responses, and error messages can be viewed without breaking the layout.
- The smallest supported window size remains usable.

### Trust and financial safety
- Read-only, simulation, and live states are unmistakable.
- No button or status implies an order was sent unless the application confirms it.
- AI-generated analysis is clearly distinguished from verified market/system data.
- Warnings are proportionate and appear before consequential actions.
- Secrets, API keys, and sensitive local paths are not exposed in logs or error dialogs.

### Performance and resilience
- Network/API operations do not block the UI event loop.
- Failures and timeouts are handled without crashing the app.
- Update downloads are verified before installation.
- Existing tests cover critical logic where practical.

## Review output
Return findings ordered by severity:
- **Critical** — security, data loss, or dangerous misrepresentation.
- **High** — core workflow broken or inaccessible.
- **Medium** — substantial usability or layout issue.
- **Low** — polish or consistency improvement.

For each finding, give evidence, impact, and a focused correction. If no issues are found, say what was checked and note any checks that could not be performed. Do not claim a visual test was run unless the UI was actually launched and inspected.
