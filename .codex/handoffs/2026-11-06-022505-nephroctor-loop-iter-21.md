# Handoff: nephroctor-loop-iter-21

## Metadata

- Generated At: 2026-11-06T02:25:05+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `28b0f2048bb31c3678870637a7653205b80fa0d2`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-020534-nephroctor-loop-iter-20.md`

## Original Goal

Loop iteration 21 after AGENT_LOOP_TICK_nephroctor #20: preferred SEO/meta hardening (`twitter:image:alt`, `og:locale:alternate`, manifest `theme_color`) unless a higher-severity bug appears; skip `.sk`/`.eu` panel and EN legal redirects; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 21 complete. Working tree clean on `origin/main` after docs handoff. Fix `28b0f20` is live: home has `twitter:image:alt`, 23 static `og:locale:alternate` tags, and `site.webmanifest` `theme_color` `#f8fafc` matching `background_color` / light HTML `theme-color`. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped).

## Completed This Session

- No higher-severity functional bug found (forms/SW absent; prior theme/lang/Clarity work done).
- Implemented SEO/meta polish on `index.html` + `site.webmanifest`.
- Extended `.audit/check_i18n.py` (alt + alternates) and `.audit/check_assets.py` (theme_color).
- Updated `.audit.md`, `state/SESSION.md`, `state/TODO.md`.

## Validated

- Local: `check_i18n.py`, `check_assets.py`, `check_structure.py`, `check_format.py` all OK.
- Deploy `28b0f20` https://github.com/polascin/nephroctor/actions/runs/42142478714: **success**. Smoke check **success**. Report security headers **success**.
- Production curl (browser UA):
  - `/` **200**; CSP + Permissions-Policy `browsing-topics=()`; `Cache-Control: no-cache, must-revalidate`
  - HTML contains `twitter:image:alt`, 23× `og:locale:alternate`, matching image alt text
  - `/site.webmanifest` has `"theme_color": "#f8fafc"` and `"background_color": "#f8fafc"`
- `gh` core rate limit healthy (~4428 remaining) before push.

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Social-card preview scrapers (Twitter/X, Facebook Sharing Debugger) not re-run against live meta.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Prefer next real functional bug (fonts/contrast/scripts) or full Beh doaudit; SEO meta polish done.
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship SEO/meta polish rather than invent a lower-value a11y tweak.
- Reason: Job preferred these three gaps; no higher-severity bug appeared.
- Decision: Set manifest `theme_color` to `#f8fafc` (not keep brand `#0077b6`).
- Reason: Align with `background_color` and light HTML `theme-color`; dark chrome still uses collapsed HTML meta; `display: browser` so brand chrome was misleading.
- Decision: Keep `og:locale:alternate` static (do not rewrite on `switchLang`).
- Reason: Crawlers see default `sk_SK` + full alternate set; client-side locale swap must not drop alternates from the document head.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF may still rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `index.html` (twitter:image:alt + og:locale:alternate)
- `site.webmanifest` (theme_color)
- `.audit/check_i18n.py`, `.audit/check_assets.py`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 28b0f20 Improve SEO metas and align manifest theme_color.
- e451c9b docs(handoff): complete nephroctor loop iter-20 after lang announce deploy [skip ci]
- 3b97b0f fix(a11y): announce home language switches via aria-live

## Modified Files

- `index.html`, `site.webmanifest`
- `.audit/check_i18n.py`, `.audit/check_assets.py`, `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-020534-nephroctor-loop-iter-20.md`
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
# Or prefer next real functional bug / full Beh doaudit (SEO meta polish is done)
```
