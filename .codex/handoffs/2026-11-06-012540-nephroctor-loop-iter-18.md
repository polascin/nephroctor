# Handoff: nephroctor-loop-iter-18

## Metadata

- Generated At: 2026-11-06T01:25:40+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `7f4a761adaf2567a943455d7d67c1905ee834619`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-010806-nephroctor-loop-iter-17.md`

## Original Goal

Loop iteration 18 after AGENT_LOOP_TICK_nephroctor #17: investigate via audits/code/browser; pick one real improvement (prefer functional/security/a11y/i18n/perf over EN legal redirects); skip `.sk`/`.eu` panel; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 18 complete. Working tree clean on `origin/main` after docs handoff. Fix `7f4a761` is live: without an explicit `nephroctor-theme`, `data-theme` stays unset (CSS media + live `prefers-color-scheme` change keep page and theme-color in sync). `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped). Audits green before and after the fix.

## Completed This Session

- Ran structure/format/theme/legal audits (all OK before change); spot-checked production redirects (shortcuts 301 OK; PowerShell false alarm on max-redirection).
- Code review found regression from iter 17: collapsed `theme-color` without `media` plus bootstrap that promoted OS dark into `data-theme="dark"` locked the page and stopped live OS follow.
- Fixed bootstrap on index + all `legal/*.html`; storage clear no longer re-locks dark; `matchMedia` `change` listener in `index.html` and `assets/legal.js`.
- Updated `.audit/check_theme_logic.js` for system-follow semantics.
- Skipped `.sk`/`.eu` panel and further EN legal redirects per job.

## Validated

- Deploy `7f4a761` https://github.com/polascin/nephroctor/actions/runs/42135573326: **success**. Smoke check **success**. Report security headers **success**. (WAF 429 retries on some probes during Smoke; Deploy did not fail.)
- Production curl (browser UA):
  - `/` **200**; CSP + Permissions-Policy `browsing-topics=()`; `Cache-Control: no-cache, must-revalidate`
  - HTML contains `leave data-theme unset` + `onColorScheme`
  - `/assets/legal.js` **200**, 8090 B; contains `onColorScheme` / collapsed theme-color comment
  - `/legal/cookies.html` **200**; bootstrap leave-unset; no OS-dark `setAttribute('data-theme', 'dark')`

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Manual OS theme toggle while page open on production (covered by `check_theme_logic.js` system-follow cases + listener present in prod JS).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Candidate real bug: cross-tab `nephroctor-lang` sync (theme and Clarity already sync; language does not).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Fix system theme follow regression rather than EN redirects or `.sk`/`.eu` panel.
- Reason: Material regression from iter-17 theme-color collapse; audits otherwise green.
- Decision: Do not write `data-theme="dark"` for bare OS dark; leave unset so CSS media applies.
- Reason: Writing the attribute locked the page against later OS light switches and fought the CSS design (`:root:not([data-theme="light"])` under media).

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF may still rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `index.html` (bootstrap + `onColorScheme` + storage)
- `assets/legal.js`
- `legal/*.html` (theme bootstrap)
- `.audit/check_theme_logic.js`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 7f4a761 fix(theme): follow system color scheme without locking data-theme
- ea02dcc docs(handoff): complete nephroctor loop iter-17 after theme-color deploy [skip ci]
- 83bac1e fix(theme): sync theme-color with page theme across tabs

## Modified Files

- `index.html`, `assets/legal.js`, all `legal/*.html` theme bootstraps
- `.audit/check_theme_logic.js`
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-010806-nephroctor-loop-iter-17.md`
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
# Prefer real functional bug next; candidate: cross-tab nephroctor-lang sync
```
