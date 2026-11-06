# Handoff: nephroctor-loop-iter-19

## Metadata

- Generated At: 2026-11-06T01:45:42+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `52fac8cdd34b6a056f811debff4096884048b2de`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-012540-nephroctor-loop-iter-18.md`

## Original Goal

Loop iteration 19 after AGENT_LOOP_TICK_nephroctor #18: prefer cross-tab sync for `nephroctor-lang` (unless a higher-severity bug); skip `.sk`/`.eu` panel; no EN legal redirects; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 19 complete. Working tree clean on `origin/main` after docs handoff. Fix `52fac8c` is live: `nephroctor-lang` syncs across tabs on home and legal pages; legal storage sync does not collapse richer site codes (e.g. `de`) to `en`. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped). Lang/legal/theme audits green before push.

## Completed This Session

- Implemented home `storage` handler for `nephroctor-lang` → `switchLang`.
- Implemented legal `storage` handler via `resolveDocLang`; persist `nephroctor-lang` only on explicit SK/EN clicks.
- Extended `.audit/check_lang_logic.js` and `.audit/check_legal_logic.js`.
- Skipped `.sk`/`.eu` panel and further EN legal redirects per job.

## Validated

- Deploy `52fac8c` https://github.com/polascin/nephroctor/actions/runs/42137828847: **success**. Smoke check **success**. Report security headers **success**. (WAF 429 retries on some Smoke probes; Deploy did not fail.)
- Production curl (browser UA):
  - `/` **200**; CSP + Permissions-Policy `browsing-topics=()`; `Cache-Control: no-cache, must-revalidate`
  - HTML contains `e.key === 'nephroctor-lang'` / `switchLang(e.newValue)`
  - `/assets/legal.js` **200**, 8686 B; contains cross-tab language + no-collapse comment
  - `/legal/cookies.html` **200**
- `gh` core rate limit was healthy (~3900 remaining) before push.

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Manual multi-tab browser exercise of language sync on production (covered by legal storage cases + index structural check).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Prefer a real functional bug next (theme / Clarity / lang storage sync done).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Implement cross-tab `nephroctor-lang` sync rather than EN redirects or `.sk`/`.eu` panel.
- Reason: Named preferred job; theme and Clarity already sync; language did not.
- Decision: Legal storage sync must not `store.set` collapsed `sk`/`en` when another tab wrote e.g. `de`.
- Reason: Would overwrite the home-page language preference and cascade back via storage.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF may still rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `index.html` (lang `storage` listener)
- `assets/legal.js` (lang `storage` + click persist)
- `.audit/check_lang_logic.js`, `.audit/check_legal_logic.js`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 52fac8c fix(i18n): sync nephroctor-lang across browser tabs
- bd073aa docs(handoff): complete nephroctor loop iter-18 after system-theme deploy [skip ci]
- 7f4a761 fix(theme): follow system color scheme without locking data-theme

## Modified Files

- `index.html`, `assets/legal.js`
- `.audit/check_lang_logic.js`, `.audit/check_legal_logic.js`
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-012540-nephroctor-loop-iter-18.md`
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
# Prefer real functional bug next (theme/Clarity/lang storage sync done)
```
