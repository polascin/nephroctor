# Handoff: nephroctor-loop-iter-28

## Metadata

- Generated At: 2026-11-06T04:42:44+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: 51499e6 (51499e63b1946fe6ff7823bd21467eaa9a048498)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-042015-nephroctor-loop-iter-27.md`

## Original Goal

Loop iteration 28 after AGENT_LOOP_TICK_nephroctor (one-shot wake): one coherent real improvement; prefer functional/security/a11y bug; skip `.sk`/`.eu` panel; no more legal redirects; rate-limit aware `gh`; commit/push/Deploy/production curl browser UA; complete handoff.

## Current State

Iter 28 shipped Clarity modal scroll lock and is live. Working tree clean after docs handoff commit (or clean before that commit). `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker; skipped).

## Completed This Session

- Audits green; no higher-severity inbound legal URL issue.
- Found medium a11y bug: first-run dialog focus on container (`tabIndex=-1`) still allowed Space/PageDown/arrows to scroll the page behind the modal despite `inert` siblings.
- `setScrollLock` on `html`/`body` + CSS `overscroll-behavior: contain`; tests; cache-bust `?v=2b163b588ee0`; pristupnost 1.9; `.audit.md` / state updated.
- Commit required `C:\Python314\Scripts` on PATH so global GitGuardian `ggshield` hook can run (do not change `core.hooksPath`).

## Validated

- Deploy `51499e6` https://github.com/polascin/nephroctor/actions/runs/42157205770: **success**. Smoke check **success**. Report security headers **success**.
- Production curl (browser UA):
  - `/` **200** + CSP / X-Frame-Options DENY / Permissions-Policy browsing-topics / HSTS; HTML references `clarity-consent.js?v=2b163b588ee0`
  - `/assets/clarity-consent.js?v=2b163b588ee0` **200**, contains `setScrollLock` and `overflow = "hidden"`
  - `/assets/clarity-consent.css?v=2b163b588ee0` **200**, contains `overscroll-behavior: contain`
  - `/legal/pristupnost.html` shows version **1.9**
  - `/manifest.webmanifest` **200**; `/apple-touch-icon.png` **200** (prior iters still good)

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Prefer a real functional/security/a11y bug next (Clarity modal scroll lock done).
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship modal scroll lock rather than another root asset probe path.
- Reason: Job preferred real a11y/functional bugs; container-focus scroll-behind is modal UX / WCAG 2.4.3 adjacent and higher severity than further favicon/manifest copies; legal redirects and `.sk`/`.eu` panel skipped per brief.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel**.
- Local deploy path for nephroctor.com still unavailable on this machine.
- Global `core.hooksPath` GitGuardian wrapper needs `ggshield` on PATH (`C:\Python314\Scripts`); local `.git/hooks/pre-commit` (pre-commit.com) already passes.
- Actions WAF may rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `assets/clarity-consent.js`, `assets/clarity-consent.css`
- `.audit/test_clarity.cjs`
- `index.html`, `legal/cookies.html`, `legal/ochrana-osobnych-udajov.html`, `legal/pristupnost.html`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 51499e6 fix(a11y): lock page scroll while Clarity consent dialog is open
- c6c4961 docs(handoff): complete nephroctor loop iter-27 after root manifest [skip ci]
- 8494589 fix(assets): serve root manifest.webmanifest for common probes

## Modified Files

- Clarity JS/CSS + tests + HTML cache-bust + pristupnost 1.9 + audit/state
- this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-042015-nephroctor-loop-iter-27.md`
- `state/TODO.md`

## Next Command

```text
git pull origin main
# Prefer real functional/security/a11y bug; Clarity modal scroll lock done
# User: WebSupport panel → nephroctor.sk and nephroctor.eu as domain aliases of nephroctor.com (not HTTP redirect)
powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1
```
