# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 20)

## HEAD

See latest commit on `origin/main` after iter-20 push (home lang aria-live).

## Latest handoff

`.codex/handoffs/` – iter-20 handoff written at end of this iteration.

## Just completed

Iter 20: home-page language switch now announces via `aria-live="polite"` (autonym), matching legal docs and Clarity. Initial paint stays silent. Accessibility statement bumped to 1.5. Skipped `.sk`/`.eu` panel and EN legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer another real functional bug (SEO meta gaps such as `twitter:image:alt` / `og:locale:alternate`, manifest `theme_color` vs chrome, fonts/contrast regressions). Or local SFTP deploy if hosting credentials become available on this machine.

## Deploys this session

- Prior: iter-19 Deploy success (`52fac8c`)
- Iter 20: see handoff after push
