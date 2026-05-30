---
name: kolme-intake
description: Gestructureerde intake voor Kolme. Gebruik deze skill bij elk nieuw klantgesprek voordat er ook maar één regel code geschreven wordt. Damon doorloopt een vaste vragenlijst, vult het briefingdocument in en slaat dat op in OneDrive. De ingevulde briefing is rechtstreekse input voor de Lovable prompt skill (kolme-lovable-prompt). Trigger bij woorden als intake, nieuw klantgesprek, briefing, nieuwe klant, kennismaking, offerte voorbereiden.
---

# Kolme Intake

## Wat deze skill doet

Deze skill zorgt dat Damon bij elk nieuw klantgesprek dezelfde structuur volgt en niets vergeet. Het resultaat is een ingevuld briefingdocument dat de basis vormt voor alles wat daarna komt: de Lovable prompt, de copy, het design en de scope.

Geen briefing betekent geen bouw. Zo simpel is het. Een halve intake levert een halve site op en discussies achteraf.

## Wanneer gebruik je dit

- Bij elk eerste inhoudelijk gesprek met een nieuwe prospect of klant
- Voordat je een Lovable prompt schrijft
- Voordat je een scope of offerte opmaakt
- Wanneer een bestaande klant een grondige restyle wil (dan herdoe je de intake)

## Hoe je werkt

1. **Open `references/intake-vragen.md`** en loop de vragen door tijdens het gesprek. Dit is je leidraad, niet een formulier dat je voorleest. Praat als een mens, vink af in je hoofd of op papier.

2. **Check de sector in `references/sectoren.md`** en stel de sectorspecifieke aanvullingsvragen. Een kapsalon heeft andere info nodig dan een bouwbedrijf.

3. **Vul na het gesprek `references/briefing-template.md` in.** Doe dit meteen na het gesprek, niet drie dagen later als je de helft vergeten bent.

4. **Sla op** als `Briefing.md` in `OneDrive/Kolme/Klanten/[Klantnaam]/`. Dit pad is verplicht en consistent (zie skill kolme-klantdossier).

5. **Geef door aan skill 2** (kolme-lovable-prompt). De ingevulde briefing is de volledige input.

## Output

Eén bestand: `Briefing.md`, volledig ingevuld, opgeslagen op de juiste plek in OneDrive. Geen losse notities, geen halve velden. Wat je niet weet noteer je expliciet als "nog op te vragen" zodat het niet vergeten wordt.

## Belangrijke principes

- **Eerst luisteren, dan bouwen.** De klant kent zijn zaak beter dan jij. Jouw werk is de juiste vragen stellen.
- **Vraag door op het unieke.** "Wat maakt jullie anders dan de concurrent" is de belangrijkste vraag van het hele gesprek. Het antwoord daarop wordt je hero copy.
- **Vraag naar echte foto's.** Een site met echte foto's van de zaak verslaat elke stockfoto. Weet je dit nu, dan weet je meteen hoeveel werk de oplevering wordt.
- **Bepaal de doelactie.** Eén site, één hoofdactie. Bellen, boeken, offerte aanvragen of langskomen. Kies er één en bouw alles daarrond.
- **Noteer het pakket en de taalvereiste.** Dit bepaalt onepager versus multipage en of er een EN-toggle komt.

## Referentiebestanden

- `references/intake-vragen.md` — de volledige vragenlijst per categorie
- `references/briefing-template.md` — leeg invulformulier, output van het gesprek
- `references/sectoren.md` — sectorspecifieke aanvullingsvragen per type zaak
