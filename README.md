# Aanwezigheidslijsten combineren (Jadadde + Villa Max)

Voegt twee Kwandoo-aanwezigheidslijsten — Jadadde (speelplein) en Villa Max
(opvang) — automatisch samen tot één Excel-bestand met drie tabbladen.

## Installatie (eenmalig)

Je hebt Python 3 nodig en twee libraries:

```bash
pip install pdfplumber openpyxl
```

## Gebruik

Download de twee PDF-lijsten uit Kwandoo en draai:

```bash
python3 combineer_aanwezigheidslijsten.py lijst1.pdf lijst2.pdf -o resultaat.xlsx
```

Voorbeeld:

```bash
python3 combineer_aanwezigheidslijsten.py Jadadde_1-3juli.pdf VillaMax_1-3juli.pdf -o Gecombineerd_1-3juli.xlsx
```

- De **volgorde van de twee PDF's maakt niet uit** — het script herkent zelf
  welke Jadadde en welke Villa Max is.
- De **datums en dagkolommen worden uit de PDF gelezen**, dus titels en
  kolommen kloppen automatisch, ook voor een andere dag of periode.
- Met `-o` kies je de naam/locatie van het Excel-bestand. Laat je `-o` weg,
  dan heet het bestand `Gecombineerde_aanwezigheidslijst.xlsx`.

## Wat je krijgt

Een Excel met drie tabbladen:

1. **Gecombineerd (overlap)** — kinderen die op *beide* lijsten staan, met de
   kolommen van zowel Jadadde als Villa Max.
2. **Alleen Jadadde** — kinderen die enkel op het speelplein zijn ingeschreven.
3. **Alleen Villa Max** — kinderen die enkel in de opvang zijn ingeschreven.

In de terminal verschijnt ook een korte samenvatting (aantal namen per lijst en
de overlappende kinderen).

## Goed om te weten

- Namen worden slim gematcht: hoofdletters, accenten (Téo = Teo), naamvolgorde
  (Bruwier Arthur = Arthur Bruwier) en ruis zoals `(papa)` of `*` worden
  genegeerd bij het bepalen van de overlap.
- Het script gaat uit van deze twee specifieke activiteiten (Jadadde speelplein
  + Villa Max opvang); enkel de namen en datums variëren per keer.
