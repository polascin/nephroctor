# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 30)

## HEAD

Pending commit for root `favicon.svg` + `browserconfig.xml` (iter 30).

## Latest handoff

`.codex/handoffs/2026-11-06-050030-nephroctor-loop-iter-29.md` (iter 29); iter 30 handoff after deploy.

## Just completed

Iter 30: ship root `/favicon.svg` (dark-scheme monogram) and `/browserconfig.xml` after confirmed prod 404s; no higher-severity bug found. Skipped `.sk`/`.eu` panel and legal redirects.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional/security/a11y bug if found. Remaining optional low: root `/android-chrome-*.png` probes if still 404.

## Deploys this session

- Iter 26: Deploy success `5ca7810` (apple-touch)
- Iter 27: Deploy success `8494589` (manifest.webmanifest), run 42154902070
- Iter 28: Deploy success `51499e6` (scroll lock), run 42157205770
- Iter 29: Deploy success `bce92c3` (dialog self-scroll), run 42158860197
- Iter 30: pending after push
