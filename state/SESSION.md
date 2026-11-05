# SESSION – Nephroctor improvement loop

Last updated: 2026-11-05 (loop iter 5)

## HEAD

Pending: versioned Clarity asset URLs + smoke edge-cache bust (after failed `eb74479` deploy).

## Latest handoff

`.codex/handoffs/2026-11-05-201442-nephroctor-loop-iter-3.md` (iter 4 landed as `eb74479` but Deploy smoke failed; iter 5 handoff after this deploy).

## Just completed

Iter 4 SFTP uploaded new Clarity assets and `.htaccess` revalidation, but OpenResty kept bare `/assets/clarity-consent.*` at prior `max-age=86400` bodies, so marker smoke failed. Iter 5: HTML `?v=ec7132f34a` (content hash) on consent script; smoke requests `?v=$GITHUB_SHA`.

## Next iteration priority

WebSupport panel: `nephroctor.sk` / `.eu` domain alias (path-preserving) instead of upstream 302 that drops path. Or local SFTP deploy replacement if hosting access becomes available.

## Deploys this session

- https://github.com/polascin/nephroctor/actions/runs/42092187784 success (`728af04`)
- https://github.com/polascin/nephroctor/actions/runs/42094228783 success (`0e3f3fc`)
- https://github.com/polascin/nephroctor/actions/runs/42095934437 **failure** (`eb74479` smoke markers / stale edge)
