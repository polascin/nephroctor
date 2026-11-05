# Handoff: nephroctor-loop-iter-14

## Metadata

- Generated At: 2026-11-06T00:04:28+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `c9cc9fb421d3a722f95021f20db2cc48c1f50d16`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-234438-nephroctor-loop-iter-13.md`

## Original Goal

Loop iteration 14 after AGENT_LOOP_TICK_nephroctor #13: investigate `/legal/imprint.html` and/or `/cookie-policy` 404s (prefer a real bug over more redirects if found); skip `.sk`/`.eu` panel; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 14 complete. Working tree clean on `origin/main` after docs handoff. Fix `c9cc9fb` is live: imprint and cookie-policy EN discoverability aliases 301 to canonical Slovak legal HTML with query preserved. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped this round as instructed). No higher-severity in-repo bug found this round.

## Completed This Session

- Verified clean tree at `51d97e9` (iter-13 handoff); prod probe confirmed 404 on imprint/cookie-policy variants; skipped alias verify per job.
- In-repo SEO/discoverability aliases:
  - `.htaccess`: RewriteRule + RedirectMatch for `/imprint`, `/legal/imprint.html` → `/legal/pravne-informacie.html`; `/cookie-policy`, `/legal/cookie-policy.html` → `/legal/cookies.html`.
  - `legal/.htaccess`: fallback RewriteRule for `imprint.html` and `cookie-policy.html`.
  - `DEPLOY.md`, `.audit.md`, `state/SESSION.md`, `state/TODO.md` updated.
- Skipped `.sk`/`.eu` panel work per job.

## Validated

- Deploy `c9cc9fb` https://github.com/polascin/nephroctor/actions/runs/42125306683: **success**. Smoke check **success** (WAF 429 retries on `/privacy`, `/terms`, `/legal`; not payload failure). Report security headers step **success** (Actions IP WAF 429 exhausted probe retries; local browser-UA curl still shows CSP + Permissions-Policy).
- Production curl (browser UA):
  - `/legal/imprint.html` **301** → `https://nephroctor.com/legal/pravne-informacie.html`
  - `/legal/imprint.html?lang=en` **301** → `.../pravne-informacie.html?lang=en`
  - `/imprint` **301** → same target
  - `/cookie-policy` and `/legal/cookie-policy.html` **301** → `/legal/cookies.html` (`?lang=en` preserved)
  - `/legal/pravne-informacie.html` **200**; `/legal/cookies.html` **200**; `/` **200**; CSP + `Permissions-Policy` with `browsing-topics=()` present

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).
- [ ] Prefer a real functional bug next; named EN legal redirect aliases for accessibility/imprint/cookie-policy are done.

## Decisions Made

- Decision: Implement both imprint and cookie-policy aliases this round (no higher-severity in-repo bug found).
- Reason: Job named them; prod was 404; same pattern as privacy/terms/accessibility EN file aliases; imprint maps to legal notice (`pravne-informacie`), cookie-policy to `cookies.html`.
- Decision: Skip Beh full doaudit and skip alias verify this round.
- Reason: Job instructions.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF still rate-limits Smoke and security-header probe (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `.htaccess`, `legal/.htaccess`, `DEPLOY.md`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- c9cc9fb fix(seo): add imprint and cookie-policy 301 aliases
- 51d97e9 docs(handoff): complete nephroctor loop iter-13 after accessibility alias deploy [skip ci]
- 1407eca fix(seo): add /legal/accessibility.html 301 to pristupnost

## Modified Files

- `.htaccess`, `legal/.htaccess`, `DEPLOY.md`
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-234438-nephroctor-loop-iter-13.md`
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
# Prefer real functional bug next; EN legal alias polish for imprint/cookie-policy/accessibility is done
```
