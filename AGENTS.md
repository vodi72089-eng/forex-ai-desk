# Agent instructions — Forex AI Desk

Before changing code:
1. Inspect the existing implementation and tests; do not assume files or behavior exist.
2. State the intended approach briefly before a broad refactor.
3. Preserve working behavior and keep changes focused.
4. Never invent API contracts, trading results, successful builds, or test results.
5. Keep trading functionality read-only/simulation unless a separately approved, tested feature explicitly authorizes otherwise.
6. Never commit API keys, tokens, passwords, or other secrets.

## UI and design work
For new UI, redesigns, or substantial interface changes, read and follow:
- `.agents/skills/frontend-design/SKILL.md` — visual direction and implementation.
- `.agents/skills/ui-ux-pro-max/SKILL.md` — user flow, design system, and product usability.
- `.agents/skills/web-design-guidelines/SKILL.md` — final UX/accessibility/trust review.

Use the skills as workflows, not as permission to rewrite unrelated parts of the application. Forex AI Desk currently uses Python/Tkinter; adapt web-oriented principles to the actual stack and do not introduce a web framework unless requested.

## Before finishing
- Run relevant unit tests and report the actual result.
- For UI changes, inspect the rendered app when tooling permits; otherwise state that visual verification was not performed.
- List changed files and known limitations.
