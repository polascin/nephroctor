# Handoff: nephroctor-loop-iter-24

## Metadata

- Generated At: 2026-11-06T03:28:04+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `b98fa42`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-030329-nephroctor-loop-iter-23.md`

## Original Goal

Loop iteration 24 after AGENT_LOOP_TICK_nephroctor #23: audits/code review; one coherent real improvement (prefer functional/security/a11y/i18n/perf; no more legal URL redirects unless broken inbound); skip `.sk`/`.eu` panel; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 24 complete. Working tree clean on `origin/main` after docs handoff. Fix `b98fa42` is live: Clarity consent `setBackgroundInert` skips `role="status"` / `aria-live` regions so polite announces stay available while the dialog is open. Cache-bust `?v=62105992024e`. Accessibility statement 1.7. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped).

## Completed This Session

- Full `.audit/*` + `test_clarity.cjs` green before the fix; no higher-severity unrelated bug surfaced.
- Found medium a11y bug: inert backdrop silenced Clarity settings-label and page-level lang live regions during the modal.
- `assets/clarity-consent.js`: `isLiveStatusRegion` exclusion in `setBackgroundInert`.
- `.audit/test_clarity.cjs`: non-inert status + inert page main asserts; private-path checks updated for seeded body children.
- HTML `?v=62105992024e` on index / cookies / privacy; `legal/pristupnost.html` 1.7 (SK+EN).
- Updated `.audit.md`, `state/SESSION.md`, `state/TODO.md`.

## Validated

- Deploy `b98fa42` https://github.com/polascin/nephroctor/actions/runs/42149341229: **success**. Smoke check **success**. Report security headers **success**.
- Production curl (browser UA):
  - `/` **200**; HTML references `clarity-consent.js?v=62105992024e`
  - `/assets/clarity-consent.js?v=62105992024e` **200**, contains `isLiveStatusRegion`
  - `/legal/pristupnost.html` **200**, `verzia 1.7`
  - CSP present; `Permissions-Policy` includes `browsing-topics=()`
- `gh` core rate limit: ~4171 remaining before watch; ~3920 after.

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Screen-reader manual confirmation of live announces during open Clarity dialog (logic covered by unit test).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Prefer a real functional/security/a11y bug next (Clarity inert/live-region clash is done).
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship inert/live-region fix (not another legal URL alias).
- Reason: Job preferred real a11y/functional bugs; no broken inbound legal URL found; inert silencing status regions is WCAG 4.1.3 adjacent and regressions the earlier live-announce work.
- Decision: Exclude by `role=status|alert` and non-off `aria-live`, not by Clarity-only class.
- Reason: Page-level lang live regions on home/legal are also body children and must keep announcing (e.g. cross-tab lang while dialog open).

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

- b98fa42 fix(a11y): exclude live status regions from Clarity inert backdrop
- 972cb5e docs(handoff): complete nephroctor loop iter-23 after impressum aliases [skip ci]
- ae4b0e6 fix(seo): add impressum 301 aliases to legal notice

## Modified Files

- `assets/clarity-consent.js`, `.audit/test_clarity.cjs`
- HTML cache-bust + pristupnost 1.7
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-030329-nephroctor-loop-iter-23.md`
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
# Prefer real functional/security/a11y bug next; Clarity inert vs aria-live is done
```
