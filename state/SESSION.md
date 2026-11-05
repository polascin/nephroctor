# SESSION – Nephroctor improvement loop

Last updated: 2026-11-05 (loop iter 4)

## HEAD

Pending commit for CSS/JS revalidation + Clarity smoke markers (after `0e3f3fc`).

## Latest handoff

`.codex/handoffs/2026-11-05-201442-nephroctor-loop-iter-3.md` (iter 4 handoff follows deploy).

## Just completed

Iter 3 Clarity CSP done (0 violations). Iter 4: stop day-long stale Clarity CSS/JS after deploy — `.htaccess` no-cache/must-revalidate for html|css|js; propagate script query to consent CSS; smoke body markers for Clarity assets.

## Next iteration priority

WebSupport panel: `nephroctor.sk` / `.eu` domain alias (path-preserving) instead of upstream 302 that drops path. Or local SFTP deploy replacement if hosting access becomes available.

## Deploys this session

- https://github.com/polascin/nephroctor/actions/runs/42092187784 success (`728af04`)
- https://github.com/polascin/nephroctor/actions/runs/42094228783 (`0e3f3fc` handoff; verify after smoke)
