# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 29)

## HEAD

`bce92c3` on `origin/main` (Clarity dialog self-scroll).

## Latest handoff

`.codex/handoffs/2026-11-06-050030-nephroctor-loop-iter-29.md`

## Just completed

Iter 29: make Clarity consent dialog self-scroll on every viewport width so Allow/Decline stay reachable after document scroll lock. Cache-bust `?v=78331b7675cf`. Deploy success run 42158860197. Skipped `.sk`/`.eu` panel and legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional/security/a11y bug if found.

## Deploys this session

- Iter 26: Deploy success `5ca7810` (apple-touch)
- Iter 27: Deploy success `8494589` (manifest.webmanifest), run 42154902070
- Iter 28: Deploy success `51499e6` (scroll lock), run 42157205770
- Iter 29: Deploy success `bce92c3` (dialog self-scroll), run 42158860197
