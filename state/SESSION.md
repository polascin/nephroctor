# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 22)

## HEAD

See latest commit on `origin/main` after iter-22 push (skip-link focus target).

## Latest handoff

`.codex/handoffs/2026-11-06-022505-nephroctor-loop-iter-21.md` (superseded by iter-22 handoff after deploy)

## Just completed

Iter 22: WCAG 2.4.1 skip-link fix. `<main id="main">` lacked `tabindex="-1"`, so keyboard focus often stayed on the skip link after activation. Added `tabindex="-1"` on home + all legal pages, `#main:focus { outline: none }`, accessibility statement 1.6, structure audit assert. Skipped `.sk`/`.eu` panel and EN legal redirects. Noted prod `/impressum` still 404 (optional next).

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Or `/impressum` (+ `/legal/impressum.html`) 301 to `pravne-informacie.html` (DE parallel of `/imprint`). Or local SFTP deploy if hosting credentials become available.

## Deploys this session

- Prior: iter-21 Deploy success (`28b0f20`)
- Iter 22: see handoff after push
