# Nasadenie na WebSupport (nephroctor.com)

## Ako to funguje

Pri každom push do vetvy `main` (alebo manuálnom spustení) sa automaticky spustí
GitHub Actions workflow, ktorý:

1. Pripraví produkčné súbory do adresára `deploy/`
2. Overí, že v payloade nechýba žiadny kritický súbor (krok „Verify deploy payload“)
3. Nahrá ich cez SFTP na WebSupport hosting (`mirror --reverse --delete`)
4. Overí, že všetky kľúčové adresy vracajú HTTP 200
5. Vypíše bezpečnostné hlavičky, ktoré server skutočne posiela

## Nastavenie GitHub Secrets

V repozitári `polascin/nephroctor` choďte do:
**Settings → Secrets and variables → Actions → New repository secret**

Pridajte tieto tajomstvá:

| Secret             | Popis                             | Príklad               |
| ------------------ | --------------------------------- | --------------------- |
| `SFTP_HOST`        | SFTP server (z WebSupport panelu) | `wXXXX.websupport.sk` |
| `SFTP_USER`        | SFTP používateľ                   | `nephroctor`          |
| `SFTP_PASSWORD`    | SFTP heslo                        | (vaše heslo)          |
| `SFTP_PORT`        | Port (zvyčajne 22 pre SFTP)       | `22`                  |
| `SFTP_REMOTE_PATH` | Cieľový adresár na serveri        | `/web`                |

### Kde nájdem SFTP údaje na WebSupport?

1. Prihláste sa do [WebSupport panelu](https://admin.websupport.sk/)
2. Zvoľte hosting pre nephroctor.com
3. Sekcia **FTP účty** — tam nájdete host, používateľa a môžete nastaviť heslo
4. Cieľový adresár je zvyčajne `/web` (koreň webu)

## Manuálne spustenie deployu

Ak chcete nasadiť bez push:

1. Choďte do **Actions** v GitHub repozitári
2. Zvoľte workflow „Deploy to WebSupport“
3. Kliknite **Run workflow** → **Run workflow**

## Čo sa nasadzuje

| Cesta              | Obsah                                                               |
| ------------------ | ------------------------------------------------------------------- |
| `index.html`       | hlavná stránka (24 jazykov, prepínané na klientovi)                 |
| `legal/`           | 6 právnych dokumentov (SK + EN)                                     |
| `assets/`          | logá, favicony, ikony, OG obrázok, `site.css`, `legal.js`, `fonts/` |
| `favicon.ico`      | koreňový favicon (prehliadače ho žiadajú implicitne)                |
| `apple-touch-icon.png` | koreňová kópia (iOS home screen / implicitná požiadavka)        |
| `apple-touch-icon-precomposed.png` | koreňová kópia (staršie iOS)                        |
| `robots.txt`       | pravidlá pre crawlery + odkaz na sitemapu                           |
| `sitemap.xml`      | sitemapa s `hreflang` alternatívami                                 |
| `site.webmanifest` | webový manifest (názov, ikony, farby)                               |
| `.htaccess`        | bezpečnostné hlavičky, HTTPS redirect, cache, kompresia             |

Ostatné súbory (`.github/`, `.audit.md`, `.doaudit.md`, `.trunk/`, `LICENSE`,
`README.md`, `DEPLOY.md`) sa na server **nenahrávajú** — zoznam je v `.deployignore`.

> **Pozor:** workflow používa `mirror --reverse --delete`. Súbory, ktoré na serveri
> existujú a v `deploy/` nie sú, budú **zmazané**. Ak niečo nahrávate na server ručne,
> pridajte to do repozitára aj do kroku „Prepare deploy directory“.

## Overenie po nasadení

Workflow overuje automaticky. Ručne skontrolujte:

- <https://nephroctor.com/> — vracia 200, logo sa zobrazuje, favicon je v záložke
- Prepínanie 24 jazykov + zmena `<title>` a meta description pri prepnutí
- `?lang=de`, `?lang=el`, `?lang=bg` — zobrazia sa správne jazyky vrátane gréčtiny a cyriliky
- Všetkých 6 dokumentov v `legal/` a prepínač SK/EN v nich
- Tmavý/svetlý režim a jeho zapamätanie po obnovení stránky

### Bezpečnostné hlavičky

Krok „Report security headers“ vypíše hlavičky, ktoré server naozaj vracia.
Ak sa nevypíše nič, hosting pravdepodobne ignoruje `.htaccess` (`AllowOverride None`).
V takom prípade treba hlavičky nastaviť v paneli WebSupport alebo požiadať podporu.
Stránka funguje aj bez nich, ale prichádza o CSP, HSTS a ochranu proti clickjackingu.

### Poznámka k smoke checku

Bot-ochrana hostingu odpovedá na požiadavky bez prehliadačového `User-Agent`
kódom **HTTP 466**. Workflow preto posiela plnohodnotný `User-Agent` — bez neho by
kontrola padala aj pri úplne funkčnej stránke. Actions IP často dostávajú HTTP 429;
Smoke preto používa malú sadu kritických HTML ciest, backoff a pri vyčerpaní 429/466
nefailuje Deploy (payload už bol nahratý).

## Doménové aliasy nephroctor.sk a nephroctor.eu (panel WebSupport)

`.htaccess` už obsahuje path-preserving **301** (napr. `/privacy` →
`/legal/ochrana-osobnych-udajov.html`, `/accessibility` a `/legal/accessibility.html` →
`/legal/pristupnost.html`, `/imprint` / `/impressum` a `/legal/imprint.html` /
`/legal/impressum.html` → `/legal/pravne-informacie.html`, `/cookie-policy` a
`/legal/cookie-policy.html` → `/legal/cookies.html`, `/health-notice` /
`/disclaimer` / `/zdravotne-upozornenie` →
`/legal/zdravotne-upozornenie.html` na `https://nephroctor.com`). Dnes však
OpenResty na hostingu ešte pred Apache odpovedá **302** na
`https://nephroctor.com` **bez cesty** (path drop). To sa z repozitária ani cez
SSH alias `websupport` (účet polascin.net, nie nephroctor.com) nedá zmeniť.

### Presné kroky v zákazníckom paneli

1. Prihláste sa do [admin.websupport.sk](https://admin.websupport.sk/).
2. Otvorte hosting / službu viazanú na **nephroctor.com** (nie iný web v tom istom
   zákazníckom účte).
3. Pre každú z domén **nephroctor.sk** a **nephroctor.eu** (aj `www.` ak sú samostatne):
   - Ak je nastavené **Presmerovanie webu** / HTTP redirect na `https://nephroctor.com`,
     **vypnite** ho.
   - Nastavte **Doménový alias** (parkovanie / alias na ten istý webpriestor ako
     nephroctor.com), nie HTTP redirect. Alias musí smerovať na ten istý document root
     (`/web` alebo ekvivalent), kde beží `.htaccess` z tohto repozitára.
4. Počkajte na propagáciu DNS/SSL (minúty až desiatky minút; HTTPS certifikát pre
   alias môže panel vystaviť samostatne).
5. Overenie z lokálneho stroja (prehliadačový User-Agent je povinný):

```powershell
# Jednorazovo (alebo): powershell -NoProfile -ExecutionPolicy Bypass -File tools/verify-domain-aliases.ps1
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
curl.exe -sI -A $ua 'https://nephroctor.sk/privacy'
curl.exe -sI -A $ua 'https://nephroctor.eu/terms'
```

Očakávané po úspešnom aliasovaní: **HTTP 301** s
`Location: https://nephroctor.com/legal/ochrana-osobnych-udajov.html` (resp. terms),
jeden skok, cesta zachovaná. Stále **302** na holé `https://nephroctor.com` znamená,
že panel stále používa HTTP redirect namiesto aliasu.
