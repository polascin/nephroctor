# Handoff: nephroctor-loop-iter-4

## Metadata

- Generated At: 2026-11-05T21:06:00+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: 6e87685 (iter-5 `?v=` bust on top of iter-4 `eb74479` + `8b12f39`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-201442-nephroctor-loop-iter-3.md`

## Original Goal

Loop iteration 4 after AGENT_LOOP_TICK_nephroctor #3: verify iter-3 state; finish Clarity CSP if incomplete, else next audit bug (long cache on clarity-consent.css without bust); commit/push/verify Deploy rate-limit aware; complete handoff.

## Current State

Iteration 4 complete; a parallel agent also landed iter-5 `6e87685` (HTML `?v=` + smoke bust) while this handoff was written. Iter 3 left clean tree at `0e3f3fc` with Clarity CSP already verified (0 violations). Iter 4 fixed unhashed CSS/JS revalidation and Smoke markers; first Deploy of `eb74479` failed Smoke (gzip and/or OpenResty edge still serving bare URLs with old TTL); `8b12f39` fixed identity encoding and succeeded.

Production after `8b12f39` (browser UA, identity encoding): `/` 200 with CSP/HSTS/nosniff/DENY; Clarity JS/CSS `Cache-Control: no-cache, must-revalidate`; JS has `aria-modal` + `scriptUrl`; CSS has `color-card`. Re-verify after `6e87685` Deploy finishes.

## Completed This Session

- Confirmed iter-3 handoff complete; no Clarity CSP WIP left (0 violations; CSP unchanged).
- Root cause of stale consent UI after green Deploy: unhashed CSS/JS cached one day; HEAD could also look stale while GET caught up.
- `.htaccess`: CSS/JS Expires 0 + `Cache-Control: no-cache, must-revalidate` (with HTML); fonts/images unchanged.
- `clarity-consent.js`: propagate `script.src` query string onto dynamically loaded `clarity-consent.css`.
- `deploy.yml` Smoke: body markers `aria-modal` / `color-card`; must use `Accept-Encoding: identity` (gzip `-o` made first marker check false-fail).
- `test_clarity.cjs`: asserts CSS URL inherits `?v=`.
- Documented in `.audit.md`, `state/SESSION.md`, `state/TODO.md`.

## Validated

- Local: `test_clarity.cjs`, `check_format.py`, `check_assets.py` PASS.
- Deploy `eb74479` run https://github.com/polascin/nephroctor/actions/runs/42095934437: SFTP OK; Smoke **failed** (gzip body grep false negative). Payload was already correct on origin.
- Deploy `8b12f39` run https://github.com/polascin/nephroctor/actions/runs/42098123693: **success**. Smoke: JS marker OK; CSS marker skipped after WAF 429 (warning, not fail). Report security headers warned (likely Actions IP 429); local curl confirms headers present.
- Deploy `6e87685` run https://github.com/polascin/nephroctor/actions/runs/42098466229: **success** (Smoke + Report security headers steps green; many WAF 429 warnings).
- Production curl (browser UA): `/` 200 + CSP/HSTS/nosniff/DENY; HTML references `clarity-consent.js?v=ec7132f34a`; versioned JS/CSS identity bodies have markers; `Cache-Control: no-cache, must-revalidate`.

## Not Yet Validated

- Visual dark-theme consent banner spot-check in a real browser after Allow.
- Clarity CSS marker under Actions IP when WAF is calm (skipped once due to 429).

## Remaining Work

- [ ] **Next priority:** WebSupport panel: `nephroctor.sk` / `.eu` domain alias with path-preserving redirects (today upstream 302 can drop path).
- [ ] Local SFTP deploy replacement (blocked: no verified hosting account for nephroctor.com).
- [ ] Clarity dashboard aggregate counters (informational).
- [ ] Optional: soften Actions WAF pressure (fewer smoke paths / longer cool-down) so security-header report and CSS marker are less often skipped.

## Decisions Made

- Decision: Revalidate unhashed CSS/JS via `no-cache, must-revalidate` instead of inventing a content-hash pipeline.
- Reason: Matches existing HTML policy; ETag still allows cheap 304; deploy becomes visible immediately.
- Decision: Propagate script query to CSS URL.
- Reason: If HTML later adds `?v=`, CSS stays in lockstep without a second hard-coded version.
- Decision: Fail Smoke on missing Clarity body markers (with identity encoding).
- Reason: Status-only 200 previously allowed a false sense that theme/a11y bytes were live.
- Decision: Skip Beh #15 full doaudit.
- Reason: Job instructions; no critical audit failure.

## Blockers / Open Questions

- Commits need `C:\Python314\Scripts` on PATH for global GitGuardian `ggshield`.
- Local deploy path for nephroctor.com still unavailable.
- GitHub Actions IPs often hit HTTP 429 from host WAF during Smoke; treat exhausted 429 as warning, verify prod from a non-Actions client.
- Prefer one `gh run list` then one `gh run watch`; avoid aggressive poll loops (API rate limit).

## Critical Files

- `.htaccess`
- `assets/clarity-consent.js`
- `.github/workflows/deploy.yml`
- `.audit/test_clarity.cjs`
- `.audit.md`
- `state/SESSION.md`
- `state/TODO.md`

## Recent Commits

- 6e87685 fix(cache): version Clarity assets to bypass edge TTL (parallel iter 5)
- 8b12f39 fix(ci): fetch Clarity smoke bodies as identity encoding
- eb74479 fix(cache): revalidate CSS/JS and smoke Clarity markers
- 0e3f3fc docs(handoff): record iter-3 Clarity CSP verify and deploy results
- 728af04 fix(ui): theme Clarity consent banner to site tokens

## Modified Files

- `.htaccess`
- `assets/clarity-consent.js`
- `.github/workflows/deploy.yml`
- `.audit/test_clarity.cjs`
- `.audit.md` / `state/*` (also touched by parallel `6e87685`)
- `index.html`, `legal/cookies.html`, `legal/ochrana-osobnych-udajov.html` (`?v=` from iter 5)
- this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-201442-nephroctor-loop-iter-3.md`
- `.htaccess` caching block
- `state/TODO.md`

## Grok bots

- Status: optional CLI at `C:\Users\polas\.grok\bin\grok.exe`; not required.
- This iteration: not invoked.

## Next Command

```text
git pull origin main; # WebSupport panel: set nephroctor.sk / .eu as aliases of nephroctor.com (path-preserving). Optionally browser dark-theme consent check after Allow.
```
