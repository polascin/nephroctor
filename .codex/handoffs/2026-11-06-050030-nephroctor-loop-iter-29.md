# Handoff: nephroctor-loop-iter-29

## Metadata

- Generated At: 2026-11-06T05:00:30+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: bce92c3 (bce92c36149c2b99c27cdb78856da4653630e73f)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-044244-nephroctor-loop-iter-28.md`

## Original Goal

Loop iteration 29 after AGENT_LOOP_TICK_nephroctor (one-shot wake): one coherent real improvement; prefer functional/security/a11y bug; skip `.sk`/`.eu` panel; no more legal redirects; rate-limit aware `gh`; commit/push/Deploy/production curl browser UA; complete handoff.

## Current State

Iter 29 shipped Clarity dialog self-scroll (companion fix to iter-28 page scroll lock) and is live. Working tree clean after docs handoff commit (or clean before that commit). `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker; skipped).

## Completed This Session

- Audits green; no higher-severity inbound legal URL issue.
- Found medium a11y regression: after document scroll lock, dialog `max-height`/`overflow: auto` applied only under `max-width: 450px`, so short desktop viewports could hide Allow/Decline with no way to reach them.
- Base-rule self-scroll (`max-height: calc(100vh/100dvh - 2rem)` + `overflow: auto`); phone media query keeps layout-only tweaks; tests; cache-bust `?v=78331b7675cf`; pristupnost 2.0; `.audit.md` / state updated.
- Commit required `C:\Python314\Scripts` on PATH so global GitGuardian `ggshield` hook can run (do not change `core.hooksPath`).

## Validated

- Deploy `bce92c3` https://github.com/polascin/nephroctor/actions/runs/42158860197: **success**. Smoke check **success**. Report security headers **success**.
- Production curl (browser UA):
  - `/` **200** + CSP / X-Frame-Options DENY / Permissions-Policy browsing-topics / HSTS; HTML references `clarity-consent.js?v=78331b7675cf`
  - `/assets/clarity-consent.css?v=78331b7675cf` **200**, contains `max-height: calc(100vh - 2rem)`, `max-height: calc(100dvh - 2rem)`, `overflow: auto`, `overscroll-behavior: contain`
  - `/legal/pristupnost.html` shows version **2.0** and self-scroll wording
  - Prior assets still good (manifest / apple-touch not re-broken)

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Prefer a real functional/security/a11y bug next (Clarity dialog self-scroll done).
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship dialog self-scroll rather than another root asset probe (browserconfig / favicon.svg / android-chrome 404s remain optional low).
- Reason: Job preferred real a11y/functional bugs; unreachable consent controls after scroll lock is a regression of medium severity and WCAG 2.1.1 / 1.4.10 adjacent; legal redirects and `.sk`/`.eu` panel skipped per brief.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel**.
- Local deploy path for nephroctor.com still unavailable on this machine.
- Global `core.hooksPath` GitGuardian wrapper needs `ggshield` on PATH (`C:\Python314\Scripts`); local `.git/hooks/pre-commit` (pre-commit.com) already passes.
- Actions WAF may rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `assets/clarity-consent.css`, `assets/clarity-consent.js`
- `.audit/test_clarity.cjs`
- `index.html`, `legal/cookies.html`, `legal/ochrana-osobnych-udajov.html`, `legal/pristupnost.html`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- bce92c3 fix(a11y): keep Clarity consent dialog scrollable after page scroll lock
- c9b083a docs(handoff): complete nephroctor loop iter-28 after Clarity scroll lock [skip ci]
- 51499e6 fix(a11y): lock page scroll while Clarity consent dialog is open

## Modified Files

- Clarity CSS + tests + HTML cache-bust + pristupnost 2.0 + audit/state
- this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-044244-nephroctor-loop-iter-28.md`
- `state/TODO.md`

## Next Command

```text
git pull origin main
# Prefer real functional/security/a11y bug; Clarity dialog self-scroll done
# User: WebSupport panel → nephroctor.sk and nephroctor.eu as domain aliases of nephroctor.com (not HTTP redirect)
powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1
```
