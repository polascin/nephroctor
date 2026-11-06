# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 25)

## HEAD

See latest commit on `origin/main` after iter-25 push (Clarity Tab trap on dialog container).

## Latest handoff

`.codex/handoffs/2026-11-06-034957-nephroctor-loop-iter-25.md`

## Just completed

Iter 25: Clarity consent Tab/Shift+Tab trap now treats dialog-container focus and escaped focus as trap edges, so first-run Shift+Tab no longer leaves the modal. Cache-bust `?v=e1bbfa3bf0ab`. Accessibility statement 1.8. Skipped `.sk`/`.eu` panel.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional/security/a11y bug if found (optional: root `/apple-touch-icon.png` 404 like favicon root copy). Or local SFTP deploy if hosting credentials become available.

## Deploys this session

- Prior: iter-24 Deploy success (`b98fa42`)
- Iter 25: Deploy success (`9064941`, run 42151628402); Smoke + security headers OK
