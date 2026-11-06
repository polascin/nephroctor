# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 26)

## HEAD

See latest commit on `origin/main` after iter-26 push (root apple-touch icons).

## Latest handoff

`.codex/handoffs/2026-11-06-040502-nephroctor-loop-iter-26.md`

## Just completed

Iter 26: root `/apple-touch-icon.png` and `/apple-touch-icon-precomposed.png` copied from `assets/` (byte-identical), deploy payload + `check_assets` asserts. No higher-severity bug found; skipped `.sk`/`.eu` panel.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional/security/a11y bug if found. Or local SFTP deploy if hosting credentials become available.

## Deploys this session

- Prior: iter-25 Deploy success (`9064941`)
- Iter 26: Deploy after root apple-touch icon fix
