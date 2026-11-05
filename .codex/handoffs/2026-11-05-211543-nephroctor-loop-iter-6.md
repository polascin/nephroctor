# Handoff: nephroctor-loop-iter-6

## Metadata

- Generated At: 2026-11-05T21:26:00+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `bfc116ff503371465acf6629c16fe52cbf3d5f68`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-211049-nephroctor-loop-iter-5.md`

## Original Goal

Loop iteration 6 after AGENT_LOOP_TICK_nephroctor #5: verify git/handoffs and `.sk`/`.eu` curl behavior; attempt domain alias fix only via available tooling; otherwise one coherent in-repo improvement; commit/push/deploy verify; complete handoff.

## Current State

Iteration 6 complete. Working tree clean on `origin/main` after docs handoff. Fix `bfc116f` is live: consent dialog uses HTML `inert` on background, privacy fallback corrected, Smoke WAF load reduced, panel alias steps documented. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged).

## Completed This Session

- Verified clean tree at `ba1a67f` (iter-5 handoff); pulled `origin/main`.
- Curl+UA: `nephroctor.sk|eu` `/privacy|/terms|/cookies|/legal` and `www.*` all **302** → `https://nephroctor.com` (path dropped); `.com/privacy` **301** path-preserving.
- SSH alias `websupport` connects (uid58858 / shell.r1.websupport.sk) but webroot is **polascin.net** only; no nephroctor.com tree; no domain/panel CLI. Alias change impossible from this agent.
- In-repo improvement instead:
  - `assets/clarity-consent.js`: `setBackgroundInert`, `aria-haspopup="dialog"`, privacy fallback `/legal/ochrana-osobnych-udajov.html`.
  - HTML `?v=c0d880beb6` (content hash).
  - Smoke: drop `/robots.txt` + `/assets/site.css` GETs; inter-request sleep 8s; security-header probe 3× retry.
  - `DEPLOY.md` panel steps; `tools/verify-domain-aliases.ps1` (run with `-ExecutionPolicy Bypass` if needed).
- Updated `.audit.md`, `state/SESSION.md`, `state/TODO.md`.
- Skipped Beh #15 full doaudit per job instructions.

## Validated

- Local: `test_clarity.cjs`, `check_format.py`, `check_assets.py` PASS.
- `tools/verify-domain-aliases.ps1`: `.com/privacy` OK; four `.sk`/`.eu` cases FAIL with 302 hint (expected until panel).
- Deploy `bfc116f` https://github.com/polascin/nephroctor/actions/runs/42101703816: **success**. Smoke check **success**; Report security headers **success**.
- Production curl (browser UA):
  - `/` 200; CSP/HSTS/nosniff/DENY; `Cache-Control: no-cache, must-revalidate`; HTML `clarity-consent.js?v=c0d880beb6`
  - `/assets/clarity-consent.js?v=c0d880beb6` 8406 B: `setBackgroundInert`, `aria-haspopup`, privacy fallback
  - `https://nephroctor.sk/privacy` still **302** to apex (panel open)

## Not Yet Validated

- Visual/AT check that `inert` hides page content from screen readers while banner is open.
- Panel alias change (requires human in WebSupport admin).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Do not invent panel/API credentials; document exact panel steps and ship unrelated high-value a11y/CI fix.
- Reason: SSH `websupport` is a different hosting account; OpenResty 302 runs before Apache.
- Decision: Soften Smoke by removing payload-already-checked static GETs rather than lengthening every backoff aggressively.
- Reason: Past runs hit 429 on `/robots.txt` and `/assets/site.css`; HTML + Clarity markers + legal 301s remain.
- Decision: Skip Beh #15 full doaudit.
- Reason: Job instructions.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.

## Critical Files

- `assets/clarity-consent.js`
- `index.html`, `legal/cookies.html`, `legal/ochrana-osobnych-udajov.html`
- `.github/workflows/deploy.yml`
- `DEPLOY.md`
- `tools/verify-domain-aliases.ps1`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- bfc116f fix(a11y,ci): inert consent dialog and ease Smoke WAF pressure
- ba1a67f docs(handoff): complete nephroctor loop iter-5 after Clarity ?v= deploy [skip ci]
- 9b163b5 docs(handoff): complete nephroctor loop iter-4 cache revalidation
- 6e87685 fix(cache): version Clarity assets to bypass edge TTL
- 8b12f39 fix(ci): fetch Clarity smoke bodies as identity encoding

## Modified Files

- `assets/clarity-consent.js` (inert, haspopup, privacy fallback)
- HTML Clarity `?v=c0d880beb6`
- `.github/workflows/deploy.yml` (leaner Smoke, header retries)
- `DEPLOY.md`, `tools/verify-domain-aliases.ps1`
- `.audit/test_clarity.cjs`, `.audit.md`, state files
- this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-211049-nephroctor-loop-iter-5.md`
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
```
