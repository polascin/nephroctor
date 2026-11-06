# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 27, after killed iter-26 shell)

## HEAD

See latest commit on `origin/main` after iter-27 push (root `manifest.webmanifest`).

## Latest handoff

`.codex/handoffs/` – iter-27 after completing stub iter-26 handoff.

## Just completed

Iter 26 verified live after loop kill: root apple-touch icons `5ca7810`, Deploy success, prod 200 PNG.
Iter 27: root `/manifest.webmanifest` byte-identical to `site.webmanifest` (common probe was 404). Skipped `.sk`/`.eu` panel and legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional/security/a11y bug if found. Or local SFTP deploy if hosting credentials become available.

## Deploys this session

- Iter 26: Deploy success `5ca7810` (apple-touch); handoff stub completed after kill
- Iter 27: Deploy after root `manifest.webmanifest`
