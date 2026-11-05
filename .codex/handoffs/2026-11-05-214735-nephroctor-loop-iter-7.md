# Handoff: nephroctor-loop-iter-7

## Metadata

- Generated At: 2026-11-05T21:47:35+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `a6743801b6a813a9592d04e94594fc99023841d3`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-05-211543-nephroctor-loop-iter-6.md`

## Original Goal

Loop iteration 7 after AGENT_LOOP_TICK_nephroctor #6: git/handoffs status; optional alias verify once; one coherent in-repo improvement with commit/push/Deploy verify + production curl; complete handoff; note aliases if still user-blocked.

## Current State

Iteration 7 complete. Working tree clean on `origin/main` after docs handoff. Fix `a674380` is live: RFC 9116 `security.txt`, consent `aria-expanded`/`aria-controls`, 44 px touch targets, accessibility statement v1.1, Clarity `?v=410f2d7022`. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged).

## Completed This Session

- Verified clean tree at `cfacb14` (iter-6 handoff); `tools/verify-domain-aliases.ps1` still 4× FAIL.
- In-repo improvement:
  - `.well-known/security.txt` (Contact, Expires 2027-11-05, Policy); `/security.txt` 301; deploy payload includes it.
  - `clarity-consent.js`: `aria-expanded`, `aria-controls`, dialog `id`; CSS min 44×44 px; HTML `?v=410f2d7022`.
  - `legal/pristupnost.html` v1.1: honest Clarity wording + dialog measures + JS/inert limitation; sitemap lastmod.
- Updated `.audit.md`, `state/SESSION.md`, `state/TODO.md`.
- Skipped Beh #15 full doaudit per job instructions.

## Validated

- Local: `test_clarity.cjs`, format/assets/structure/links PASS.
- `tools/verify-domain-aliases.ps1`: `.com/privacy` OK; four `.sk`/`.eu` FAIL (expected).
- Deploy `a674380` https://github.com/polascin/nephroctor/actions/runs/42105167113: **success**. Smoke check **success**; Report security headers **success** (CI header probe warned on 429; production curl OK).
- Production curl (browser UA):
  - `/` 200; CSP/HSTS/nosniff/DENY; `Cache-Control: no-cache, must-revalidate`; HTML `clarity-consent.js?v=410f2d7022`
  - `/assets/clarity-consent.js?v=410f2d7022` 8752 B: `aria-expanded`, `aria-controls`, `setBackgroundInert`
  - `/.well-known/security.txt` 200 (291 B, Contact/Expires/Policy); `/security.txt` 301 → well-known
  - `/legal/pristupnost.html` 200 with v1.1 + Clarity dialog measures
  - `https://nephroctor.sk/privacy` still **302** to apex (panel open)

## Not Yet Validated

- AT check that `aria-expanded` announces correctly when reopening from settings.
- Panel alias change (requires human in WebSupport admin).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Do not burn the iteration on panel/SSH retries; ship security.txt + dialog a11y + statement accuracy.
- Reason: Alias verify confirmed unchanged OpenResty 302; SSH still cannot reconfigure domains.
- Decision: Skip Beh #15 full doaudit.
- Reason: Job instructions.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.

## Critical Files

- `.well-known/security.txt`
- `assets/clarity-consent.js`, `assets/clarity-consent.css`
- `legal/pristupnost.html`
- `.htaccess`, `.github/workflows/deploy.yml`
- `index.html`, `legal/cookies.html`, `legal/ochrana-osobnych-udajov.html`
- `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- a674380 fix(security,a11y): add security.txt and expand consent dialog a11y
- cfacb14 docs(handoff): complete nephroctor loop iter-6 after inert/WAF deploy [skip ci]
- bfc116f fix(a11y,ci): inert consent dialog and ease Smoke WAF pressure

## Modified Files

- `.well-known/security.txt` (new)
- `assets/clarity-consent.js` / `.css`; HTML `?v=410f2d7022`
- `legal/pristupnost.html`, `sitemap.xml`, `.htaccess`, deploy.yml
- `.audit.md`, state files, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-05-211543-nephroctor-loop-iter-6.md`
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
