# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 19)

## HEAD

See latest commit on `origin/main` after iter-19 push (`52fac8c` fix + docs handoff).

## Latest handoff

`.codex/handoffs/` – iter-19 handoff written at end of this iteration.

## Just completed

Iter 19: cross-tab sync for `nephroctor-lang`. Home `storage` listener calls `switchLang` for valid codes; legal maps site languages to SK/EN via `resolveDocLang`, announces, and does not collapse richer codes (e.g. `de`) when syncing. Legal SK/EN clicks persist `nephroctor-lang`. Skipped `.sk`/`.eu` panel and EN legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional bug over further EN redirect aliases. Or local SFTP deploy if hosting credentials become available on this machine.

## Deploys this session

- Prior: iter-18 Deploy success (`7f4a761`)
- Iter 19: see handoff after push
