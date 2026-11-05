# Handoff: nephroctor-loop-iter-12

## Metadata

- Generated At: 2026-11-05T23:26:38+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `d2eebd874732b17fd8a1cd9730e006bdb5890703`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-230355-nephroctor-loop-iter-11.md`

## Original Goal

Loop iteration 12 after AGENT_LOOP_TICK_nephroctor #11: prefer coherent non-trivial improvement (bug, a11y beyond redirects, security, i18n, performance, content accuracy); skip `.sk`/`.eu` alias panel work; one fix with commit/push/Deploy verify + production curl browser UA; complete handoff. No full Beh #15. Rate-limit aware `gh`.

## Current State

Iteration 12 complete. Working tree clean on `origin/main` after docs handoff. Fix `d2eebd8` is live: legal document SK/EN switch announces via polite live region; accessibility statement v1.4. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped this round as instructed).

## Completed This Session

- Verified clean tree at `3d4f2b8` (iter-11 handoff); skipped alias verify per job.
- In-repo improvement (a11y, non-Clarity, non-redirect):
  - `assets/legal.js`: `role="status"` + `aria-live="polite"` announce on user-initiated SK/EN switch; initial `?lang=` / storage paint stays silent; same-language re-click does not re-announce.
  - `.audit/check_legal_logic.js`: DOM stub `createElement`/`body` + click announce cases.
  - `legal/pristupnost.html` v1.4: declares legal-doc live announce.
  - `.audit.md`, `state/SESSION.md`, `state/TODO.md` updated.
- Skipped Beh #15 full doaudit per job instructions.
- Did not add `/legal/accessibility.html` alias this round (still prod 404; named next optional in-repo).

## Validated

- Local: `node .audit/check_legal_logic.js` all cases OK (incl. announce); structure/format OK.
- Deploy `d2eebd8` https://github.com/polascin/nephroctor/actions/runs/42119984638: **success**. Smoke check **success**; Report security headers **success**.
- Production curl (browser UA):
  - `/` 200; CSP present; `Permissions-Policy` includes `browsing-topics=()`
  - `/legal/pristupnost.html` 200; body contains verzia/version **1.4** and `aria-live` mention
  - `/assets/legal.js` 200; contains `Document language: English` and `aria-live`
  - `/legal/accessibility.html` still **404** (left for next optional in-repo)

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Screen-reader manual listen of the legal-doc announce (logic + DOM covered by audit; AT not run in CI).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).
- [ ] Optional in-repo: `/legal/accessibility.html` (prod 404) and possibly `/legal/imprint.html` / `/cookie-policy` EN discoverability.

## Decisions Made

- Decision: Prefer legal-doc `aria-live` language announce over another redirect batch.
- Reason: Job asked for coherent non-trivial improvement and listed a11y beyond redirects; audits were green; `/legal/accessibility.html` 404 remains optional SEO polish.
- Decision: Announce only on user click with actual language change, not on initial paint.
- Reason: Avoid noisy status on every legal page load when `?lang=en` or stored preference applies.
- Decision: Skip Beh #15 full doaudit; skip alias verify this round.
- Reason: Job instructions.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF still rate-limits Smoke (429 with retry); do not treat as payload failure when retries succeed.

## Critical Files

- `assets/legal.js`, `legal/pristupnost.html`, `.audit/check_legal_logic.js`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- d2eebd8 fix(a11y): announce legal document language switches via aria-live
- 3d4f2b8 docs(handoff): complete nephroctor loop iter-11 after health-notice shortcuts deploy [skip ci]
- 7d1b638 fix(seo): add health-notice and disclaimer URL shortcuts

## Modified Files

- `assets/legal.js`, `legal/pristupnost.html`, `.audit/check_legal_logic.js`
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-230355-nephroctor-loop-iter-11.md`
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
# Optional next in-repo: /legal/accessibility.html → 301 → /legal/pristupnost.html (prod 404 today)
```
