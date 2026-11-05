# Handoff: nephroctor-loop-iter-13

## Metadata

- Generated At: 2026-11-05T23:44:38+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `1407eca9ff8bdd14ccfee3ac0e3fdc25d914238f`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-232638-nephroctor-loop-iter-12.md`

## Original Goal

Loop iteration 13 after AGENT_LOOP_TICK_nephroctor #12: prefer `/legal/accessibility.html` 301 → `/legal/pristupnost.html` (preserve `?lang=en`) unless higher-severity bug; skip `.sk`/`.eu` panel aliases; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 13 complete. Working tree clean on `origin/main` after docs handoff. Fix `1407eca` is live: `/legal/accessibility.html` 301 to `/legal/pristupnost.html` with query preserved. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped this round as instructed).

## Completed This Session

- Verified clean tree at `9cb3e46` (iter-12 handoff); skipped alias verify per job.
- In-repo SEO/discoverability alias (preferred fix):
  - `.htaccess`: RewriteRule + RedirectMatch for `/legal/accessibility.html` → `/legal/pristupnost.html`.
  - `legal/.htaccess`: fallback RewriteRule for `accessibility.html`.
  - `DEPLOY.md`, `.audit.md`, `state/SESSION.md`, `state/TODO.md` updated.
- Skipped `.sk`/`.eu` panel work per job.

## Validated

- Deploy `1407eca` https://github.com/polascin/nephroctor/actions/runs/42122459470: **success**. Smoke check **success**; Report security headers **success** (WAF 429 retries during smoke; not payload failure).
- Production curl (browser UA):
  - `/legal/accessibility.html` **301** → `https://nephroctor.com/legal/pristupnost.html`
  - `/legal/accessibility.html?lang=en` **301** → `.../pristupnost.html?lang=en`
  - `/accessibility` still **301** → `/legal/pristupnost.html`
  - `/legal/pristupnost.html` **200**; `/` **200**; CSP + `Permissions-Policy` with `browsing-topics=()` present

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).
- [ ] Optional in-repo: `/legal/imprint.html` / `/cookie-policy` EN discoverability aliases.

## Decisions Made

- Decision: Implement preferred `/legal/accessibility.html` alias this round (no higher-severity in-repo bug found).
- Reason: Job named it; prod was 404; same pattern as privacy/terms/disclaimer EN file aliases.
- Decision: Skip Beh full doaudit and skip alias verify this round.
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

- 1407eca fix(seo): add /legal/accessibility.html 301 to pristupnost
- 9cb3e46 docs(handoff): complete nephroctor loop iter-12 after legal lang a11y deploy [skip ci]
- d2eebd8 fix(a11y): announce legal document language switches via aria-live

## Modified Files

- `.htaccess`, `legal/.htaccess`, `DEPLOY.md`
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-232638-nephroctor-loop-iter-12.md`
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
# Optional next in-repo: /legal/imprint.html or /cookie-policy EN discoverability
```
