# Handoff: nephroctor-loop-iter-25

## Metadata

- Generated At: 2026-11-06T03:49:57+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `9064941`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-032804-nephroctor-loop-iter-24.md`

## Original Goal

Loop iteration 25 after AGENT_LOOP_TICK_nephroctor #24: audits/code review; one coherent real improvement (prefer functional/security/a11y/i18n/perf; no more legal URL redirects unless broken inbound); skip `.sk`/`.eu` panel; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 25 complete. Working tree clean on `origin/main` after docs handoff. Fix `9064941` is live: Clarity consent Tab/Shift+Tab trap treats dialog-container focus and escaped focus as edges, so first-run Shift+Tab no longer leaves the modal. Cache-bust `?v=e1bbfa3bf0ab`. Accessibility statement 1.8. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped).

## Completed This Session

- Full `.audit/*` + `test_clarity.cjs` green before the fix; no higher-severity unrelated bug surfaced.
- Found medium a11y bug: first-run focus on dialog root (`tabIndex=-1`) sat outside the previous first/last control wrap.
- `assets/clarity-consent.js`: `onKeyDown` wraps when active is banner, first/last, or outside `banner.contains`.
- `.audit/test_clarity.cjs`: container + escaped-focus trap asserts; mock `querySelectorAll` fixed for compound focusable selector.
- HTML `?v=e1bbfa3bf0ab` on index / cookies / privacy; `legal/pristupnost.html` 1.8 (SK+EN).
- Updated `.audit.md`, `state/SESSION.md`, `state/TODO.md`.
- Noted low optional follow-up: root `/apple-touch-icon.png` **404** (link tag already points at `/assets/…`; same pattern as root `favicon.ico`).

## Validated

- Deploy `9064941` https://github.com/polascin/nephroctor/actions/runs/42151628402: **success**. Smoke check **success**. Report security headers **success**.
- Production curl (browser UA):
  - `/` **200**; HTML references `clarity-consent.js?v=e1bbfa3bf0ab`
  - `/assets/clarity-consent.js?v=e1bbfa3bf0ab` **200**, contains trap comments + `!banner.contains(active)`
  - `/legal/pristupnost.html` **200**, `verzia 1.8` / `version 1.8`, Tab-trap wording
  - CSP present; `Permissions-Policy` includes `browsing-topics=()`; `X-Frame-Options: DENY`

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Manual keyboard confirmation in a real browser (logic covered by unit test).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Prefer a real functional/security/a11y bug next (Clarity Tab-trap container edge is done). Optional low: root apple-touch-icon copy.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship Tab-trap container/escape fix (not another legal URL alias; not apple-touch root copy).
- Reason: Job preferred real a11y/functional bugs; Shift+Tab leaving a modal is WCAG 2.1.2 / 2.4.3 adjacent and higher severity than a redundant root icon when `<link rel="apple-touch-icon">` already works.
- Decision: Treat dialog root focus and any non-contained activeElement as trap edges.
- Reason: First-run intentionally focuses the labelled dialog for AT announcement; the control list alone cannot wrap that node.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF may still rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `assets/clarity-consent.js`
- `.audit/test_clarity.cjs`
- `index.html`, `legal/cookies.html`, `legal/ochrana-osobnych-udajov.html` (`?v=`)
- `legal/pristupnost.html`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 9064941 fix(a11y): keep Clarity Tab trap on dialog container focus
- 4abc958 docs(handoff): complete nephroctor loop iter-24 after Clarity inert fix [skip ci]
- b98fa42 fix(a11y): exclude live status regions from Clarity inert backdrop

## Modified Files

- `assets/clarity-consent.js`, `.audit/test_clarity.cjs`
- HTML cache-bust + pristupnost 1.8
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-032804-nephroctor-loop-iter-24.md`
- `DEPLOY.md` (domain alias section)
- `state/TODO.md`

## Grok bots

- Status: optional; not invoked this iteration.

## Next Command

```text
git pull origin main
# User: WebSupport panel → nephroctor.sk and nephroctor.eu as domain aliases of nephroctor.com (not HTTP redirect)
powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1
# Expect: https://nephroctor.sk/privacy → 301 → https://nephroctor.com/legal/ochrana-osobnych-udajov.html
# Prefer real functional/security/a11y bug next; Clarity Tab-trap container edge is done
# Optional low: copy assets/apple-touch-icon.png to repo root (like favicon.ico) + deploy + check_assets assert
```
