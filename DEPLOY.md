# Nasadenie na WebSupport (nephroctor.com)

## Ako to funguje

Pri každom push do vetvy `main` (alebo manuálnom spustení) sa automaticky spustí
GitHub Actions workflow, ktorý:

1. Pripraví iba produkčné súbory (`index.html`, `assets/`)
2. Nahrá ich cez SFTP na WebSupport hosting
3. Overí, že stránka vracia HTTP 200

## Nastavenie GitHub Secrets

V repozitári `polascin/nephroctor` choďte do:
**Settings → Secrets and variables → Actions → New repository secret**

Pridajte tieto tajomstvá:

| Secret            | Popis                                           | Príklad                    |
| ----------------- | ----------------------------------------------- | -------------------------- |
| `SFTP_HOST`       | SFTP server (z WebSupport panelu)               | `wXXXX.websupport.sk`     |
| `SFTP_USER`       | SFTP používateľ                                 | `nephroctor`               |
| `SFTP_PASSWORD`   | SFTP heslo                                      | (vaše heslo)               |
| `SFTP_PORT`       | Port (zvyčajne 22 pre SFTP)                     | `22`                       |
| `SFTP_REMOTE_PATH`| Cieľový adresár na serveri                      | `/web`                     |

### Kde nájdem SFTP údaje na WebSupport?

1. Prihláste sa do [WebSupport panelu](https://admin.websupport.sk/)
2. Zvoľte hosting pre nephroctor.com
3. Sekcia **FTP účty** — tam nájdete host, používateľa a môžete nastaviť heslo
4. Cieľový adresár je zvyčajne `/web` (koreň webu)

## Manuálne spustenie deployu

Ak chcete nasadiť bez push:
1. Choďte do **Actions** v GitHub repozitári
2. Zvoľte workflow „Deploy to WebSupport"
3. Kliknite **Run workflow** → **Run workflow**

## Čo sa nasadzuje

Iba tieto súbory:
- `index.html` — hlavná stránka
- `assets/logo.png` — logo (biele pozadie)
- `assets/logo-transparent.png` — logo (priehľadné pozadie)

Ostatné súbory (`.github/`, `.audit.md`, `LICENSE`, `README.md` atď.) sa na server **nenahrávajú**.

## Overenie po nasadení

Po úspešnom deployi overte:
- https://nephroctor.com/ — vracia 200
- Logo sa zobrazuje
- Prepínanie 24 jazykov funguje
