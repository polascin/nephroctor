# Handoff: nephroctor-loop-iter-20

## Metadata

- Generated At: 2026-11-06T02:05:34+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `3b97b0fe9f7b1d6609bd4ab06e4e05c233908ea6`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-014542-nephroctor-loop-iter-19.md`

## Original Goal

Loop iteration 20 after AGENT_LOOP_TICK_nephroctor #19: find another real bug (forms, focus, SEO meta, service worker, fonts, contrast, broken scripts, legal content accuracy); skip `.sk`/`.eu` panel and EN legal redirects; theme/Clarity/lang storage sync already done; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 20 complete. Working tree clean on `origin/main` after docs handoff. Fix `3b97b0f` is live: home-page language switch announces the new language autonym via `aria-live="polite"` after click or cross-tab sync; initial paint stays silent. Accessibility statement is version 1.5. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped).

## Completed This Session

- Focused audit: no forms, no service worker; fonts/contrast/links/i18n/structure/lang/legal audits green.
- Implemented home `announceLang` + `role="status"` live region; `switchLang(..., { announce: false })` on initial paint.
- Updated `legal/pristupnost.html` to 1.5 (SK + EN) documenting home announce.
- Updated `sitemap.xml` lastmod for `/` and pristupnost; extended `.audit/check_lang_logic.js`.

## Validated

- Local: `check_lang_logic.js`, `check_legal_logic.js`, `check_i18n.py`, `check_structure.py`, `check_format.py` all OK.
- Deploy `3b97b0f` https://github.com/polascin/nephroctor/actions/runs/42140368385: **success**. Smoke check **success**. Report security headers **success**.
- Production curl (browser UA):
  - `/` **200**; CSP + Permissions-Policy `browsing-topics=()`; `Cache-Control: no-cache, must-revalidate`
  - HTML contains `announceLang`, `aria-live', 'polite'`, `announce: false`
  - `/legal/pristupnost.html` **200**; SK `verzia 1.5` + EN `version 1.5` + home-announce wording
  - `/sitemap.xml` contains `2026-11-06`
- `gh` core rate limit healthy (~4700 remaining) before push.

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Manual screen-reader exercise of home language announce on production (covered by structural + legal announce pattern).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Optional SEO/meta polish: `twitter:image:alt`; static `og:locale:alternate`; reconcile manifest `theme_color` (`#0077b6`) with live theme-color metas.
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Fix home language announce via aria-live rather than SEO meta polish.
- Reason: Real a11y gap vs legal/Clarity already announcing; forms/SW absent; fonts/contrast/links green.
- Decision: Announce the language autonym (`translations[code].name`) without adding 24 new i18n keys.
- Reason: Autonym is already correct and self-describing; avoids translation risk and REQUIRED_KEYS churn.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF may still rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `index.html` (lang live region + `announceLang`)
- `legal/pristupnost.html` (statement 1.5)
- `sitemap.xml`
- `.audit/check_lang_logic.js`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 3b97b0f fix(a11y): announce home language switches via aria-live
- 8de4c17 docs(handoff): complete nephroctor loop iter-19 after lang sync deploy [skip ci]
- 52fac8c fix(i18n): sync nephroctor-lang across browser tabs

## Modified Files

- `index.html`, `legal/pristupnost.html`, `sitemap.xml`
- `.audit/check_lang_logic.js`, `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-014542-nephroctor-loop-iter-19.md`
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
# Or optional SEO: twitter:image:alt / og:locale:alternate / manifest theme_color reconciliation
```
