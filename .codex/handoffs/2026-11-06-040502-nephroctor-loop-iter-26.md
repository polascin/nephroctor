# Handoff: nephroctor-loop-iter-26

## Metadata

- Generated At: 2026-11-06T04:05:02+01:00
- Project Root: D:\Dev\nephroctor
- Git Branch: main
- Head Commit: (docs handoff after fix `5ca7810`)
- Production: https://nephroctor.com
- Prior handoff: `.codex/handoffs/2026-11-06-034957-nephroctor-loop-iter-25.md`

## Original Goal

Loop iteration 26 after AGENT_LOOP_TICK_nephroctor #25: one coherent real improvement (apple-touch redirect/copy OK if nothing better); prefer higher-severity bug if found; no legal redirects; skip `.sk`/`.eu` panel; rate-limit aware `gh`; commit/push/Deploy verify + production curl browser UA; complete handoff.

## Current State

Iteration 26 complete. Working tree clean on `origin/main` after docs handoff. Fix `5ca7810` is live: root `/apple-touch-icon.png` and `/apple-touch-icon-precomposed.png` are byte-identical copies of `assets/apple-touch-icon.png` (same pattern as root `favicon.ico`). `.sk`/`.eu` still OpenResty **302** path-drop (panel blocker unchanged; skipped).

## Completed This Session

- Focused audit: assets/structure/clarity green; no higher-severity functional/security/a11y bug surfaced.
- Prod probe before fix: `/apple-touch-icon.png` and `/apple-touch-icon-precomposed.png` **404**; `/assets/apple-touch-icon.png` and `/favicon.ico` **200**.
- Root copies from `assets/apple-touch-icon.png` (SHA256 match).
- `.github/workflows/deploy.yml`: stage + Verify deploy payload for both root icons (required; deploy uses explicit file list).
- `.audit/check_assets.py`: presence + byte-identity asserts.
- Docs: `.audit.md` iter-26, `DEPLOY.md`, `README.md`, `state/SESSION.md`, `state/TODO.md`.

## Validated

- Deploy `5ca7810` https://github.com/polascin/nephroctor/actions/runs/42153206194: **success**. Smoke check **success**. Report security headers **success** (Actions IP saw 429 annotations on some probes; Smoke still green; local prod headers verified).
- Production curl (browser UA):
  - `/` **200**; CSP present; `X-Frame-Options: DENY`; `Permissions-Policy` includes `browsing-topics=()`
  - `/apple-touch-icon.png` **200**, `image/png`, 10468 bytes
  - `/apple-touch-icon-precomposed.png` **200**, `image/png`, 10468 bytes
  - `/assets/apple-touch-icon.png` **200**, 10468 bytes
  - `/favicon.ico` **200**

## Not Yet Validated

- Panel alias change (requires human in WebSupport admin).
- Local SFTP deploy path for nephroctor.com.
- Manual iOS home-screen add (logic covered by prod 200 + audit asserts).

## Remaining Work

- [ ] **Next priority (user panel):** WebSupport: switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`; then `powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1`.
- [ ] Prefer a real functional/security/a11y bug next (root apple-touch icons done).
- [ ] Local SFTP deploy replacement (blocked: no nephroctor.com on SSH `websupport`; secrets only in GitHub Actions).
- [ ] Clarity dashboard aggregate counters (informational).

## Decisions Made

- Decision: Ship root apple-touch copies (not another legal URL alias).
- Reason: No higher-severity bug found after audit/prod probe; job explicitly allowed apple-touch redirect/copy; iOS still probes root paths even when `<link rel="apple-touch-icon">` points at `/assets/…`.
- Decision: Include `apple-touch-icon-precomposed.png` as the same bytes.
- Reason: Prod also returned 404 for the legacy precomposed request; one coherent asset fix covers both implicit iOS probes.
- Decision: Update deploy workflow payload list, not only the repo root.
- Reason: Deploy stages an explicit file set; a root file not listed would never reach production.

## Blockers / Open Questions

- **`nephroctor.sk` / `.eu` path-preserving fix requires WebSupport customer panel** (no API from this agent; SSH cannot reconfigure domains).
- Local deploy path for nephroctor.com still unavailable on this machine.
- Commits need `C:\Python314\Scripts` on PATH for `ggshield`.
- Parallel loop agents can race; pull before commit. Prefer sparse `gh` polling.
- Actions WAF may still rate-limit Smoke/security-header probes (429 with retry); do not treat as payload failure when Smoke succeeds and local prod headers verify.

## Critical Files

- `apple-touch-icon.png`, `apple-touch-icon-precomposed.png` (root)
- `assets/apple-touch-icon.png`
- `.github/workflows/deploy.yml`
- `.audit/check_assets.py`
- `.audit.md`, `DEPLOY.md`, `README.md`
- `state/SESSION.md`, `state/TODO.md`

## Recent Commits

- 5ca7810 fix(assets): serve root apple-touch icons for iOS requests
- fa584bd docs(handoff): complete nephroctor loop iter-25 after Clarity Tab trap [skip ci]
- 9064941 fix(a11y): keep Clarity Tab trap on dialog container focus

## Modified Files

- Root apple-touch PNGs, deploy workflow, check_assets, docs/state, this handoff

## Context To Load

- This handoff
- `.codex/handoffs/2026-11-06-034957-nephroctor-loop-iter-25.md`
- `DEPLOY.md` (domain alias section)
- `state/TODO.md`

## Grok bots

- Status: optional; not invoked this iteration.

## Next Command

```text
git pull origin main
# User: WebSupport panel → nephroctor.sk and nephroctor.eu as domain aliases of nephroctor.com (not HTTP redirect)
powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1
# Prefer real functional/security/a11y bug next; root apple-touch icons done
```
