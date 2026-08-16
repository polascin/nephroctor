# nephroctor.com

Statická viacjazyčná prezentačná stránka živnostníka **MUDr. Ľubomír Polaščín – Nephroctor**.

Čistý HTML5 + CSS3 + vanilla JavaScript. Bez frameworku, bez backendu, bez databázy
a **bez jedinej požiadavky na tretiu stranu** — všetky písma, obrázky a skripty sa
načítavajú z vlastnej domény.

## Štruktúra

```text
index.html            hlavná stránka, obsah v 24 jazykoch EÚ prepínaný na klientovi
legal/                6 právnych dokumentov, každý v slovenčine a angličtine
  ochrana-osobnych-udajov.html   zásady spracúvania osobných údajov (GDPR čl. 13/14)
  cookies.html                   cookies a lokálne úložisko
  podmienky-pouzivania.html      podmienky používania
  pravne-informacie.html         identifikácia poskytovateľa, orgán dozoru, ARS
  pristupnost.html               vyhlásenie o prístupnosti (WCAG 2.1 AA)
  zdravotne-upozornenie.html     zdravotné upozornenie (medical disclaimer)
assets/
  site.css            spoločný štýl pre index aj právne dokumenty (jediný zdroj pravdy)
  legal.js            prepínač témy a SK/EN pre právne dokumenty
  fonts/              Inter (variable, 6 subsetov), hosťované lokálne — SIL OFL 1.1
  logo.*              logo v PNG a WebP
  favicon.*, icon-*   favicony a ikony aplikácie odvodené z monogramu loga
  og-image.jpg        náhľad pre sociálne siete (1200 × 630)
favicon.ico           koreňová kópia (prehliadače ju žiadajú implicitne)
robots.txt            pravidlá pre crawlery + odkaz na sitemapu
sitemap.xml           sitemapa s hreflang alternatívami pre 24 jazykov
site.webmanifest      webový manifest
.htaccess             bezpečnostné hlavičky, HTTPS redirect, cache, kompresia
```

## Jazyky

24 úradných jazykov EÚ: `sk` `cs` `en` `de` `fr` `es` `it` `pt` `nl` `pl` `hu` `ro`
`bg` `hr` `sl` `da` `sv` `fi` `et` `lv` `lt` `el` `ga` `mt`.

Jazyk sa vyberá v poradí **`?lang=` v URL → uložená voľba → jazyk prehliadača → slovenčina**.
Pri prepnutí sa mení nielen obsah, ale aj `<title>`, meta description, Open Graph,
`og:locale`, kanonická URL a atribút `lang`. Každý jazyk má stabilnú adresu
`https://nephroctor.com/?lang=XX` uvedenú v `hreflang` alternatívach.

Právne dokumenty existujú v slovenčine a angličtine; **záväzná je slovenská verzia**.

## Nasadenie

Push do `main` spustí GitHub Actions workflow, ktorý nahrá stránku cez SFTP
na WebSupport a overí ju. Podrobnosti v [DEPLOY.md](DEPLOY.md).

## Audit

Stránka prechádza opakovaným hĺbkovým auditom. Kontrolný zoznam, pravidlá a
záznamy jednotlivých behov sú v [`.audit.md`](.audit.md); postup pre ďalší beh
je v [`.doaudit.md`](.doaudit.md).

## Licencie

- Kód a obsah stránky — pozri [LICENSE](LICENSE).
- Písmo Inter © The Inter Project Authors, SIL Open Font License 1.1
  (pozri [`assets/fonts/NOTICE.txt`](assets/fonts/NOTICE.txt)).
