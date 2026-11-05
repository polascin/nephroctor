# SESSION – Nephroctor improvement loop

Last updated: 2026-11-05 (loop iter 6)

## HEAD

See latest commit on `origin/main` after iter-6 push.

## Latest handoff

`.codex/handoffs/` – iter-6 handoff written at end of this iteration.

## Just completed

Iter 6: confirmed `.sk`/`.eu` still OpenResty 302 path-drop; SSH `websupport` has no nephroctor.com webroot. In-repo: consent dialog `inert` + privacy fallback + WAF-lighter Smoke + panel alias docs/`tools/verify-domain-aliases.ps1`.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Or local SFTP deploy if hosting credentials become available on this machine.

## Deploys this session

- Prior: `42098466229` success (`6e87685`)
- Iter 6: see handoff after push
