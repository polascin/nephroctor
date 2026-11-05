# SESSION – Nephroctor improvement loop

Last updated: 2026-11-05 (loop iter 14)

## HEAD

See latest commit on `origin/main` after iter-14 push.

## Latest handoff

`.codex/handoffs/` – iter-14 handoff written at end of this iteration.

## Just completed

Iter 14: skipped alias verify (panel still open). In-repo: `/imprint` and `/legal/imprint.html` 301 → `/legal/pravne-informacie.html`; `/cookie-policy` and `/legal/cookie-policy.html` 301 → `/legal/cookies.html` (query `?lang=en` preserved). No higher-severity in-repo bug found.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional bug over further EN redirect aliases. Or local SFTP deploy if hosting credentials become available on this machine.

## Deploys this session

- Prior: iter-13 Deploy success (`1407eca`)
- Iter 14: see handoff after push
