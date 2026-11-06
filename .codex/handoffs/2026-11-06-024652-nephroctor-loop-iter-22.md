# Handoff: nephroctor-loop-iter-22

## Metadata

- Generated At: 2026-11-06T02:46:52+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `6b3154e4ec46226ffff71c6b8d90d4ca8bedd127`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-022505-nephroctor-loop-iter-21.md`

## Original Goal

Loop iteration 22 after AGENT_LOOP_TICK_nephroctor #21: find one coherent real improvement (prefer functional/security/a11y); skip `.sk`/`.eu` panel and EN legal redirects; rate-limit aware `gh`; light audit OK (no full Beh #15 unless critical); commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 22 complete. Working tree clean on `origin/main` after docs handoff. Fix `6b3154e` is live: skip-to-content targets are focusable via `tabindex="-1"` on `<main id="main">` (home + all legal pages); `#main:focus` outline suppressed; accessibility statement 1.6; structure audit asserts the attribute. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped).

## Completed This Session

- Light audit: structure/contrast/fonts/assets/links/lang/legal/theme green; no critical Beh #15 failures.
- Found WCAG 2.4.1 gap: skip link scrolled but often left keyboard focus on the skip control.
- Noted prod `/impressum` **404** (DE parallel of working `/imprint`); deferred in favour of the a11y fix (not an EN legal redirect).
- Implemented skip-target `tabindex="-1"`, CSS, statement 1.6, `check_structure.py` assert; updated `.audit.md`, `state/SESSION.md`, `state/TODO.md`.

## Validated

- Local: `check_structure.py`, `check_format.py`, `check_contrast.py`, `check_lang_logic.js`, `check_legal_logic.js` OK.
- Deploy `6b3154e` https://github.com/polascin/nephroctor/actions/runs/42144923500: **success**. Smoke check **success**. Report security headers **success** (WAF **429** annotations on header/smoke probes; not treated as payload failure).
- Production curl (browser UA):
  - `/` **200**; CSP present; Permissions-Policy includes `browsing-topics=()`; `Cache-Control: must-revalidate, no-cache`; HTML has `<main id="main" tabindex="-1">`
  - `/legal/pristupnost.html` **200**; SK `verzia 1.6` + EN `version 1.6` + tabindex wording; `<main … tabindex="-1">`
  - `/legal/cookies.html` **200** with tabindex
  - `/assets/site.css` **200** contains `#main:focus { outline: none }`
- `gh` core rate limit healthy (~4018 remaining) before push.

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Manual keyboard exercise of skip-link focus move on production (covered by markup + WCAG technique H69/G1).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Optional in-repo: `/impressum` + `/legal/impressum.html` → 301 `/legal/pravne-informacie.html` (prod 404; DE discoverability parallel to `/imprint`).
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship skip-link focus fix rather than `/impressum` redirect.
- Reason: Job preferred real a11y/functional bug; impressum is discoverability (and not EN), lower severity than broken keyboard bypass.
- Decision: Suppress `#main:focus` outline.
- Reason: Programmatic focus after skip should not flash a 3 px ring around the entire landmark; interactive controls keep `:focus-visible` rings.
- Decision: Do not run full Beh #15.
- Reason: Light audit clean; no critical failures.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF may still rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `index.html`, `legal/*.html` (`tabindex="-1"` on `#main`)
- `assets/site.css` (`#main:focus`)
- `legal/pristupnost.html` (statement 1.6)
- `.audit/check_structure.py`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 6b3154e fix(a11y): make skip-link target focusable with tabindex -1
- b511143 docs(handoff): complete nephroctor loop iter-21 after SEO meta deploy [skip ci]
- 28b0f20 Improve SEO metas and align manifest theme_color.

## Modified Files

- `index.html`, `legal/*.html`, `assets/site.css`
- `.audit/check_structure.py`, `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-022505-nephroctor-loop-iter-21.md`
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
# Or optional: /impressum (+ /legal/impressum.html) 301 → /legal/pravne-informacie.html
```
