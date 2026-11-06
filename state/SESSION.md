# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 27)

## HEAD

`8494589` on `origin/main` (root `manifest.webmanifest`).

## Latest handoff

`.codex/handoffs/2026-11-06-042015-nephroctor-loop-iter-27.md`

## Just completed

Iter 26 verified after loop kill (apple-touch live). Iter 27: root `/manifest.webmanifest` = `site.webmanifest`. Skipped `.sk`/`.eu` panel and legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional/security/a11y bug if found.

## Deploys this session

- Iter 26: Deploy success `5ca7810` (apple-touch)
- Iter 27: Deploy success `8494589` (manifest.webmanifest), run 42154902070
