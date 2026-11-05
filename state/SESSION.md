# SESSION – Nephroctor improvement loop

Last updated: 2026-11-05 (loop iter 4 handoff; HEAD includes iter-5 `?v=` bust)

## HEAD

`6e87685` on `main` (iter 4: `eb74479` + `8b12f39`; iter 5 edge `?v=` on top).

## Latest handoff

`.codex/handoffs/2026-11-05-210600-nephroctor-loop-iter-4.md`

## Just completed

Iter 4: `.htaccess` CSS/JS revalidation; Clarity CSS inherits script query; Smoke body markers with identity encoding (`8b12f39`). Iter 5 (parallel): HTML `clarity-consent.js?v=ec7132f34a` + smoke `?v=$GITHUB_SHA` after OpenResty kept bare URLs on old TTL during `eb74479` smoke.

## Next iteration priority

WebSupport panel: `nephroctor.sk` / `.eu` domain alias (path-preserving) instead of upstream 302 that drops path. Or local SFTP deploy replacement if hosting access becomes available.

## Deploys this session

- https://github.com/polascin/nephroctor/actions/runs/42094228783 success (`0e3f3fc`)
- https://github.com/polascin/nephroctor/actions/runs/42095934437 failure (`eb74479`; gzip then/or edge stale)
- https://github.com/polascin/nephroctor/actions/runs/42098123693 success (`8b12f39`)
- https://github.com/polascin/nephroctor/actions/runs/42098466229 success (`6e87685`)
