# Handoff: nephroctor-loop-iter-10

## Metadata

- Generated At: 2026-11-05T22:46:51+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `dd948101f1acca41dfd59a84a1c73bcddf82bb0f`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-222531-nephroctor-loop-iter-9.md`

## Original Goal

Loop iteration 10 after AGENT_LOOP_TICK_nephroctor #9: prefer non-Clarity improvement; git/handoffs; optional alias verify once; one coherent fix with commit/push/Deploy verify + production curl; complete handoff.

## Current State

Iteration 10 complete. Working tree clean on `origin/main` after docs handoff. Fix `dd94810` is live: `/accessibility` and `/pristupnost` 301 to accessibility statement; Permissions-Policy includes `browsing-topics=()`; sitemap `lastmod` refreshed for home/privacy/cookies. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged).

## Completed This Session

- Verified clean tree at `85068f6` (iter-9 handoff); `tools/verify-domain-aliases.ps1` still 4× FAIL.
- In-repo improvement (non-Clarity):
  - `.htaccess`: `/accessibility` + `/pristupnost` RewriteRule (alias hosts) and RedirectMatch (canonical); Permissions-Policy adds `browsing-topics=()`.
  - `sitemap.xml`: `lastmod` 2026-11-05 for `/`, privacy, cookies (unchanged legal pages keep 2026-08-16).
  - `DEPLOY.md`, `.audit.md`, `state/SESSION.md`, `state/TODO.md` updated.
- Skipped Beh #15 full doaudit per job instructions.

## Validated

- Local: `check_format.py`, `check_assets.py` PASS.
- `tools/verify-domain-aliases.ps1`: `.com/privacy` OK; four `.sk`/`.eu` FAIL (expected).
- Deploy `dd94810` https://github.com/polascin/nephroctor/actions/runs/42113944516: **success**. Smoke check **success**; Report security headers **success** (WAF 429 retries during smoke, then recovered).
- Production curl (browser UA):
  - `/` 200; CSP/HSTS/nosniff/DENY; `Permissions-Policy` includes `browsing-topics=()`; `Cache-Control: no-cache, must-revalidate`
  - `/accessibility` 301 → `/legal/pristupnost.html`; `/pristupnost` same; `?lang=en` preserved on Location
  - `/sitemap.xml` 200 with `lastmod` 2026-11-05 on home/privacy/cookies
  - Alias verify still **302** path-drop on `.sk`/`.eu` (panel open)

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Prefer SEO/legal URL discoverability over further Clarity a11y polish.
- Reason: Job asked for non-Clarity if possible; `/accessibility` was a real 404; mirrors existing `/privacy`/`/terms`/`/cookies` pattern.
- Decision: Skip Beh #15 full doaudit.
- Reason: Job instructions.
- Decision: Keep `lastmod` of untouched legal pages at 2026-08-16.
- Reason: Only bump dates for files actually changed since August.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF still rate-limits Smoke (429 with retry); do not treat as payload failure when retries succeed.

## Critical Files

- `.htaccess`, `sitemap.xml`, `DEPLOY.md`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- dd94810 fix(seo): add accessibility URL shortcuts and refresh sitemap lastmod
- 85068f6 docs(handoff): complete nephroctor loop iter-9 after live-region a11y deploy [skip ci]
- ca2bcd9 fix(a11y): announce Clarity consent language changes via live region

## Modified Files

- `.htaccess`, `sitemap.xml`, `DEPLOY.md`
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-222531-nephroctor-loop-iter-9.md`
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
# Optional next in-repo: e.g. /health-notice shortcut, or stale lastmod spot-check after legal edits
```
