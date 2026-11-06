# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 18)

## HEAD

See latest commit on `origin/main` after iter-18 push.

## Latest handoff

`.codex/handoffs/` – iter-18 handoff written at end of this iteration.

## Just completed

Iter 18: regression from iter-17 theme-color collapse. Without an explicit `nephroctor-theme`, bootstrap promoted OS dark into `data-theme="dark"` (locking the page) and the single meta without `media` no longer tracked live OS changes. Fix: set `data-theme` only for stored light/dark; `matchMedia` `change` listener refreshes icon + theme-color when following system; storage clear no longer re-locks dark. Skipped `.sk`/`.eu` panel and EN legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional bug (e.g. cross-tab `nephroctor-lang` sync) over further EN redirect aliases. Or local SFTP deploy if hosting credentials become available on this machine.

## Deploys this session

- Prior: iter-17 Deploy success (`83bac1e`)
- Iter 18: see handoff after push
