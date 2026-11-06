# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 28)

## HEAD

Pending commit: Clarity modal scroll lock (`setScrollLock` + overscroll-behavior).

## Latest handoff

`.codex/handoffs/2026-11-06-042015-nephroctor-loop-iter-27.md` (iter 28 handoff follows deploy)

## Just completed

Iter 28: lock document scroll while Clarity consent dialog is open (container focus still received Space/PageDown). Cache-bust `?v=2b163b588ee0`. Skipped `.sk`/`.eu` panel and legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional/security/a11y bug if found.

## Deploys this session

- Iter 26: Deploy success `5ca7810` (apple-touch)
- Iter 27: Deploy success `8494589` (manifest.webmanifest), run 42154902070
- Iter 28: Deploy pending (scroll lock)
