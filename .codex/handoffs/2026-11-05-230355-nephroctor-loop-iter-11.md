# Handoff: nephroctor-loop-iter-11

## Metadata

- Generated At: 2026-11-05T23:03:55+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `7d1b63899c6de3884a678b0630c1cabbdd47518b`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-224651-nephroctor-loop-iter-10.md`

## Original Goal

Loop iteration 11 after AGENT_LOOP_TICK_nephroctor #10: prefer non-Clarity coherent improvement; skip alias work; one fix with commit/push/Deploy verify + production curl browser UA; complete handoff. No full Beh #15.

## Current State

Iteration 11 complete. Working tree clean on `origin/main` after docs handoff. Fix `7d1b638` is live: `/health-notice`, `/disclaimer`, `/zdravotne-upozornenie` and EN legal aliases 301 to medical disclaimer. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped this round as instructed).

## Completed This Session

- Verified clean tree at `d8144b4` (iter-10 handoff); skipped alias verify per job.
- In-repo improvement (non-Clarity):
  - `.htaccess`: RewriteRule + RedirectMatch for `/health-notice`, `/disclaimer`, `/zdravotne-upozornenie`, `/legal/disclaimer.html`, `/legal/health-notice.html` → `/legal/zdravotne-upozornenie.html`.
  - `legal/.htaccess`: fallback RewriteRule for `disclaimer.html` and `health-notice.html`.
  - `DEPLOY.md`, `.audit.md`, `state/SESSION.md`, `state/TODO.md` updated.
- Skipped Beh #15 full doaudit per job instructions.
- Did not bump sitemap `lastmod` for zdravotne-upozornenie (HTML content unchanged).

## Validated

- Deploy `7d1b638` https://github.com/polascin/nephroctor/actions/runs/42116937804: **success**. Smoke check **success**; Report security headers **success** (WAF 429 retries during smoke, then recovered).
- Production curl (browser UA):
  - `/` 200; CSP present; `Permissions-Policy` includes `browsing-topics=()`
  - `/health-notice` 301 → `/legal/zdravotne-upozornenie.html`
  - `/health-notice?lang=en` 301 with `?lang=en` preserved
  - `/disclaimer`, `/zdravotne-upozornenie` 301 → same target
  - `/legal/disclaimer.html`, `/legal/health-notice.html` 301 → same target
  - `/legal/zdravotne-upozornenie.html` 200

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).
- [ ] Optional in-repo: `/legal` EN alias polish, or other SEO discoverability only if a real 404 remains.

## Decisions Made

- Decision: Prefer health-notice URL shortcuts over further Clarity a11y polish.
- Reason: Job asked for non-Clarity; iter-10 handoff named `/health-notice`; prod confirmed 404s on those paths.
- Decision: Add `/disclaimer` and EN `/legal/*.html` aliases alongside SK `/zdravotne-upozornenie`.
- Reason: Footer already labels EN copy as “Medical disclaimer”; mirrors privacy/terms English path aliases.
- Decision: Skip Beh #15 full doaudit; skip alias verify this round.
- Reason: Job instructions.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF still rate-limits Smoke (429 with retry); do not treat as payload failure when retries succeed.

## Critical Files

- `.htaccess`, `legal/.htaccess`, `DEPLOY.md`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 7d1b638 fix(seo): add health-notice and disclaimer URL shortcuts
- d8144b4 docs(handoff): complete nephroctor loop iter-10 after accessibility shortcuts deploy [skip ci]
- dd94810 fix(seo): add accessibility URL shortcuts and refresh sitemap lastmod

## Modified Files

- `.htaccess`, `legal/.htaccess`, `DEPLOY.md`
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-224651-nephroctor-loop-iter-10.md`
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
# Optional next in-repo: only if a real remaining 404/SEO gap is confirmed; avoid Clarity churn
```
