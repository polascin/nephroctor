# SESSION – Nephroctor improvement loop

Last updated: 2026-11-06 (loop iter 24)

## HEAD

See latest commit on `origin/main` after iter-24 push (Clarity inert vs aria-live).

## Latest handoff

`.codex/handoffs/2026-11-06-030329-nephroctor-loop-iter-23.md` (superseded by iter-24 handoff after docs commit)

## Just completed

Iter 24: Clarity consent `setBackgroundInert` no longer marks `role="status"` / `aria-live` regions inert, so polite announces stay available while the dialog is open. Cache-bust `?v=62105992024e`. Accessibility statement 1.7. Skipped `.sk`/`.eu` panel.

## Next iteration priority

WebSupport panel (user): switch `nephroctor.sk` / `.eu` from HTTP redirect to domain alias of `nephroctor.com`, then run `tools/verify-domain-aliases.ps1`. Prefer a real functional/security/a11y bug if found. Or local SFTP deploy if hosting credentials become available.

## Deploys this session

- Prior: iter-23 Deploy success (`ae4b0e6`)
- Iter 24: Deploy pending after push
