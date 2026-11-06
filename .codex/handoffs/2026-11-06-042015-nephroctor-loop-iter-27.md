# Handoff: nephroctor-loop-iter-27

## Metadata

- Generated At: 2026-11-06T04:20:15+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: 8494589 (84945895b9ec42f60057e40a2f9d03169ed039eb)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-040502-nephroctor-loop-iter-26.md`

## Original Goal

Recovery after 20-minute Nephroctor improve loop shell died (exit 4294967295, externally killed). Parent restarting. Confirm HEAD / Deploy / prod for iter 26; finish incomplete WIP if any; otherwise one coherent real improvement (no legal redirects, skip `.sk`/`.eu` panel); report doaudit terminal 28001 only.

## Current State

Recovery complete. Iter 26 apple-touch Deploy was already success; stub handoff completed (also docs commit `7ad983d`). Iter 27 shipped root `manifest.webmanifest` and is live. Working tree clean after docs handoff commit. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker; skipped).

## Completed This Session

- Confirmed HEAD was `5ca7810` apple-touch; Deploy run 42153206194 **success**; prod apple-touch PNG **200**.
- Completed stub iter-26 handoff (placeholders → facts); parallel docs commit `7ad983d` [skip ci] also landed.
- No incomplete WIP beyond handoff stub; Deploy had finished.
- Iter 27: root `/manifest.webmanifest` byte-identical to `site.webmanifest` (prod was **404**).
- Deploy payload + `check_assets` / `check_format` asserts; `DEPLOY.md` / `README.md` / `.audit.md` / state updated.
- Daily doaudit loop terminal 28001: **still running** (report only; parent owns restarts).

## Validated

- Deploy `8494589` https://github.com/polascin/nephroctor/actions/runs/42154902070: **success**. Smoke check **success**. Report security headers **success** (Actions WAF 429 warnings on probes; local prod headers OK).
- Production curl (browser UA):
  - `/` **200** + CSP / X-Frame-Options DENY / Permissions-Policy browsing-topics / HSTS
  - `/manifest.webmanifest` **200** `application/manifest+json` (JSON name Nephroctor)
  - `/site.webmanifest` **200** same type/length
  - `/apple-touch-icon.png` **200** `image/png` (iter 26 still good)

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Prefer a real functional/security/a11y bug next (root apple-touch + root manifest probe paths done).
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: After verifying iter 26 Deploy live, ship root `manifest.webmanifest` rather than invent a marginal Clarity tweak.
- Reason: Confirmed prod **404** on a common tooling probe; same proven pattern as root favicon / apple-touch; no higher-severity bug in green audits; legal redirects and `.sk`/`.eu` panel skipped per brief.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel**.
- Local deploy path for nephroctor.com still unavailable on this machine.
- Actions WAF may rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.
- Improve loop shell can be externally killed mid-watch; recovery must re-verify Deploy + complete handoff.

## Critical Files

- `manifest.webmanifest`
- `.github/workflows/deploy.yml`
- `.audit/check_assets.py`, `.audit/check_format.py`
- `DEPLOY.md`, `README.md`, `.audit.md`, `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 8494589 fix(assets): serve root manifest.webmanifest for common probes
- 7ad983d docs(handoff): complete nephroctor loop iter-26 after root apple-touch icons [skip ci]
- 5ca7810 fix(assets): serve root apple-touch icons for iOS requests

## Modified Files

- `manifest.webmanifest` (new)
- deploy/audit/docs/state as above
- this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-040502-nephroctor-loop-iter-26.md`
- `state/TODO.md`

## Next Command

```text
git pull origin main
# Prefer real functional/security/a11y bug; root apple-touch + manifest.webmanifest done
# User: WebSupport panel → nephroctor.sk and nephroctor.eu as domain aliases of nephroctor.com (not HTTP redirect)
powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1
```
