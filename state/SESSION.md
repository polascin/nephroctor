# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 17)

## HEAD

See latest commit on `origin/main` after iter-17 push.

## Latest handoff

`.codex/handoffs/` – iter-17 handoff written at end of this iteration.

## Just completed

Iter 17: full `.audit/*` + `test_clarity.cjs` + new `check_theme_logic.js` green. Real bug: `theme-color` followed OS `prefers-color-scheme` media metas while the page theme uses `data-theme` / `nephroctor-theme`, so browser chrome stayed wrong after an explicit toggle; theme also did not sync across tabs. Fixed bootstrap + toggle `syncThemeColor` and `storage` listener on index and legal. Skipped `.sk`/`.eu` panel and further EN legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional bug over further EN redirect aliases. Or local SFTP deploy if hosting credentials become available on this machine.

## Deploys this session

- Prior: iter-16 Deploy success (`5594332`)
- Iter 17: see handoff after push
