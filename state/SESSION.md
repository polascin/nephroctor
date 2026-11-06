# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 21)

## HEAD

See latest commit on `origin/main` after iter-21 push (SEO/meta polish).

## Latest handoff

`.codex/handoffs/` – iter-21 handoff written at end of this iteration.

## Just completed

Iter 21: SEO/meta hardening on home: `twitter:image:alt` (matches `og:image:alt`); static 23× `og:locale:alternate` for every non-primary locale; `site.webmanifest` `theme_color` reconciled to `#f8fafc` (same as `background_color` / light HTML `theme-color`). Audits extended in `check_i18n.py` + `check_assets.py`. Skipped `.sk`/`.eu` panel and EN legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer another real functional bug (fonts, contrast, broken scripts) or a full Beh doaudit. Or local SFTP deploy if hosting credentials become available on this machine.

## Deploys this session

- Prior: iter-20 Deploy success (`3b97b0f`)
- Iter 21: see handoff after push
