---
name: kolme-lovable-prompt
description: Genereert een volledige, sectorspecifieke Lovable prompt voor een Kolme klantsite. Neemt het ingevulde briefingdocument van skill kolme-intake als input en levert een prompt in het Engels (Lovable werkt beter in het Engels). De prompt is altijd authentiek aan de klant, nooit een generieke template met een naam erin. Trigger bij woorden als Lovable prompt, site bouwen, prompt schrijven, klant in Lovable zetten.
---

# Kolme Lovable Prompt

## Wat deze skill doet

Deze skill zet een ingevulde briefing om in één complete Lovable prompt in het Engels. Die prompt bevat alles: techniek, structuur, secties, copy-richtlijnen, kleuren, footer met juridische pagina's en een cookiebanner. Je plakt de prompt in Lovable en krijgt een site die klopt voor deze specifieke klant in deze specifieke sector.

Lovable werkt beter in het Engels, dus de prompt is altijd in het Engels. De zichtbare website-copy die je in de prompt vraagt is in het Nederlands (of NL+EN als de briefing dat zegt).

## Input

Het bestand `Briefing.md` uit `OneDrive/Kolme/Klanten/[Klantnaam]/`, output van skill kolme-intake. Lees de hele briefing voor je begint. Geen volledige briefing betekent terug naar skill 1.

## Hoe je werkt

1. **Lees de briefing.** Haal eruit: sector, pakket, doelactie, toon, taal, trustbuilders, foto's, het unieke verkooppunt.

2. **Bepaal onepager of multipage** met de beslisboom in `references/prompt-architectuur.md`.

3. **Kies het kleurenpalet** uit `references/sectorpaletten.md` (sectorstandaard of klantspecifiek uit de briefing).

4. **Kies de secties en hun volgorde** uit `references/sectie-templates.md` voor deze sector.

5. **Pas de copy-regels toe** uit `references/copy-regels.md`. De hero komt uit het unieke punt van de klant, niet uit een template.

6. **Voeg de footer en juridische pagina's toe** met `references/av-pv-cookie-templates.md`. Vul de placeholders in met de gegevens uit de briefing.

7. **Schrijf de volledige prompt in het Engels** volgens de vaste architectuur. Eén blok dat de klant kan kopiëren.

## Output

Eén Lovable prompt in het Engels, klaar om te plakken. Authentiek aan de klant: de zaaksnaam, het verhaal, de specialiteiten en het unieke punt zitten verwerkt in de copy, niet als losse variabelen.

## Gouden regel

Een prompt die werkt voor twee verschillende klanten is een slechte prompt. Lees iemand de hero voor zonder de naam te noemen en de klant moet zichzelf herkennen. Lukt dat niet, dan is de prompt te generiek.

## Referentiebestanden

- `references/prompt-architectuur.md` — vaste basisstructuur van elke prompt
- `references/sectorpaletten.md` — kleurpaletten per sector met hex-codes
- `references/sectie-templates.md` — secties, hero's, trustbars, formuliervelden per sector
- `references/copy-regels.md` — copy-principes die in elke prompt zitten
- `references/av-pv-cookie-templates.md` — AV, PV en cookiebeleid met placeholders
