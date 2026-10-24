# MD Tradingsystems Hulp

Hulp op afstand voor klanten van MD Tradingsystems: de klant opent de app, klikt op **Accepteren**
als Dennis Fransen verbinding maakt, en Dennis kan meekijken en meehelpen. Alleen inkomend, niets
installeren, geen wachtwoord of nummer doorgeven.

Dit is een aangepaste build van [RustDesk](https://github.com/rustdesk/rustdesk) 1.5.0
(AGPL-3.0). Deze repository is de volledige broncode van die aangepaste versie.

*English: a branded, incoming-only build of RustDesk 1.5.0 that connects to our own server. Source
of the modified version is this repository; license AGPL-3.0, see [`LICENCE`](../LICENCE).*

## Wijzigingen ten opzichte van RustDesk 1.5.0 (24 oktober 2026)

- `patch.py` zet bij het bouwen:
  - de eigen ID-/relayserver `hulp.correcthosting.nl` en de publieke sleutel daarvan;
  - een eigen publieke sleutel voor het ondertekende instellingenbestand;
  - de naam "MD Tradingsystems Hulp" in de Windows-programma-info en de Nederlandse en Engelse
    teksten (de vermelding "Powered by RustDesk" blijft staan);
  - de MD-iconen uit `iconen/`.
- `custom.txt` (leesbaar: `custom.json`): ondertekende instellingen. Alleen inkomend, de klant
  accepteert met een klik, installeren en instellingen verborgen, geen terminal, camera, tunnel,
  printer, opname of updatemeldingen. De privésleutel staat niet in deze repository.
- `.github/workflows/flutter-build.yml` is ingekort tot Windows x64 en macOS (Intel + Apple
  Silicon), met de stappen hierboven. `mdt-hulp.yml` start de build en zet de downloads in een
  release. Op macOS heet de app "MD Tradingsystems Hulp", met bundle-id `nl.mdtradingsystems.hulp`.

## Bouwen

Actions → **MD Tradingsystems Hulp bouwen** → Run workflow. Na 1 à 2 uur staan de bestanden onder
Releases. Ze zijn nog niet ondertekend door Apple of Microsoft; dat volgt zodra de certificaten er
zijn.

## Lokaal controleren

In een verse checkout van tag `1.5.0` met `libs/hbb_common`: `python3 mdt-hulp/patch.py`. Het script
stopt met een fout als een vervanging niet precies één keer past (bijvoorbeeld na een update van
RustDesk).
