# Handoff: nephroctor-loop-iter-26

## Metadata

- Generated At: 2026-11-06T04:05:02+01:00
- Completed At: 2026-11-06T04:12:00+01:00 (recovery after improve-loop shell kill)
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: 5ca7810
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-034957-nephroctor-loop-iter-25.md`

## Original Goal

Loop iteration 26 after AGENT_LOOP_TICK_nephroctor #25: audits/code review; one coherent real improvement (prefer functional/security/a11y; no more legal URL redirects unless broken inbound); skip `.sk`/`.eu` panel; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 26 code and Deploy completed before the 20-minute improve loop shell died (exit 4294967295, externally killed) while watching Deploy / writing handoff. Stub handoff placeholders filled during recovery. Fix `5ca7810` is live: root apple-touch icons. `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker; skipped).

## Completed This Session

- Root `/apple-touch-icon.png` and `/apple-touch-icon-precomposed.png` copied from `assets/` (byte-identical).
- Deploy payload + `check_assets` asserts for root apple-touch presence and match.
- `DEPLOY.md`, `README.md`, `.audit.md`, `state/SESSION.md`, `state/TODO.md` updated.
- Deploy watched to success (Smoke + Report security headers); Actions WAF 429 annotations with retries, not payload failure.

## Validated

- Deploy `5ca7810` run 42153206194: **success**. Smoke check **success**. Report security headers **success** (with 429 probe warnings).
- Production curl (browser UA):
  - `/` **200** HTML + security headers (CSP, X-Frame-Options DENY, Permissions-Policy browsing-topics)
  - `/apple-touch-icon.png` **200** `image/png` length 10468
  - `/apple-touch-icon-precomposed.png` **200** `image/png`

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Optional follow-up noted in recovery: root `/manifest.webmanifest` was still **404** (HTML links `site.webmanifest`).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport domain alias for `.sk`/`.eu`; then `tools/verify-domain-aliases.ps1`.
- [ ] Prefer a real functional/security/a11y bug next. Optional low: root `manifest.webmanifest` copy (taken in iter 27).
- [ ] Local SFTP deploy replacement (blocked).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship root apple-touch copies (same pattern as root `favicon.ico`).
- Reason: Prod 404 on implicit iOS requests; no higher-severity bug found; legal redirects and `.sk`/`.eu` panel skipped per brief.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel**.
- Local deploy path for nephroctor.com still unavailable on this machine.
- Actions WAF may rate-limit Smoke/security-header probes (429 with retry).
- Improve loop shell can be externally killed mid-`gh run watch`; recovery must re-verify Deploy + complete handoff.

## Critical Files

- `apple-touch-icon.png`, `apple-touch-icon-precomposed.png`
- `.github/workflows/deploy.yml`, `.audit/check_assets.py`
- `DEPLOY.md`, `README.md`, `.audit.md`, state files

## Recent Commits

- 5ca7810 fix(assets): serve root apple-touch icons for iOS requests
- fa584bd docs(handoff): complete nephroctor loop iter-25 after Clarity Tab trap [skip ci]
- 9064941 fix(a11y): keep Clarity Tab trap on dialog container focus

## Context To Load

- This handoff
- Next: iter-27 handoff after `manifest.webmanifest`

## Next Command

```text
# Prefer real functional/security/a11y bug; root apple-touch done
# Optional low: root manifest.webmanifest (common probe 404)
# User panel: nephroctor.sk / .eu as domain aliases (not HTTP redirect)
powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1
```
