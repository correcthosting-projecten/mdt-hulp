#!/usr/bin/env python3
"""MD Tradingsystems Hulp: zet onze server, sleutels, naam en iconen in de RustDesk-bron.

Draait in GitHub Actions direct na het uitchecken (met submodules), vóór de build. Elke
vervanging moet precies zo vaak voorkomen als verwacht; anders stopt het script met een fout,
zodat een nieuwe RustDesk-versie nooit stilzwijgend een half aangepaste app oplevert.
Lokaal testen: `python3 mdt-hulp/patch.py` in een verse checkout van de tag (met hbb_common).
"""
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HIER = pathlib.Path(__file__).resolve().parent

APP_NAAM = 'MD Tradingsystems Hulp'
BEDRIJF = 'MD Tradingsystems'
SERVER = 'hulp.correcthosting.nl'
# Publieke sleutel van hbbs op hulp.correcthosting.nl (id_ed25519.pub).
SERVER_SLEUTEL = '8eKUABvoygDLjnEENYiFRxLD71il4qSu04ls+wYhstA='
# Publieke sleutel waarmee custom.txt is ondertekend (privésleutel staat alleen op de jump).
CONFIG_SLEUTEL = 'ipHCaB0XiW4aub2OmLPhv17T4fVA7aQxj4kUxsgonxw='


def vervang(pad, vervangingen):
    bestand = ROOT / pad
    tekst = bestand.read_text(encoding='utf-8')
    for oud, nieuw, aantal in vervangingen:
        gevonden = tekst.count(oud)
        if gevonden != aantal:
            sys.exit(f'{pad}: verwacht {aantal}x, gevonden {gevonden}x: {oud!r}')
        tekst = tekst.replace(oud, nieuw)
    bestand.write_text(tekst, encoding='utf-8')
    print(f'aangepast: {pad}')


def taalbestand(pad, eigen_teksten):
    """Vervangt RustDesk alleen in de vertaling (rechterkant), nooit in de sleutel waarop de code zoekt."""
    bestand = ROOT / pad
    regels = bestand.read_text(encoding='utf-8').split('\n')
    patroon = re.compile(r'^(\s*\(")(.*?)(", ")(.*)("\),?\s*)$')
    nog_te_doen = dict(eigen_teksten)
    for i, regel in enumerate(regels):
        m = patroon.match(regel)
        if not m:
            continue
        sleutel, waarde = m.group(2), m.group(4)
        if sleutel in nog_te_doen:
            waarde = nog_te_doen.pop(sleutel)
        elif sleutel != 'powered_by_me':  # credit aan RustDesk laten staan
            waarde = waarde.replace('RustDesk', APP_NAAM)
        regels[i] = m.group(1) + sleutel + m.group(3) + waarde + m.group(5)
    if nog_te_doen:
        sys.exit(f'{pad}: sleutels niet gevonden: {sorted(nog_te_doen)}')
    bestand.write_text('\n'.join(regels), encoding='utf-8')
    print(f'aangepast: {pad}')


vervang('libs/hbb_common/src/config.rs', [
    ('pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];',
     f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{SERVER}"];', 1),
    ('pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";',
     f'pub const RS_PUB_KEY: &str = "{SERVER_SLEUTEL}";', 1),
])
vervang('src/common.rs', [
    ('const KEY: &str = "5Qbwsde3unUcJBtrx9ZkvUmwFNoExHzpryHuPUdqlWM=";',
     f'const KEY: &str = "{CONFIG_SLEUTEL}";', 1),
])
for cargo in ('Cargo.toml', 'libs/portable/Cargo.toml'):
    vervang(cargo, [
        ('description = "RustDesk Remote Desktop"', f'description = "{APP_NAAM}"', 1),
        ('ProductName = "RustDesk"', f'ProductName = "{APP_NAAM}"', 1),
        ('OriginalFilename = "rustdesk.exe"', 'OriginalFilename = "MD-Tradingsystems-Hulp.exe"', 1),
        # Taakbeheer en de UAC-vraag tonen de FileDescription als programmanaam.
        ('FileDescription = "RustDesk Remote Desktop"', f'FileDescription = "{APP_NAAM}"', 1),
    ])
vervang('flutter/windows/runner/Runner.rc', [
    ('VALUE "CompanyName", "Purslane Tech Pte. Ltd." "\\0"', f'VALUE "CompanyName", "{BEDRIJF}" "\\0"', 1),
    ('VALUE "FileDescription", "RustDesk Remote Desktop" "\\0"', f'VALUE "FileDescription", "{APP_NAAM}" "\\0"', 1),
    ('VALUE "ProductName", "RustDesk" "\\0"', f'VALUE "ProductName", "{APP_NAAM}" "\\0"', 1),
])

taalbestand('src/lang/nl.rs', {
    'config_acc': f'Om uw computer op afstand te kunnen bedienen, moet u {APP_NAAM} toestemming geven voor Toegankelijkheid.',
    'config_screen': f'Om met u mee te kunnen kijken, moet u {APP_NAAM} toestemming geven voor Schermopname.',
})
taalbestand('src/lang/en.rs', {})

iconen = HIER / 'iconen'
for bron, doelen in {
    'icon.ico': ['res/icon.ico', 'flutter/windows/runner/resources/app_icon.ico'],
    'tray-icon.ico': ['res/tray-icon.ico'],
    'png-512.png': ['res/icon.png', 'res/mac-icon.png'],
    'png-32.png': ['res/32x32.png'],
    'png-64.png': ['res/64x64.png'],
    'png-128.png': ['res/128x128.png'],
    'png-256.png': ['res/128x128@2x.png'],
    'AppIcon.icns': ['flutter/macos/Runner/AppIcon.icns'],
    'icon.svg': ['flutter/assets/icon.svg'],
}.items():
    for doel in doelen:
        if not (ROOT / doel).exists():
            sys.exit(f'icoon-doel bestaat niet (andere RustDesk-indeling?): {doel}')
        shutil.copyfile(iconen / bron, ROOT / doel)
print('iconen vervangen')
print('klaar: MD Tradingsystems Hulp-aanpassingen toegepast')
