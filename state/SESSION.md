# SESSION – Nephroctor improvement loop

Last updated: 2026-11-05 (loop iter 5)

## HEAD

`9b163b5` on `origin/main` (iter-5 fix `6e87685` already deployed).

## Latest handoff

`.codex/handoffs/2026-11-05-211049-nephroctor-loop-iter-5.md`

## Just completed

Iter 4 cache/revalidate landed but Smoke failed on OpenResty-stale bare Clarity URLs. Iter 5: HTML `?v=ec7132f34a` + smoke `?v=$GITHUB_SHA`; Deploy `42098466229` success; production markers verified.

## Next iteration priority

WebSupport panel: `nephroctor.sk` / `.eu` domain alias (path-preserving) instead of upstream 302 that drops path. Or local SFTP deploy replacement if hosting access becomes available.

## Deploys this session

- https://github.com/polascin/nephroctor/actions/runs/42095934437 failure (`eb74479`)
- https://github.com/polascin/nephroctor/actions/runs/42098123693 success (`8b12f39`)
- https://github.com/polascin/nephroctor/actions/runs/42098466229 success (`6e87685`; Smoke + security headers)
