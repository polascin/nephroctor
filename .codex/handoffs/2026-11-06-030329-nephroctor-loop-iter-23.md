# Handoff: nephroctor-loop-iter-23

## Metadata

- Generated At: 2026-11-06T03:03:29+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `ae4b0e6d9e6d3ac88f5daee0f075e10c6e40a6d0`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-024652-nephroctor-loop-iter-22.md`

## Original Goal

Loop iteration 23 after AGENT_LOOP_TICK_nephroctor #22: implement `/impressum` + `/legal/impressum.html` 301 → `pravne-informacie.html` (prod 404; `/imprint` already works), or prefer a higher-severity functional bug if found; skip `.sk`/`.eu` panel; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 23 complete. Working tree clean on `origin/main` after docs handoff. Fix `ae4b0e6` is live: `/impressum` and `/legal/impressum.html` 301 to `/legal/pravne-informacie.html` with query preserved (DE discoverability parallel of `/imprint`). No higher-severity in-repo functional bug found this round. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped).

## Completed This Session

- Confirmed prod `/impressum` and `/legal/impressum.html` **404**; `/imprint` **301** OK.
- No higher-severity in-repo bug surfaced; shipped named impressum aliases.
- `.htaccess`: RewriteRule + RedirectMatch for `/impressum`, `/legal/impressum.html`.
- `legal/.htaccess`: fallback RewriteRule for `impressum.html`.
- Updated `DEPLOY.md`, `.audit.md`, `state/SESSION.md`, `state/TODO.md`.

## Validated

- Deploy `ae4b0e6` https://github.com/polascin/nephroctor/actions/runs/42146813511: **success**. Smoke check **success**. Report security headers **success**.
- Production curl (browser UA):
  - `/impressum` **301** → `https://nephroctor.com/legal/pravne-informacie.html`
  - `/impressum?lang=en` **301** → `.../pravne-informacie.html?lang=en`
  - `/legal/impressum.html` **301** → same target
  - `/legal/impressum.html?lang=en` **301** with `?lang=en` preserved
  - `/imprint` still **301** → same target
  - `/legal/pravne-informacie.html` **200**; `/` **200**; CSP + `Permissions-Policy` with `browsing-topics=()` present
- `gh` core rate limit healthy (~4694 remaining before push; ~4311 after watch).

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Prefer a real functional/security/a11y bug next (impressum/imprint/cookie-policy/accessibility legal aliases are done).
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship `/impressum` aliases (no higher-severity in-repo bug found).
- Reason: Job named them; prod was 404; same pattern as `/imprint` → `pravne-informacie.html`.
- Decision: Do not add impressum to Deploy Smoke redirect loop.
- Reason: Smoke keeps a small critical set to limit WAF pressure; local prod curl verified the new paths.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF may still rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `.htaccess`, `legal/.htaccess`
- `DEPLOY.md`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- ae4b0e6 fix(seo): add impressum 301 aliases to legal notice
- 0fb2aba docs(handoff): complete nephroctor loop iter-22 after skip-link deploy [skip ci]
- 6b3154e fix(a11y): make skip-link target focusable with tabindex -1

## Modified Files

- `.htaccess`, `legal/.htaccess`, `DEPLOY.md`
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-024652-nephroctor-loop-iter-22.md`
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
# Prefer real functional/security/a11y bug next; legal URL alias polish for impressum is done
```
