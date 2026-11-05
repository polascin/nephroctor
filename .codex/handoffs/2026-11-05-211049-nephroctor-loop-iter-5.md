# Handoff: nephroctor-loop-iter-5

## Metadata

- Generated At: 2026-11-05T21:10:49+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: 9b163b56286d3d786430f644b116fcbcad1e24d4 (docs after fix `6e87685549398a7f9366762dfe21474b519c724e`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-210600-nephroctor-loop-iter-4.md`

## Original Goal

Loop iteration 5 after AGENT_LOOP_TICK_nephroctor #4: verify whether iter-4 cache/smoke WIP landed; finish it if abandoned; otherwise one next priority; commit/push; verify Deploy (rate-limit aware); curl production; write complete handoff.

## Current State

Iteration 5 complete. Working tree clean on `origin/main`. Iter-4 code (`eb74479`) was already on main but Deploy Smoke had failed. Parallel follow-up `8b12f39` (identity encoding) and this iteration’s `6e87685` (versioned Clarity URLs) are live. Production serves theme/a11y Clarity assets via `?v=ec7132f34a` with `Cache-Control: no-cache, must-revalidate`.

## Completed This Session

- Verified fresh state: clean tree after `eb74479`; no iter-4 handoff yet at start; Deploy `42095934437` **failure**.
- Root cause of Smoke failure (not abandoned WIP): SFTP had uploaded new Clarity JS/CSS and `.htaccess`, but OpenResty edge kept bare `/assets/clarity-consent.js` and `.css` on prior `max-age=86400` bodies (old JS ~5606 B without `aria-modal`; old CSS without `color-card`). Origin with `?v=…` returned correct bytes and `no-cache`.
- `8b12f39` (parallel): `Accept-Encoding: identity` for Smoke body grep (avoids gzip false negative). Useful, but insufficient alone against edge TTL on bare URLs.
- This iteration (`6e87685`): HTML script tags on `index.html`, `legal/cookies.html`, `legal/ochrana-osobnych-udajov.html` use `clarity-consent.js?v=ec7132f34a` (SHA256 prefix of JS+CSS). JS already propagates query to CSS. Smoke requests `?v=$GITHUB_SHA` plus no-cache request headers.
- Updated `.audit.md`, `state/SESSION.md`, `state/TODO.md`.
- Skipped Beh #15 full doaudit per job instructions.
- Did not change WebSupport panel aliases (requires customer panel; unsafe/impossible from repo alone).

## Validated

- Local: `check_format.py`, `check_assets.py`, `test_clarity.cjs` PASS.
- Deploy `6e87685` https://github.com/polascin/nephroctor/actions/runs/42098466229: **success**. Smoke check **success**; Report security headers **success** (sparse `gh` polling only).
- Production curl (browser UA) after Deploy:
  - `/` 200; CSP/HSTS/nosniff/DENY; `Cache-Control: no-cache, must-revalidate`; HTML contains `clarity-consent.js?v=ec7132f34a`
  - `/assets/clarity-consent.js?v=ec7132f34a` 7585 B: `aria-modal`, `cssUrl.search`, `data-choice`; `no-cache, must-revalidate`
  - `/assets/clarity-consent.css?v=ec7132f34a` 1628 B: `color-card`; `no-cache, must-revalidate`
  - `https://nephroctor.sk/privacy` still upstream **302** to `https://nephroctor.com` (path dropped); panel alias still open.

## Not Yet Validated

- Visual dark-theme consent banner in a real browser after Allow (tokens present on versioned CSS).
- Bare Clarity URLs without `?v=` may remain on edge until prior TTL expires; browsers use versioned HTML refs.

## Remaining Work

- [ ] **Next priority:** WebSupport panel: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com` so path-preserving 301 in `.htaccess` can apply (today openresty 302 drops path).
- [ ] Local SFTP deploy replacement (blocked: no verified hosting account for nephroctor.com).
- [ ] Clarity dashboard aggregate counters (informational).
- [ ] Optional: reduce Actions WAF 429 pressure on Smoke.

## Decisions Made

- Decision: Bust edge/browser cache with content-hash `?v=` on HTML script tags and `$GITHUB_SHA` on Smoke, not only `.htaccess` revalidation.
- Reason: Proven that origin already had correct bytes while bare URLs stayed stale for up to a day under OpenResty.
- Decision: Leave `nephroctor.sk` / `.eu` alias change for panel work, not a repo-only redirect tweak.
- Reason: Upstream openresty 302 runs before Apache; `.htaccess` host rule is only a fallback after aliasing.
- Decision: Skip Beh #15 full doaudit.
- Reason: Job instructions; failure mode was deploy/cache, not a new audit finding.

## Blockers / Open Questions

- `nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel (no API access from this agent).
- Local deploy path for nephroctor.com still unavailable.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.

## Critical Files

- `index.html`
- `legal/cookies.html`
- `legal/ochrana-osobnych-udajov.html`
- `.github/workflows/deploy.yml`
- `.htaccess` (already revalidating from iter 4)
- `assets/clarity-consent.js` (query propagation from iter 4)
- `.audit.md`
- `state/SESSION.md`
- `state/TODO.md`

## Recent Commits

- 9b163b5 docs(handoff): complete nephroctor loop iter-4 cache revalidation
- 6e87685 fix(cache): version Clarity assets to bypass edge TTL
- 8b12f39 fix(ci): fetch Clarity smoke bodies as identity encoding
- eb74479 fix(cache): revalidate CSS/JS and smoke Clarity markers
- 0e3f3fc docs(handoff): record iter-3 Clarity CSP verify and deploy results

## Modified Files

- `index.html`, `legal/cookies.html`, `legal/ochrana-osobnych-udajov.html` (`?v=ec7132f34a`)
- `.github/workflows/deploy.yml` (Smoke `?v=$GITHUB_SHA`)
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`
- this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-210600-nephroctor-loop-iter-4.md`
- `.audit.md` (Loop iter 4 and 5)
- `state/TODO.md`

## Grok bots

- Status: optional; not invoked this iteration.

## Next Command

```text
git pull origin main
# In WebSupport panel: set nephroctor.sk and nephroctor.eu as domain aliases of nephroctor.com (not HTTP redirect), then verify https://nephroctor.sk/privacy -> 301 to https://nephroctor.com/legal/ochrana-osobnych-udajov.html
```
