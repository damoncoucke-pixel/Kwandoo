#!/usr/bin/env python3
"""Build Kwandoo_Kennisbank_v3.html — v3 production knowledge base.

Extends v2 with WCAG 2.1 AA accessibility, a Quick Start homepage,
Workflows tab, prominent Dangerous-Actions section, expanded Billing
and Reporting modules, breadcrumbs, back-to-top, Ctrl+K, and the
Ingelmunster colour palette (#2d7a3a / #1a3a6b).

Reuses modules.json + embedded PNG screenshots from the v2 builder.
"""
import base64
import json
import re
from pathlib import Path

data = json.loads(Path("modules.json").read_text(encoding="utf-8"))
modules = data["modules"]

# ---------------------------------------------------------------------------
# Extend the Billing module with the menu items that v2 didn't cover.
# ---------------------------------------------------------------------------
EXTRA_BILLING_SECTIONS = [
    {
        "id": "synchronisatie-bestanden",
        "title": "12. Synchronisatie bestanden",
        "content": (
            "Facturatie > Synchronisatie bestanden\n\n"
            "Functie: exporteert de boekhoudgegevens voor synchronisatie met "
            "het financieel systeem van de gemeente.\n\n"
            "Gebruik:\n"
            "• Enkel voor medewerkers met de rol 'Facturatie'.\n"
            "• Voer een export uit na elke facturatierun.\n"
            "• Het bestand wordt aangeleverd in het gewenste boekhoudformaat.\n\n"
            "✅ Tip: Controleer altijd of het bedrag in de export overeenstemt "
            "met de totalen van de facturatierun voordat je het aanlevert aan "
            "de financiële dienst.\n\n"
            "Vereiste rol: Facturatie"
        ),
    },
    {
        "id": "boekjaren",
        "title": "13. Boekjaren",
        "content": (
            "Facturatie > Boekjaren\n\n"
            "Functie: overzicht en beheer van boekjaren. Elk boekjaar heeft "
            "een start- en einddatum.\n\n"
            "Gebruik:\n"
            "• Normaal enkel aangepast bij de jaarwissel.\n"
            "• Een afgesloten boekjaar blokkeert nieuwe facturatieruns op die "
            "periode.\n\n"
            "⚠️ Let op: Sluit een boekjaar pas af nadat alle facturatieruns, "
            "creditnota's en betalingen voor dat jaar verwerkt zijn.\n\n"
            "Vereiste rol: Applicatie beheerder"
        ),
    },
    {
        "id": "gemarkeerde-rekeningnummers",
        "title": "14. Gemarkeerde rekeningnummers",
        "content": (
            "Facturatie > Gemarkeerde rekeningnummers\n\n"
            "Functie: lijst van rekeningnummers die door het systeem of een "
            "medewerker gemarkeerd zijn voor opvolging — typisch bij SEPA-"
            "problemen of teruggestuurde betalingen.\n\n"
            "Gebruik:\n"
            "• Controleer deze lijst minstens maandelijks of bij elke melding "
            "van een betalingsprobleem.\n"
            "• Per rekeningnummer kan je een opmerking toevoegen en de "
            "markering opheffen wanneer het probleem opgelost is.\n\n"
            "Vereiste rol: Facturatie"
        ),
    },
    {
        "id": "herfacturatie",
        "title": "15. Herfacturatie van een bestaande run",
        "content": (
            "Functie: herberekent de facturen voor een al uitgevoerde "
            "facturatierun — handig na correcties op de onderliggende "
            "tijdsregistraties of inschrijvingen.\n\n"
            "🔴 Belangrijk: Een herfacturatie OVERSCHRIJFT de bestaande "
            "factuurdata voor de geselecteerde periode. Gebruik dit enkel "
            "na overleg met Kevin Samyn.\n\n"
            "Werkwijze:\n"
            "1. Open de bestaande facturatierun via Facturatie > Administratie.\n"
            "2. Klik op het menu-icoon rechts van de run.\n"
            "3. Selecteer 'Herfactureer'.\n"
            "4. Bevestig dat je de bestaande data wil overschrijven.\n"
            "5. Wacht tot de status terug op 'PDF aangemaakt' staat.\n\n"
            "⚠️ Let op: PDF's worden niet automatisch vernieuwd na een "
            "herfacturatie — hergenereer ze handmatig via het menu-icoon."
        ),
    },
    {
        "id": "minimum-facturen",
        "title": "16. Minimumbedrag per factuur",
        "content": (
            "Functie: facturen onder een ingesteld minimumbedrag worden "
            "gegroepeerd op de volgende factuur of overgeslagen voor die "
            "periode.\n\n"
            "Configuratie:\n"
            "• Instelbaar per facturatierun in stap 3 'Extra parameters'.\n"
            "• Standaardwaarde: zie Administratie > Beheer organisatie > "
            "Afrekeningen.\n\n"
            "✅ Tip: Zet het minimumbedrag op €2,50 voor opvangfacturen om "
            "lage maandbedragen te bundelen. Voor activiteitenfacturen laat "
            "je het minimum best op €0 — anders verdwijnen kleine "
            "inschrijvingen uit de facturatie."
        ),
    },
    {
        "id": "facturen-met-boetes",
        "title": "17. Facturen met boetes",
        "content": (
            "Functie: overzicht van afrekeningen waar één of meerdere boetes "
            "toegepast werden (laattijdig afhalen, no-show, afwezigheid na "
            "voorinschrijving, …).\n\n"
            "Werkwijze:\n"
            "1. Open de facturatierun via Facturatie > Administratie.\n"
            "2. Klik op het lijst-icoon naast de run.\n"
            "3. Activeer de filter 'Met boete'.\n"
            "4. Controleer per factuur of de boete correct is.\n\n"
            "⚠️ Let op: Een lege lijst kan betekenen dat de boetes niet "
            "correct gekoppeld zijn aan de voorinschrijvingsactiviteit. "
            "Controleer in dat geval de tarief-koppeling op het "
            "activiteitenoverzicht."
        ),
    },
]

# ---------------------------------------------------------------------------
# Extend the Reporting module: how the module works, configure mode, K&G,
# and an extra task-to-report cheat sheet.
# ---------------------------------------------------------------------------
EXTRA_REPORTING_SECTIONS = [
    {
        "id": "hoe-rapportering-werkt",
        "title": "13. Hoe de rapporteringsmodule werkt",
        "content": (
            "Ga naar Rapportering > Algemeen om het dashboard met alle "
            "rapporten te openen.\n\n"
            "Filtering:\n"
            "• Filter links op entiteit (Dienst Vrije Tijd, Speelpleinwerking, "
            "De MaxI CV, …) — zo zie je enkel de rapporten die relevant zijn "
            "voor jouw dienst.\n\n"
            "Iconen naast elk rapport:\n"
            "• CSV-icoon — download als .csv\n"
            "• Excel-icoon — download als .xlsx\n"
            "• Mail-icoon — verzend het rapport per e-mail aan een doelgroep\n"
            "• Info-icoon — toont een korte beschrijving van het rapport\n\n"
            "Rapporten met parameters (asynchroon):\n"
            "1. Klik op het rapport.\n"
            "2. Vul de parameters in (bv. datumbereik).\n"
            "3. Klik op 'Exporteer'.\n"
            "4. Je wordt doorgestuurd naar 'Recente rapporten'.\n"
            "5. Ververs de pagina — het rapport verschijnt na enkele seconden."
        ),
    },
    {
        "id": "configureer-editmode",
        "title": "14. Configureer-modus (editMode)",
        "content": (
            "⚠️ Let op: 'Configureer' opent dezelfde pagina als 'Algemeen', "
            "maar in bewerkingsmodus. De URL bevat ?editMode=1.\n\n"
            "Functionaliteit:\n"
            "• Per categorie verschijnt een 'Verberg'-knop.\n"
            "• Verborgen categorieën zijn niet meer zichtbaar op het "
            "dashboard van die gebruiker.\n"
            "• De knop 'Toon alles' rechtsbovenaan zet alle verborgen "
            "categorieën terug zichtbaar.\n\n"
            "Aanbeveling:\n"
            "• Verberg categorie 'Zaalverhuur' (niet in gebruik).\n"
            "• Verberg jaarspecifieke rapporten uit oude jaren "
            "(2020 t.e.m. 2024) om het dashboard overzichtelijk te houden."
        ),
    },
    {
        "id": "aanbevolen-rapporten",
        "title": "15. Aanbevolen rapporten per taak",
        "content": (
            "Onderstaand overzicht toont de meest nuttige rapporten per "
            "concrete taak.\n\n"
            "@@TABLE@@" + json.dumps(
                [
                    ["Taak", "Rapport", "Waar"],
                    ["Hoeveel kinderen ingeschreven per activiteit?", "Activiteiten: inschrijvingsoverzicht deelnemers", "Dashboard > Activiteiten"],
                    ["E-mailadressen exporteren voor mailing", "Mail: e-mailadressen gebruikers met inschrijving/entiteit", "Dashboard > Gebruikers"],
                    ["Onbetaalde tijdsregistraties controleren", "Niet-gefactureerde tijdsregistraties", "Dashboard > Kinderen"],
                    ["Omzetoverzicht per activiteit", "Activiteiten: omzet per activiteit (per entiteit)", "Dashboard > Activiteiten"],
                    ["Inwoners vs niet-inwoners", "Activiteiten: inwoners vs niet-inwoners per entiteit", "Dashboard > Activiteiten"],
                    ["CODA / boekhoudkundig rapport", "Boekhoudkundig rapport (welkomstpagina)", "Admin welkomstpagina"],
                    ["Kind & Gezin subsidies", "Kind & Gezin rapportering", "Aparte K&G sectie"],
                ],
                ensure_ascii=False,
            ) + "\n"
        ),
    },
    {
        "id": "kind-gezin-extra",
        "title": "16. Kind & Gezin rapportering — uitgebreid",
        "content": (
            "Aparte sectie voor de wettelijke rapportering aan Kind & Gezin "
            "in het kader van subsidies voor kinderopvang.\n\n"
            "Werkwijze:\n"
            "1. Ga naar Rapportering > Kind en gezin.\n"
            "2. Selecteer het rapport type (Uren pakketten, Kwartaal "
            "aangiftedossier, FCUD, …).\n"
            "3. Selecteer jaar en kwartaal.\n"
            "4. Klik op 'Download'.\n\n"
            "⚠️ Let op: De module opent altijd op de LIVE-omgeving "
            "(ingelmunster.kwandoo.com), ook als je vanuit de testomgeving "
            "navigeert. Het exportformaat is specifiek voor K&G — wijzig "
            "het bestand niet vóór indiening.\n\n"
            "✅ Tip: Plan de K&G-indiening in je agenda telkens na het "
            "einde van een kwartaal (april, juli, oktober, januari)."
        ),
    },
]


def append_sections(module_id: str, extras: list):
    mod = next((m for m in modules if m["id"] == module_id), None)
    if mod is None:
        return
    existing_ids = {s["id"] for s in mod["sections"]}
    for s in extras:
        if s["id"] not in existing_ids:
            mod["sections"].append(s)


append_sections("facturatie", EXTRA_BILLING_SECTIONS)
append_sections("rapportering", EXTRA_REPORTING_SECTIONS)


# ---------------------------------------------------------------------------
# Per-module ownership metadata.
# ---------------------------------------------------------------------------
OWNERSHIP = {
    "activiteiten":   {"editor": "Kevin Samyn", "review": "september 2026"},
    "inschrijvingen": {"editor": "Kevin Samyn", "review": "september 2026"},
    "opvang":         {"editor": "Kevin Samyn", "review": "september 2026"},
    "facturatie":     {"editor": "Kevin Samyn", "review": "september 2026"},
    "rapportering":   {"editor": "Kevin Samyn", "review": "september 2026"},
    "communicatie":   {"editor": "Kevin Samyn", "review": "september 2026"},
    "gebruikers":     {"editor": "Kevin Samyn", "review": "september 2026"},
}
for m in modules:
    if m["id"] in OWNERSHIP:
        m["meta"] = OWNERSHIP[m["id"]]
        m["meta"]["updated"] = "mei 2026"


# ---------------------------------------------------------------------------
# Quick Start cards on the homepage.
# ---------------------------------------------------------------------------
QUICK_START = [
    {"emoji": "🏃",  "title": "Nieuwe activiteit aanmaken",   "module": "activiteiten",   "section_starts": "2."},
    {"emoji": "👶",  "title": "Kind inschrijven via loket",    "module": "inschrijvingen", "section_starts": "2."},
    {"emoji": "📋",  "title": "Aanwezigheidslijst afdrukken",  "module": "rapportering",   "section_starts": "9."},
    {"emoji": "💶",  "title": "Nieuwe facturatierun starten",  "module": "facturatie",     "section_starts": "4."},
    {"emoji": "📊",  "title": "Rapport exporteren",            "module": "rapportering",   "section_starts": "4."},
    {"emoji": "📧",  "title": "Herinnering versturen",         "module": "facturatie",     "section_starts": "6."},
    {"emoji": "👤",  "title": "Nieuwe medewerker toevoegen",   "module": "gebruikers",     "section_starts": "2."},
]


def find_section(module_id: str, prefix: str):
    mod = next((m for m in modules if m["id"] == module_id), None)
    if mod is None:
        return None
    s = next((s for s in mod["sections"] if s["title"].startswith(prefix)), None)
    return s["id"] if s else None


for qs in QUICK_START:
    qs["section"] = find_section(qs["module"], qs["section_starts"])


# ---------------------------------------------------------------------------
# Workflows (cross-module procedures, rendered as accordion).
# ---------------------------------------------------------------------------
WORKFLOWS = [
    {
        "id": "wf-schooljaar",
        "icon": "🍂",
        "title": "Start van het schooljaar (augustus / september)",
        "intro": "Doorloop deze checklist voor je het nieuwe werkjaar opstart. Alle stappen samen duren typisch een halve dag.",
        "steps": [
            ("Vakantiedagen en schoolvrije dagen instellen", "opvang", "3."),
            ("Nieuwe activiteiten voor het schooljaar aanmaken", "activiteiten", "2."),
            ("Openingsuren opvang controleren voor de nieuwe set", "opvang", "3."),
            ("Promo teksten en aanbod teksten updaten naar het nieuwe jaar", "gebruikers", "5."),
            ("Nieuwe medewerkers + monitoren toevoegen en rollen toekennen", "gebruikers", "2."),
            ("Postcodes inwoners controleren (voordeeltarief)", "gebruikers", "5."),
            ("Vragenlijsten koppelen aan activiteiten (allergieën, alleen naar huis, …)", "activiteiten", "10."),
        ],
    },
    {
        "id": "wf-maandafsluiting",
        "icon": "📅",
        "title": "Maandelijkse afsluiting opvang",
        "intro": "Doorloop in deze volgorde — overslaan van een stap leidt tot foute facturen.",
        "steps": [
            ("Tijdsregistraties controleren via de datavalidatierun", "opvang", "6."),
            ("Nieuwe opvang-facturatierun aanmaken via het boek-icoon", "facturatie", "4."),
            ("Controleer afrekeningen en verzend per e-mail of post", "facturatie", "4."),
            ("Herinneringsrun starten voor onbetaalde facturen", "facturatie", "6."),
            ("Rapport 'niet-gefactureerde tijdsregistraties' controleren", "rapportering", "15."),
        ],
    },
    {
        "id": "wf-kind-inschrijven",
        "icon": "📝",
        "title": "Een kind inschrijven (volledig proces)",
        "intro": "Voor zowel loketinschrijvingen als probleemsituaties bij online inschrijven.",
        "steps": [
            ("Kindprofiel zoeken of een nieuw kind aanmaken", "inschrijvingen", "4."),
            ("Inschrijven via het loket — volg de volgorde nauwkeurig", "inschrijvingen", "2."),
            ("Tarief of korting toepassen indien van toepassing", "facturatie", "10."),
            ("Bevestigingsmail controleren via de mailinghistoriek", "communicatie", "5."),
            ("Op wachtlijst plaatsen indien volzet — opbellijst gebruiken", "inschrijvingen", "7."),
        ],
    },
    {
        "id": "wf-annulatie",
        "icon": "❌",
        "title": "Een inschrijving annuleren",
        "intro": "Annulaties triggeren automatisch boetes als de activiteit dat zo geconfigureerd heeft. Werk daarom altijd in deze volgorde.",
        "steps": [
            ("Kind zoeken via de zoekbalk of via Inschrijvingen > Kinderen", "inschrijvingen", "4."),
            ("Annulatie uitvoeren met of zonder boete (zie procedure)", "inschrijvingen", "3."),
            ("Terugbetaling instellen of krediet overzetten", "facturatie", "8."),
            ("Ouder informeren via een aangepaste mailing", "communicatie", "3."),
        ],
    },
]


def resolve_workflow_steps(workflows):
    for wf in workflows:
        new_steps = []
        for label, mod_id, prefix in wf["steps"]:
            sect = find_section(mod_id, prefix)
            new_steps.append({"label": label, "module": mod_id, "section": sect})
        wf["steps"] = new_steps


resolve_workflow_steps(WORKFLOWS)


# ---------------------------------------------------------------------------
# Dangerous Actions — Warning page.
# ---------------------------------------------------------------------------
DANGER_ITEMS = [
    {
        "title": "“Aanmelden als [ouder]” — LIVE omgeving",
        "body": (
            "Je verlaat de testomgeving en werkt rechtstreeks in de live productieomgeving (ingelmunster.kwandoo.com). "
            "Alle wijzigingen worden onmiddellijk zichtbaar voor de ouder."
        ),
        "rec": "Gebruik 'Aanmelden als' enkel bewust. Nooit testen via deze knop.",
    },
    {
        "title": "Activiteit verwijderen",
        "body": (
            "Alle gekoppelde inschrijvingen, tijdsregistraties en facturatiedata moeten eerst verwijderd worden. "
            "Deze actie is onomkeerbaar."
        ),
        "rec": "Zet een activiteit op status 'Concept' of archiveer ze in plaats van te verwijderen.",
    },
    {
        "title": "“Verwijder afrekeningen” in een facturatierun",
        "body": (
            "Deze knop is enkel actief voor runs die nog niet afgerond zijn. "
            "Eenmaal aangeklikt zijn de afrekeningen permanent verwijderd."
        ),
        "rec": "Gebruik dit nooit zonder bevestiging van Kevin Samyn.",
    },
    {
        "title": "Gebruiker permanent verwijderen",
        "body": (
            "Alle gekoppelde inschrijvingen, facturatiehistoriek en profielgegevens gaan verloren."
        ),
        "rec": "Gebruik 'Deactiveer gebruiker' in plaats van verwijderen. Historiek blijft dan bewaard.",
    },
    {
        "title": "Bulk-aanmaak deelnemers (D4–5)",
        "body": (
            "Verkeerde input kan een Internal Server Error veroorzaken. Deelnemers kunnen half-aangemaakt blijven."
        ),
        "rec": "Test altijd eerst in de testomgeving. Bij fouten: meld aan Kevin Samyn.",
    },
    {
        "title": "Activatiemail versturen",
        "body": (
            "Verstuurt onmiddellijk een mail aan de ouder. Niet ongedaan te maken. "
            "Als het e-mailadres ontbreekt of ongeldig is, stuurt het systeem je door naar het bewerkformulier met een foutmelding."
        ),
        "rec": "Controleer altijd het e-mailadres vóór je op verzenden klikt.",
    },
]


# ---------------------------------------------------------------------------
# PNG → base64 data URIs (same as v2).
# ---------------------------------------------------------------------------
IMAGES = {}
for png in sorted(Path(".").glob("*.png")):
    b64 = base64.b64encode(png.read_bytes()).decode("ascii")
    IMAGES[png.name] = f"data:image/png;base64,{b64}"


PAYLOAD = {
    "modules": modules,
    "quickStart": QUICK_START,
    "workflows": WORKFLOWS,
    "danger": DANGER_ITEMS,
}

PAYLOAD_JSON = json.dumps(PAYLOAD, ensure_ascii=False)
IMAGES_JSON = json.dumps(IMAGES, ensure_ascii=False)
print(f"Payload: {len(PAYLOAD_JSON):,} bytes; {len(IMAGES)} PNGs ({sum(len(v) for v in IMAGES.values()):,} bytes data URIs)")


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------
HTML = r"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kwandoo Kennisbank v3 — Gemeente Ingelmunster</title>
<meta name="description" content="Interne kennisbank voor de Dienst Vrije Tijd van Gemeente Ingelmunster — handleidingen, workflows en veiligheidswaarschuwingen rond Kwandoo.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {
  --green: #2d7a3a;
  --green-dark: #1f5a28;
  --green-soft: #EAF6EC;
  --blue: #1a3a6b;
  --blue-soft: #E4EAF4;
  --red: #c0392b;
  --red-soft: #FDEDEB;
  --bg: #F8F9FA;
  --card: #FFFFFF;
  --border: #E8EAED;
  --text: #1f2328;
  --muted: #5f6368;
  --warning-border: #F57C00;
  --warning-soft: #FFF3E0;
  --success-border: #2E7D32;
  --success-soft: #E8F5E9;
}

*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; height: 100%; }
body {
  font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 14.5px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-thumb { background: #dadce0; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #bdc1c6; }

/* Visible focus indicators — never remove (WCAG 2.4.7) */
a:focus-visible, button:focus-visible, input:focus-visible,
textarea:focus-visible, [tabindex]:focus-visible, [role="button"]:focus-visible {
  outline: 3px solid #FFB300;
  outline-offset: 2px;
  border-radius: 6px;
}

.skip-link {
  position: absolute; top: -42px; left: 12px;
  background: var(--blue); color: #fff;
  padding: 9px 14px; border-radius: 0 0 8px 8px;
  font-weight: 700; text-decoration: none;
  z-index: 100;
  transition: top .15s;
}
.skip-link:focus { top: 0; }

/* ===== Header ===== */
.app-header {
  position: fixed; top: 0; left: 0; right: 0; height: 68px;
  background: linear-gradient(135deg, var(--green) 0%, #3F9555 55%, var(--blue) 100%);
  color: #fff;
  display: flex; align-items: center; gap: 14px;
  padding: 0 20px;
  z-index: 50;
  box-shadow: 0 2px 10px rgba(0,0,0,0.18);
}
.hamburger {
  width: 36px; height: 36px; border: none; background: rgba(255,255,255,0.12);
  color: #fff; border-radius: 8px; cursor: pointer; font-size: 18px;
  display: flex; align-items: center; justify-content: center;
}
.hamburger:hover { background: rgba(255,255,255,0.22); }

.brand { display: flex; align-items: center; gap: 12px; min-width: 0; }
.brand-logo {
  width: 36px; height: 36px; border-radius: 8px; background: #fff;
  color: var(--green-dark); font-weight: 900; font-size: 14px;
  display: flex; align-items: center; justify-content: center;
}
.brand-text { line-height: 1.1; min-width: 0; }
.brand-text .title { font-weight: 800; font-size: 16px; white-space: nowrap; color: #fff; }
.brand-text .subtitle { font-size: 11.5px; opacity: 0.88; white-space: nowrap; }

.maintainer {
  font-size: 11.5px; opacity: 0.85; margin-right: auto;
  padding: 4px 10px; background: rgba(255,255,255,0.10);
  border-radius: 999px; border: 1px solid rgba(255,255,255,0.18);
  white-space: nowrap; display: none;
}
@media (min-width: 920px) { .maintainer { display: inline-block; } }

.search-wrap {
  position: relative; flex: 1; max-width: 480px; margin-right: 8px;
}
.search-input {
  width: 100%; height: 40px;
  background: rgba(255,255,255,0.96); color: var(--text);
  border: none; outline: none;
  border-radius: 10px; padding: 0 60px 0 40px;
  font-family: inherit; font-size: 14.5px;
}
.search-input:focus { box-shadow: 0 0 0 3px rgba(255,255,255,0.35); }
.search-icon {
  position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
  font-size: 16px; opacity: 0.55; pointer-events: none;
}
.search-kbd {
  position: absolute; right: 32px; top: 50%; transform: translateY(-50%);
  font-size: 11px; padding: 2px 6px; background: #ECEFF1; color: #455A64;
  border-radius: 4px; pointer-events: none; font-family: monospace;
  border: 1px solid #CFD8DC; font-weight: 700;
}
.search-clear {
  position: absolute; right: 8px; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; font-size: 18px;
  color: var(--muted); padding: 4px 8px;
}

.search-suggest {
  position: absolute; top: 46px; left: 0; right: 0;
  background: #fff; color: var(--text);
  border: 1px solid var(--border); border-radius: 10px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.18);
  z-index: 60; overflow: hidden; display: none;
}
.search-suggest.open { display: block; }
.suggest-item {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 14px; cursor: pointer;
  border-bottom: 1px solid #F1F3F4; font-size: 13.5px;
}
.suggest-item:last-child { border-bottom: none; }
.suggest-item:hover, .suggest-item.focused { background: var(--green-soft); }
.suggest-item .s-icon { font-size: 14px; flex-shrink: 0; }
.suggest-item .s-title { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.suggest-item .s-tag { color: var(--muted); font-size: 11.5px; flex-shrink: 0; }

/* ===== Layout ===== */
.layout { display: flex; height: 100vh; padding-top: 68px; }
.sidebar {
  width: 248px; flex-shrink: 0;
  background: #fff; border-right: 1px solid var(--border);
  overflow-y: auto; transition: margin-left .22s ease;
}
.sidebar.collapsed { margin-left: -260px; }
.sidebar-inner { padding: 14px 10px 24px; }
.sidebar-section-title {
  font-size: 10.5px; font-weight: 800; letter-spacing: 0.6px;
  color: var(--muted); text-transform: uppercase;
  padding: 12px 10px 6px;
}
.sidebar-section-title:first-child { padding-top: 4px; }

.mod-item {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 10px; border-radius: 8px; cursor: pointer;
  color: var(--text); font-weight: 600; font-size: 13.5px;
  border-left: 3px solid transparent; margin-bottom: 2px;
}
.mod-item:hover { background: #F1F3F4; }
.mod-item.active {
  background: var(--green-soft);
  border-left-color: var(--green);
  font-weight: 800; color: var(--green-dark);
}
.mod-item.danger { color: var(--red); font-weight: 800; }
.mod-item.danger.active { background: var(--red-soft); border-left-color: var(--red); color: var(--red); }
.mod-icon { font-size: 16px; }
.mod-label { flex: 1; min-width: 0; line-height: 1.2; }
.mod-chev { font-size: 10px; opacity: 0.55; transition: transform .15s; }
.mod-item.active .mod-chev { transform: rotate(90deg); }

.sub-list { padding: 2px 0 8px 8px; }
.sub-item {
  display: block; padding: 7px 10px 7px 24px;
  font-size: 12.8px; color: #3c4043;
  border-radius: 6px; cursor: pointer; margin-bottom: 1px;
  border-left: 3px solid transparent; line-height: 1.3;
}
.sub-item:hover { background: #F1F3F4; }
.sub-item.active {
  background: var(--blue-soft);
  border-left-color: var(--blue);
  color: var(--blue); font-weight: 800;
}

/* ===== Main ===== */
.main {
  flex: 1; overflow-y: auto; padding: 22px 32px 96px;
  min-width: 0;
}
.main-inner { max-width: 980px; margin: 0 auto; }

.breadcrumbs {
  display: flex; align-items: center; gap: 6px;
  font-size: 12.5px; color: var(--muted);
  margin-bottom: 10px; flex-wrap: wrap;
}
.breadcrumbs a, .breadcrumbs button {
  background: none; border: none; padding: 0; cursor: pointer;
  font: inherit; color: var(--green-dark); font-weight: 700;
}
.breadcrumbs .sep { color: #B0BEC5; }
.breadcrumbs .current { color: var(--text); font-weight: 800; }

.module-head {
  display: flex; gap: 16px; align-items: flex-start;
  margin-bottom: 6px;
}
.module-head .big-icon { font-size: 36px; line-height: 1; }
.module-head h1 {
  font-size: 26px; font-weight: 900; margin: 0; color: var(--blue);
  line-height: 1.15;
}
.module-head p { color: var(--muted); margin: 4px 0 0; font-size: 14px; }

.meta-block {
  display: flex; flex-wrap: wrap; gap: 8px 18px;
  background: var(--blue-soft); color: var(--blue);
  padding: 10px 14px; border-radius: 10px;
  font-size: 12.5px; font-weight: 700;
  margin: 12px 0 18px;
}
.meta-block span { display: inline-flex; align-items: center; gap: 6px; }

.quick-chips {
  display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 22px;
}
.chip {
  background: #fff; border: 1px solid var(--border);
  padding: 6px 12px; border-radius: 999px; font-size: 12.5px;
  cursor: pointer; color: #3c4043; font-weight: 600;
}
.chip:hover { background: var(--green-soft); border-color: var(--green); color: var(--green-dark); }
.chip.active { background: var(--blue); border-color: var(--blue); color: #fff; }

.section-card {
  background: #fff; border: 1px solid var(--border);
  border-radius: 12px; margin-bottom: 14px; overflow: hidden;
}
.section-header {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 18px; font-weight: 800; font-size: 15.5px;
  color: var(--text); cursor: pointer; user-select: none; background: #fff;
}
.section-header.active { background: var(--blue-soft); color: var(--blue); }
.section-header .sect-chev { margin-left: auto; font-size: 11px; opacity: 0.6; }
.section-body {
  padding: 6px 18px 16px;
  border-top: 1px solid var(--border);
}
.section-body h3 { font-size: 15px; font-weight: 800; margin: 16px 0 6px; color: var(--blue); }
.section-body h4 { font-size: 13.5px; font-weight: 800; margin: 12px 0 4px; color: var(--green-dark); }

/* Notes — never colour-only: prefix icon + bold label */
.note { padding: 10px 14px; border-left: 4px solid; border-radius: 6px; margin: 10px 0; font-size: 13.6px; line-height: 1.5; }
.note.red    { background: var(--red-soft);     border-color: var(--red);     color: var(--red); }
.note.orange { background: var(--warning-soft); border-color: var(--warning-border); color: #8c5a00; }
.note.green  { background: var(--success-soft); border-color: var(--success-border); color: #1B5E20; }

.kb-list { margin: 6px 0; padding-left: 26px; }
.kb-list li { margin: 2px 0; line-height: 1.5; }
.kb-subhead { display: block; margin-top: 14px; margin-bottom: 4px; font-weight: 800; color: var(--blue); }
.kb-img { max-width: 100%; border-radius: 8px; border: 1px solid var(--border); margin: 12px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08); display: block; }
.kb-table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 12px 0; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; font-size: 13.2px; }
.kb-table th { background: var(--green); color: #fff; font-weight: 800; text-align: left; padding: 8px 12px; }
.kb-table td { padding: 8px 12px; border-top: 1px solid var(--border); vertical-align: top; }
.kb-table tbody tr:nth-child(odd) td  { background: #FFFFFF; }
.kb-table tbody tr:nth-child(even) td { background: #F2F3F4; }
.para { margin: 4px 0; }
.spacer { height: 6px; }
mark.hl { background: #fff2a8; padding: 0 2px; border-radius: 2px; }

/* ===== Search results ===== */
.results-head { font-size: 13px; color: var(--muted); margin: 10px 0 12px; font-weight: 600; }
.result-card {
  background: #fff; border: 1px solid var(--border); border-radius: 12px;
  padding: 14px 16px; margin-bottom: 12px; cursor: pointer;
}
.result-card:hover, .result-card:focus-visible { border-color: var(--green); box-shadow: 0 2px 10px rgba(45,122,58,0.12); }
.result-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.result-tag  { background: var(--green-soft); color: var(--green-dark); padding: 2px 9px; border-radius: 999px; font-size: 11.5px; font-weight: 800; }
.result-emoji { font-size: 14px; }
.result-title   { font-weight: 800; font-size: 15px; margin: 4px 0; color: var(--blue); }
.result-preview { font-size: 13px; color: #3c4043; line-height: 1.45; }
.empty-state { text-align: center; padding: 60px 16px; color: var(--muted); }
.empty-state .ico { font-size: 56px; opacity: 0.45; }
.empty-state .msg { font-size: 15px; font-weight: 800; margin-top: 10px; }
.empty-state .sub { font-size: 13px; margin-top: 4px; }
.empty-state .alt-terms { margin-top: 14px; }
.empty-state .alt-terms button {
  background: var(--green-soft); border: 1px solid var(--green);
  color: var(--green-dark); border-radius: 999px;
  padding: 5px 12px; margin: 4px; cursor: pointer; font: inherit;
  font-size: 12.5px; font-weight: 700;
}

/* ===== Quick Start cards ===== */
.qs-title { font-size: 17px; font-weight: 800; color: var(--blue); margin: 22px 0 10px; }
.qs-grid {
  display: grid; gap: 14px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
@media (max-width: 980px) { .qs-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 560px) { .qs-grid { grid-template-columns: 1fr; } }
.qs-card {
  display: flex; align-items: center; gap: 12px;
  background: linear-gradient(135deg, #ffffff 0%, var(--green-soft) 100%);
  border: 1px solid var(--border); border-left: 4px solid var(--green);
  padding: 14px 16px; border-radius: 12px; cursor: pointer;
  text-align: left; font-family: inherit; width: 100%;
  transition: transform .12s, box-shadow .12s;
}
.qs-card:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(45,122,58,0.15); }
.qs-card .qs-emoji { font-size: 28px; flex-shrink: 0; }
.qs-card .qs-text  { font-weight: 800; color: var(--blue); }
.qs-card .qs-where { display: block; font-weight: 600; color: var(--muted); font-size: 12px; margin-top: 2px; }

/* ===== Need Help block ===== */
.need-help {
  background: #fff; border: 1px solid var(--border);
  border-radius: 12px; padding: 16px 18px; margin: 22px 0;
}
.need-help h2 { font-size: 17px; margin: 0 0 8px; color: var(--blue); font-weight: 800; }
.need-help p { margin: 4px 0; font-size: 13.5px; }
.need-help a { color: var(--green-dark); font-weight: 800; }

/* ===== Workflows ===== */
.workflow-card {
  background: #fff; border: 1px solid var(--border);
  border-radius: 12px; margin-bottom: 12px; overflow: hidden;
}
.workflow-head {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 18px; cursor: pointer; font-weight: 800;
  background: linear-gradient(135deg, #ffffff 0%, var(--green-soft) 100%);
  font-size: 15.5px; color: var(--blue);
  border: none; width: 100%; text-align: left; font-family: inherit;
}
.workflow-head .wf-icon { font-size: 22px; }
.workflow-head .wf-chev { margin-left: auto; font-size: 12px; opacity: 0.6; }
.workflow-card.open .wf-chev { transform: rotate(180deg); }
.workflow-body { display: none; padding: 4px 20px 16px; }
.workflow-card.open .workflow-body { display: block; }
.workflow-body p.intro { color: var(--muted); margin: 8px 0 12px; font-size: 13.5px; }
.wf-step {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 9px 0; border-bottom: 1px dashed var(--border);
}
.wf-step:last-child { border-bottom: none; }
.wf-step input[type=checkbox] {
  margin-top: 4px; width: 16px; height: 16px;
  accent-color: var(--green); cursor: pointer; flex-shrink: 0;
}
.wf-step .wf-label { flex: 1; font-size: 13.5px; }
.wf-step .wf-go {
  background: var(--blue-soft); color: var(--blue);
  border: 1px solid var(--blue); border-radius: 8px;
  padding: 4px 10px; font: inherit; font-size: 12px; font-weight: 800;
  cursor: pointer; flex-shrink: 0;
}
.wf-step .wf-go:hover { background: var(--blue); color: #fff; }
.wf-step input:checked + .wf-label { text-decoration: line-through; color: var(--muted); }

/* ===== Danger page ===== */
.danger-banner {
  background: var(--red); color: #fff;
  padding: 22px 24px; border-radius: 14px;
  margin-bottom: 18px;
}
.danger-banner h1 { margin: 0; font-size: 24px; font-weight: 900; display: flex; align-items: center; gap: 12px; }
.danger-banner p { margin: 6px 0 0; font-size: 14.5px; opacity: 0.95; }
.danger-item {
  background: var(--red); color: #fff;
  border-radius: 12px; padding: 16px 18px; margin-bottom: 12px;
  border: 1px solid #a82d20;
}
.danger-item h2 { font-size: 16.5px; font-weight: 800; margin: 0 0 6px; display: flex; align-items: center; gap: 8px; }
.danger-item p { margin: 4px 0; font-size: 13.5px; line-height: 1.5; }
.danger-item .rec {
  margin-top: 8px; background: rgba(255,255,255,0.16);
  padding: 8px 12px; border-radius: 8px; font-size: 13.5px;
  display: flex; gap: 8px; align-items: flex-start;
}
.danger-item .rec strong { white-space: nowrap; }

/* Login As warning shown at the top of the Inschrijvingen module */
.loginas-warning {
  background: var(--red-soft); border-left: 6px solid var(--red);
  border-radius: 8px; padding: 14px 18px; margin: 6px 0 18px;
  color: #5b1a14;
}
.loginas-warning h2 {
  margin: 0 0 4px; font-size: 15px; color: var(--red); font-weight: 900;
  display: flex; align-items: center; gap: 8px;
}
.loginas-warning p { margin: 4px 0; font-size: 13.5px; line-height: 1.5; }
.loginas-warning .first { font-weight: 800; color: #5b1a14; }

/* Per-module support block + page footer */
.module-support {
  margin-top: 26px; background: #fff; border: 1px solid var(--border);
  border-radius: 12px; padding: 14px 18px; font-size: 13.5px;
}
.module-support h3 { margin: 0 0 4px; font-size: 14.5px; color: var(--green-dark); font-weight: 800; }
.module-support a { color: var(--green-dark); font-weight: 800; }

.page-footer {
  margin: 40px auto 8px; max-width: 980px;
  border-top: 1px solid var(--border); padding-top: 16px;
  font-size: 12.5px; color: var(--muted);
}
.page-footer p { margin: 4px 0; }
.page-footer a { color: var(--green-dark); font-weight: 700; }

/* Updates empty-state note */
.empty-updates {
  background: var(--warning-soft); border: 1px solid #FFE082; color: #8D6E00;
  border-radius: 10px; padding: 14px 16px; font-size: 13.5px;
}

/* Back to top */
.back-top {
  position: fixed; right: 24px; bottom: 24px;
  width: 46px; height: 46px; border-radius: 50%;
  background: var(--blue); color: #fff; border: none;
  font-size: 20px; cursor: pointer;
  box-shadow: 0 4px 16px rgba(0,0,0,0.25);
  display: none; align-items: center; justify-content: center;
  z-index: 55;
}
.back-top.visible { display: flex; }
.back-top:hover { background: #122a4d; }

@media (max-width: 720px) {
  .sidebar { position: fixed; top: 68px; bottom: 0; left: 0; z-index: 40; }
  .sidebar.collapsed { margin-left: -260px; }
  .main { padding: 18px 16px 96px; }
  .brand-text .subtitle { display: none; }
  .search-kbd { display: none; }
  .meta-block { font-size: 11.5px; }
}
</style>
</head>
<body>

<a href="#main-content" class="skip-link">Ga naar inhoud</a>

<header class="app-header" role="banner">
  <button class="hamburger" id="hamburger" aria-label="Toon of verberg het menu" aria-expanded="true">☰</button>
  <div class="brand">
    <div class="brand-logo" aria-hidden="true">4i</div>
    <div class="brand-text">
      <div class="title">Kwandoo Kennisbank <span style="opacity:.7;font-weight:600;font-size:12px;">v3</span></div>
      <div class="subtitle">Dienst Vrije Tijd — Gemeente Ingelmunster</div>
    </div>
  </div>
  <span class="maintainer" aria-label="Versie-informatie">Bijgewerkt: mei 2026 · Onderhoud: Kevin Samyn — Dienst Vrije Tijd</span>
  <div class="search-wrap">
    <span class="search-icon" aria-hidden="true">🔍</span>
    <label for="searchInput" class="sr-only" style="position:absolute;left:-9999px;">Zoek in de kennisbank</label>
    <input id="searchInput" class="search-input" type="search" placeholder="Zoek in de kennisbank…" autocomplete="off"
           aria-label="Zoek in de kennisbank" aria-controls="searchSuggest" aria-expanded="false">
    <span class="search-kbd" aria-hidden="true">Ctrl+K</span>
    <button id="searchClear" class="search-clear" style="display:none" aria-label="Zoekopdracht wissen">×</button>
    <div id="searchSuggest" class="search-suggest" role="listbox" aria-label="Zoeksuggesties"></div>
  </div>
</header>

<div class="layout">
  <aside class="sidebar" id="sidebar" role="navigation" aria-label="Hoofdnavigatie">
    <div class="sidebar-inner">
      <div class="sidebar-section-title">Start</div>
      <nav id="navStart" aria-label="Start"></nav>
      <div class="sidebar-section-title">Modules</div>
      <nav id="navModules" aria-label="Modules"></nav>
      <div class="sidebar-section-title">Werkprocessen</div>
      <nav id="navWorkflows" aria-label="Werkprocessen"></nav>
      <div class="sidebar-section-title">Beheer</div>
      <nav id="navAdmin" aria-label="Beheer"></nav>
    </div>
  </aside>
  <main class="main" id="main" role="main">
    <div class="main-inner" id="main-content" tabindex="-1"></div>
    <footer class="page-footer" role="contentinfo">
      <p><strong>🛠️ Technisch probleem of bug in Kwandoo?</strong></p>
      <p>Contacteer de Kwandoo Helpdesk via <a href="https://support.kwandoo.be" target="_blank" rel="noopener noreferrer">support.kwandoo.be</a> of mail <a href="mailto:support@kwandoo.be">support@kwandoo.be</a>.</p>
      <p>Officiële online handleidingen: <a href="https://kwandoo.atlassian.net" target="_blank" rel="noopener noreferrer">kwandoo.atlassian.net</a></p>
      <p style="margin-top:10px;">Bijgewerkt: mei 2026 · Inhoudelijk verantwoordelijke: Kevin Samyn — Dienst Vrije Tijd</p>
    </footer>
  </main>
</div>

<button class="back-top" id="backTop" aria-label="Terug naar boven">▲</button>

<script>
"use strict";
const PAYLOAD = __PAYLOAD_JSON__;
const IMAGES  = __IMAGES_JSON__;
const MODULES = PAYLOAD.modules;
const QUICK_START = PAYLOAD.quickStart;
const WORKFLOWS = PAYLOAD.workflows;
const DANGER_ITEMS = PAYLOAD.danger;

const SIDEBAR_GROUPS = {
  start:    [{ id: "home",     icon: "🏠",  title: "Home",                       description: "Snelstart en hulp" }],
  modules:  MODULES,
  workflow: [{ id: "workflows", icon: "🧭", title: "Werkprocessen",              description: "Stap-voor-stap doorheen meerdere modules" }],
  admin:    [{ id: "warning",   icon: "⛔", title: "Waarschuwing — onomkeerbaar", description: "Acties die NIET ongedaan gemaakt kunnen worden", danger: true }],
};

const state = {
  view: { kind: "home" }, // {kind:'home'} | {kind:'module', moduleId, sectionId?} | {kind:'workflows'} | {kind:'warning'} | {kind:'updates'} | {kind:'search', query}
  sidebarCollapsed: false,
  searchQuery: "",
  updatesLoaded: false,
  updatesRawText: "",
  updatesError: null,
};
let updatesModule = null;

function $(s) { return document.querySelector(s); }
function el(tag, attrs, ...children) {
  const e = document.createElement(tag);
  if (attrs) for (const k in attrs) {
    if (k === "class") e.className = attrs[k];
    else if (k === "html") e.innerHTML = attrs[k];
    else if (k.startsWith("on") && typeof attrs[k] === "function") e.addEventListener(k.slice(2), attrs[k]);
    else if (attrs[k] !== false && attrs[k] != null) e.setAttribute(k, attrs[k]);
  }
  for (const c of children) {
    if (c == null || c === false) continue;
    e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return e;
}
function escHtml(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function findModule(id) { return MODULES.find(m => m.id === id); }
function findSection(modId, secId) {
  const m = findModule(modId); if (!m) return null;
  return m.sections.find(s => s.id === secId) || null;
}
function getAllSearchableModules() { return updatesModule ? MODULES.concat([updatesModule]) : MODULES; }

// ===== Content rendering =====
function isStep(l)    { return /^\d+\.\s/.test(l) && l.length < 250; }
function isBullet(l)  { return /^[•\-\*]\s/.test(l); }
function isSubhead(l) { return /^\d+\.\d+\s+\S/.test(l) && l.length < 120; }

function renderContent(text) {
  if (!text) return "";
  const lines = text.split(/\r?\n/);
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const raw = lines[i];
    const line = raw.trim();
    if (!line) { out.push('<div class="spacer"></div>'); i++; continue; }
    if (line.startsWith("@@TABLE@@")) {
      try {
        const d = JSON.parse(line.slice("@@TABLE@@".length));
        const headers = d[0] || [];
        let html = '<table class="kb-table"><thead><tr>';
        for (const h of headers) html += "<th scope=\"col\">" + escHtml(h) + "</th>";
        html += "</tr></thead><tbody>";
        for (let r = 1; r < d.length; r++) {
          html += "<tr>";
          for (let c = 0; c < headers.length; c++) html += "<td>" + escHtml(d[r][c] || "") + "</td>";
          html += "</tr>";
        }
        html += "</tbody></table>";
        out.push(html);
      } catch (e) { out.push('<div class="para">' + escHtml(line) + "</div>"); }
      i++; continue;
    }
    const im = line.match(/^@@IMG@@(.+?)@@$/);
    if (im) {
      const src = IMAGES[im[1]];
      if (src) out.push('<img class="kb-img" src="' + src + '" alt="Schermafbeelding uit Kwandoo: ' + escHtml(im[1].replace(/_/g, " ").replace(/\.png$/, "")) + '" loading="lazy">');
      i++; continue;
    }
    if (line.startsWith("🔴")) { out.push('<div class="note red" role="note"><strong>Belangrijk:</strong> ' + escHtml(line.replace(/^🔴\s*Belangrijk:?\s*/, "")) + "</div>"); i++; continue; }
    if (line.startsWith("⚠️")) { out.push('<div class="note orange" role="note"><strong>Let op:</strong> ' + escHtml(line.replace(/^⚠️\s*Let op:?\s*/, "")) + "</div>"); i++; continue; }
    if (line.startsWith("✅")) { out.push('<div class="note green" role="note"><strong>Tip:</strong> ' + escHtml(line.replace(/^✅\s*Tip:?\s*/, "")) + "</div>"); i++; continue; }
    if (isSubhead(line)) { out.push('<h4 class="kb-subhead">' + escHtml(line) + "</h4>"); i++; continue; }
    if (isStep(line)) {
      const items = [];
      while (i < lines.length && isStep(lines[i].trim()) && !isSubhead(lines[i].trim())) {
        items.push(lines[i].trim().replace(/^\d+\.\s+/, ""));
        i++;
      }
      out.push('<ol class="kb-list">' + items.map(t => "<li>" + escHtml(t) + "</li>").join("") + "</ol>");
      continue;
    }
    if (isBullet(line)) {
      const items = [];
      while (i < lines.length && isBullet(lines[i].trim())) {
        items.push(lines[i].trim().replace(/^[•\-\*]\s+/, ""));
        i++;
      }
      out.push('<ul class="kb-list">' + items.map(t => "<li>" + escHtml(t) + "</li>").join("") + "</ul>");
      continue;
    }
    out.push('<div class="para">' + escHtml(line) + "</div>");
    i++;
  }
  return out.join("");
}

// ===== Sidebar =====
function renderSidebar() {
  renderNavGroup("#navStart",     SIDEBAR_GROUPS.start,    "home");
  renderNavGroup("#navModules",   SIDEBAR_GROUPS.modules,  "module");
  renderNavGroup("#navWorkflows", SIDEBAR_GROUPS.workflow, "workflows");
  const adminItems = updatesModule
    ? SIDEBAR_GROUPS.admin.concat([{ id: "updates", icon: "📝", title: updatesModule.title, description: updatesModule.description }])
    : SIDEBAR_GROUPS.admin.concat([{ id: "updates", icon: "📝", title: "Updates & Nieuws", description: "Recente updates" }]);
  renderNavGroup("#navAdmin", adminItems, "admin");
}

function renderNavGroup(selector, items, kind) {
  const nav = $(selector); if (!nav) return;
  nav.innerHTML = "";
  for (const it of items) {
    const isActive = isItemActive(it, kind);
    const cls = "mod-item" + (isActive ? " active" : "") + (it.danger ? " danger" : "");
    const item = el("div", {
      class: cls, role: "button", tabindex: "0",
      "aria-current": isActive ? "page" : false,
      "aria-label": "Open " + it.title,
      onclick: () => navigateToItem(it),
      onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); navigateToItem(it); } }
    },
      el("span", { class: "mod-icon", "aria-hidden": "true" }, it.icon),
      el("span", { class: "mod-label" }, it.title),
      it.sections ? el("span", { class: "mod-chev", "aria-hidden": "true" }, "▸") : null
    );
    nav.appendChild(item);
    // Show sub-sections only for an active module
    if (isActive && it.sections) {
      const sub = el("div", { class: "sub-list" });
      for (const s of it.sections) {
        const sActive = state.view.kind === "module" && state.view.moduleId === it.id && state.view.sectionId === s.id;
        sub.appendChild(el("div", {
          class: "sub-item" + (sActive ? " active" : ""),
          role: "button", tabindex: "0",
          "aria-current": sActive ? "page" : false,
          onclick: (e) => { e.stopPropagation(); openSection(it.id, s.id); },
          onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openSection(it.id, s.id); } }
        }, s.title));
      }
      nav.appendChild(sub);
    }
  }
}

function isItemActive(item, kind) {
  if (state.view.kind === "search") return false;
  if (kind === "home")       return state.view.kind === "home";
  if (kind === "workflows")  return state.view.kind === "workflows";
  if (kind === "admin")      return state.view.kind === "warning" && item.id === "warning" || state.view.kind === "updates" && item.id === "updates";
  if (kind === "module")     return state.view.kind === "module" && state.view.moduleId === item.id;
  return false;
}

function navigateToItem(item) {
  if (item.id === "home")      goHome();
  else if (item.id === "workflows") goWorkflows();
  else if (item.id === "warning")   goWarning();
  else if (item.id === "updates")   goUpdates();
  else                              openModule(item.id);
}

// ===== Navigation =====
function goHome()      { state.view = { kind: "home" };     afterNavigate(); }
function goWorkflows() { state.view = { kind: "workflows" }; afterNavigate(); }
function goWarning()   { state.view = { kind: "warning" };  afterNavigate(); }
function goUpdates()   { state.view = { kind: "updates" };  afterNavigate(); }
function openModule(id)  { state.view = { kind: "module", moduleId: id }; afterNavigate(); }
function openSection(modId, secId) {
  state.view = { kind: "module", moduleId: modId, sectionId: secId };
  afterNavigate(true);
  setTimeout(() => { const t = document.getElementById("sect-" + secId); if (t) t.scrollIntoView({ behavior: "smooth", block: "start" }); }, 30);
}

function afterNavigate(keepScroll) {
  state.searchQuery = "";
  $("#searchInput").value = "";
  $("#searchClear").style.display = "none";
  $("#searchSuggest").classList.remove("open");
  renderSidebar();
  renderMain();
  if (!keepScroll) $("#main").scrollTop = 0;
  const main = $("#main-content");
  if (main) main.focus({ preventScroll: true });
}

// ===== Main router =====
function renderMain() {
  const root = $("#main-content");
  root.innerHTML = "";
  if (state.view.kind === "search") return renderSearchPage(root);
  if (state.view.kind === "home")      return renderHome(root);
  if (state.view.kind === "workflows") return renderWorkflows(root);
  if (state.view.kind === "warning")   return renderWarning(root);
  if (state.view.kind === "updates")   return renderUpdatesView(root);
  if (state.view.kind === "module")    return renderModule(root);
  renderHome(root);
}

// ===== Home page =====
function renderHome(root) {
  root.appendChild(crumb([{ label: "Home", current: true }]));
  root.appendChild(el("div", { class: "module-head" },
    el("div", { class: "big-icon", "aria-hidden": "true" }, "🏠"),
    el("div", null,
      el("h1", null, "Welkom in de Kwandoo Kennisbank"),
      el("p", null, "Gemeente Ingelmunster — Dienst Vrije Tijd. Snelle toegang tot procedures, workflows en veiligheidsregels.")
    )
  ));
  root.appendChild(el("div", { class: "meta-block", "aria-label": "Versie-informatie" },
    el("span", null, el("strong", null, "📅 Bijgewerkt:"), " mei 2026"),
    el("span", null, el("strong", null, "👤 Onderhoud:"), " Kevin Samyn — Dienst Vrije Tijd"),
    el("span", null, el("strong", null, "🔄 Volgende review:"), " september 2026")
  ));

  // Quick start
  root.appendChild(el("h2", { class: "qs-title" }, "Meest gebruikte acties"));
  const grid = el("div", { class: "qs-grid", role: "list" });
  for (const qs of QUICK_START) {
    const card = el("button", {
      class: "qs-card", role: "listitem",
      "aria-label": qs.title + " — gaat naar de betreffende sectie",
      onclick: () => { if (qs.section) openSection(qs.module, qs.section); else openModule(qs.module); }
    },
      el("span", { class: "qs-emoji", "aria-hidden": "true" }, qs.emoji),
      el("span", { class: "qs-text" }, qs.title,
        el("span", { class: "qs-where" }, "→ " + (findModule(qs.module) || {title:""}).title)
      )
    );
    grid.appendChild(card);
  }
  root.appendChild(grid);

  // Need help
  const help = el("div", { class: "need-help" });
  help.innerHTML =
    "<h2>Hulp nodig?</h2>" +
    "<p><strong>🛠️ Kwandoo Helpdesk:</strong> <a href=\"https://support.kwandoo.be\" target=\"_blank\" rel=\"noopener noreferrer\">support.kwandoo.be</a> · <a href=\"mailto:support@kwandoo.be\">support@kwandoo.be</a></p>" +
    "<p><strong>👤 Inhoudelijk:</strong> Kevin Samyn — Dienst Vrije Tijd, Gemeente Ingelmunster</p>" +
    "<p><strong>📖 Officiële handleidingen:</strong> <a href=\"https://kwandoo.atlassian.net\" target=\"_blank\" rel=\"noopener noreferrer\">kwandoo.atlassian.net</a></p>" +
    "<p style=\"color:var(--muted);font-size:12.5px;margin-top:8px;\">Vermeld bij elke ticket: omschrijving van het probleem, een screenshot en of het om de live- of testomgeving gaat.</p>";
  root.appendChild(help);

  // Modules quick access
  root.appendChild(el("h2", { class: "qs-title" }, "Modules"));
  const grid2 = el("div", { class: "qs-grid", role: "list" });
  for (const m of MODULES) {
    grid2.appendChild(el("button", {
      class: "qs-card", role: "listitem",
      "aria-label": "Open module " + m.title,
      onclick: () => openModule(m.id)
    },
      el("span", { class: "qs-emoji", "aria-hidden": "true" }, m.icon),
      el("span", { class: "qs-text" }, m.title,
        el("span", { class: "qs-where" }, m.description)
      )
    ));
  }
  root.appendChild(grid2);
}

// ===== Module view =====
function renderModule(root) {
  const mod = findModule(state.view.moduleId);
  if (!mod) return renderHome(root);
  root.appendChild(crumb([
    { label: "Home", onClick: goHome },
    { label: mod.title, current: true }
  ]));
  root.appendChild(el("div", { class: "module-head" },
    el("div", { class: "big-icon", "aria-hidden": "true" }, mod.icon),
    el("div", null,
      el("h1", null, mod.title),
      el("p", null, mod.description)
    )
  ));
  if (mod.meta) {
    root.appendChild(el("div", { class: "meta-block", "aria-label": "Module-metadata" },
      el("span", null, el("strong", null, "📅 Bijgewerkt:"), " " + mod.meta.updated),
      el("span", null, el("strong", null, "👤 Redacteur:"), " " + mod.meta.editor),
      el("span", null, el("strong", null, "🔄 Volgende review:"), " " + mod.meta.review)
    ));
  }
  // Login-as warning at the top of the Registrations module
  if (mod.id === "inschrijvingen") {
    const w = el("div", { class: "loginas-warning", role: "alert" });
    w.innerHTML =
      '<h2>⛔ RISICO: “Aanmelden als” schakelt over naar de LIVE omgeving</h2>' +
      '<p class="first">Als je vanuit een ouderprofiel op “Aanmelden als [naam]” klikt, verlaat je de testomgeving en werk je rechtstreeks in de live productieomgeving (ingelmunster.kwandoo.com).</p>' +
      '<p>Alle wijzigingen die je hier doet, zijn onmiddellijk zichtbaar voor de ouder.</p>' +
      '<p>✅ Gebruik “Aanmelden als” enkel om inschrijvingen af te ronden of te corrigeren op vraag van een ouder — nooit om te testen.</p>';
    root.appendChild(w);
  }

  // Quick chips
  if (mod.sections && mod.sections.length) {
    const chips = el("div", { class: "quick-chips", role: "list" });
    for (const s of mod.sections) {
      chips.appendChild(el("button", {
        class: "chip" + (state.view.sectionId === s.id ? " active" : ""),
        role: "listitem",
        "aria-label": "Spring naar " + s.title,
        onclick: () => openSection(mod.id, s.id)
      }, s.title));
    }
    root.appendChild(chips);
  }

  for (const s of mod.sections || []) {
    root.appendChild(buildSectionCard(mod, s));
  }

  root.appendChild(buildSupportBlock());
}

function buildSectionCard(mod, s) {
  const isActive = state.view.sectionId === s.id;
  const card = el("section", { class: "section-card", id: "sect-" + s.id, "aria-labelledby": "h-" + s.id });
  card.appendChild(el("h2", {
    class: "section-header" + (isActive ? " active" : ""),
    id: "h-" + s.id,
    role: "button", tabindex: "0",
    "aria-expanded": "true",
    onclick: () => { openSection(mod.id, s.id); },
    onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openSection(mod.id, s.id); } }
  },
    document.createTextNode(s.title),
    el("span", { class: "sect-chev", "aria-hidden": "true" }, "▼")
  ));
  const body = el("div", { class: "section-body" });
  body.innerHTML = renderContent(s.content);
  card.appendChild(body);
  return card;
}

function buildSupportBlock() {
  const support = el("aside", { class: "module-support", "aria-label": "Hulp bij deze module" });
  support.innerHTML =
    "<h3>🛠️ Technisch probleem of bug?</h3>" +
    "<p>Kwandoo Helpdesk: <a href=\"https://support.kwandoo.be\" target=\"_blank\" rel=\"noopener noreferrer\">support.kwandoo.be</a> · <a href=\"mailto:support@kwandoo.be\">support@kwandoo.be</a></p>" +
    "<p>Vermeld altijd: omschrijving van het probleem, een screenshot en of het om de live- of testomgeving gaat.</p>";
  return support;
}

// ===== Workflows view =====
function renderWorkflows(root) {
  root.appendChild(crumb([
    { label: "Home", onClick: goHome },
    { label: "Werkprocessen", current: true }
  ]));
  root.appendChild(el("div", { class: "module-head" },
    el("div", { class: "big-icon", "aria-hidden": "true" }, "🧭"),
    el("div", null,
      el("h1", null, "Werkprocessen"),
      el("p", null, "Doorloop een proces van begin tot einde — elke stap linkt naar de juiste module.")
    )
  ));
  for (const wf of WORKFLOWS) {
    const card = el("article", { class: "workflow-card", "aria-labelledby": "wf-" + wf.id });
    const head = el("button", {
      class: "workflow-head", id: "wf-" + wf.id,
      "aria-expanded": "false",
      onclick: (e) => {
        card.classList.toggle("open");
        head.setAttribute("aria-expanded", card.classList.contains("open") ? "true" : "false");
      }
    },
      el("span", { class: "wf-icon", "aria-hidden": "true" }, wf.icon),
      el("span", null, wf.title),
      el("span", { class: "wf-chev", "aria-hidden": "true" }, "▼")
    );
    card.appendChild(head);
    const body = el("div", { class: "workflow-body" });
    body.appendChild(el("p", { class: "intro" }, wf.intro));
    let n = 1;
    for (const st of wf.steps) {
      const checkboxId = "chk-" + wf.id + "-" + (n++);
      body.appendChild(el("div", { class: "wf-step" },
        el("input", { type: "checkbox", id: checkboxId, "aria-label": "Markeer stap als afgewerkt: " + st.label }),
        el("label", { class: "wf-label", for: checkboxId }, st.label),
        st.section
          ? el("button", {
              class: "wf-go",
              "aria-label": "Open de module voor: " + st.label,
              onclick: () => openSection(st.module, st.section)
            }, "Open →")
          : el("button", {
              class: "wf-go",
              "aria-label": "Open de module: " + st.label,
              onclick: () => openModule(st.module)
            }, "Open →")
      ));
    }
    card.appendChild(body);
    root.appendChild(card);
  }
  root.appendChild(buildSupportBlock());
}

// ===== Warning view =====
function renderWarning(root) {
  root.appendChild(crumb([
    { label: "Home", onClick: goHome },
    { label: "Waarschuwing", current: true }
  ]));
  const banner = el("section", { class: "danger-banner", role: "alert", "aria-label": "Waarschuwing — onomkeerbare acties" });
  banner.innerHTML =
    '<h1>⛔ Acties die NIET ongedaan gemaakt kunnen worden</h1>' +
    '<p>Deze acties zijn permanent. Lees ze grondig vóór je ze uitvoert — bij twijfel altijd overleggen met Kevin Samyn.</p>';
  root.appendChild(banner);
  let n = 1;
  for (const d of DANGER_ITEMS) {
    const card = el("article", { class: "danger-item", "aria-labelledby": "dh-" + n });
    card.innerHTML =
      '<h2 id="dh-' + n + '"><span aria-hidden="true">⛔</span> ' + n + '. ' + escHtml(d.title) + '</h2>' +
      '<p>' + escHtml(d.body) + '</p>' +
      '<div class="rec"><strong>➜ Aanbeveling:</strong> ' + escHtml(d.rec) + '</div>';
    root.appendChild(card);
    n++;
  }
  root.appendChild(buildSupportBlock());
}

// ===== Updates view (loaded via fetch) =====
function renderUpdatesView(root) {
  root.appendChild(crumb([
    { label: "Home", onClick: goHome },
    { label: "Updates & Nieuws", current: true }
  ]));
  root.appendChild(el("div", { class: "module-head" },
    el("div", { class: "big-icon", "aria-hidden": "true" }, "📝"),
    el("div", null,
      el("h1", null, "Updates & Nieuws"),
      el("p", null, "Nieuwste procedures, problemen en oplossingen — onderhouden door de dienst.")
    )
  ));
  if (!updatesModule || !updatesModule.sections.length) {
    const note = el("div", { class: "empty-updates", role: "note" });
    note.textContent = state.updatesError
      ? "Updates laden enkel via de webversie. Open de website via de GitHub Pages URL."
      : "Nog geen updates beschikbaar. Updates verschijnen hier zodra het bestand 'kennisbank-updates.txt' op de server staat.";
    root.appendChild(note);
    return;
  }
  for (const s of updatesModule.sections) {
    const card = el("section", { class: "section-card" });
    card.appendChild(el("h2", { class: "section-header active" },
      document.createTextNode(s.title),
      el("span", { class: "sect-chev", "aria-hidden": "true" }, "▼")
    ));
    const body = el("div", { class: "section-body" });
    body.innerHTML = renderContent(s.content);
    card.appendChild(body);
    root.appendChild(card);
  }
  root.appendChild(buildSupportBlock());
}

// ===== Breadcrumbs =====
function crumb(parts) {
  const nav = el("nav", { class: "breadcrumbs", "aria-label": "Broodkruimels" });
  parts.forEach((p, i) => {
    if (i > 0) nav.appendChild(el("span", { class: "sep", "aria-hidden": "true" }, "›"));
    if (p.current) nav.appendChild(el("span", { class: "current" }, p.label));
    else nav.appendChild(el("button", { onclick: p.onClick, "aria-label": "Ga terug naar " + p.label }, p.label));
  });
  return nav;
}

// ===== Search =====
const SYNONYM_GROUPS = [
  ["inloggen", "aanmelden", "login", "account", "klantenzone", "wachtwoord", "paswoord"],
  ["rekening", "betaling", "factuur", "afrekening", "facturatie"],
  ["kind", "leerling", "deelnemer", "kindbeheer"],
  ["mail", "email", "e-mail", "bericht", "communicatie", "mailing"],
  ["fout", "probleem", "error", "werkt niet", "faq"],
  ["opvang", "tijdregistratie", "tijdsregistratie", "klok"],
  ["rapport", "overzicht", "export", "download", "rapportering"],
  ["rol", "rechten", "toegang", "permissie", "gebruiker"],
  ["boete", "straf", "annulatie", "annulering"],
  ["allergie", "medisch", "vragenlijst"],
];
const SYNONYM_MAP = {};
for (const g of SYNONYM_GROUPS) for (const w of g) SYNONYM_MAP[w] = g.filter(x => x !== w);
function getSynonyms(q) { return SYNONYM_MAP[q.toLowerCase().trim()] || []; }

function levenshtein(a, b, threshold) {
  if (a === b) return 0;
  if (Math.abs(a.length - b.length) > threshold) return threshold + 1;
  if (!a.length) return b.length;
  if (!b.length) return a.length;
  let prev = new Array(b.length + 1);
  for (let j = 0; j <= b.length; j++) prev[j] = j;
  for (let i = 1; i <= a.length; i++) {
    const curr = new Array(b.length + 1); curr[0] = i;
    let rowMin = i;
    for (let j = 1; j <= b.length; j++) {
      const cost = a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1;
      curr[j] = Math.min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost);
      if (curr[j] < rowMin) rowMin = curr[j];
    }
    if (rowMin > threshold) return threshold + 1;
    prev = curr;
  }
  return prev[b.length];
}
function tokenize(t) { return t.toLowerCase().split(/[^a-zà-ÿ0-9]+/i).filter(w => w.length >= 3); }
function fuzzyWordMatch(q, words) {
  if (q.length <= 5) return false;
  for (const w of words) {
    if (Math.abs(w.length - q.length) > 2) continue;
    if (levenshtein(q, w, 2) <= 2) return true;
  }
  return false;
}

let SEARCH_INDEX = [];
function rebuildSearchIndex() {
  SEARCH_INDEX = [];
  for (const m of getAllSearchableModules()) {
    for (const s of m.sections) {
      SEARCH_INDEX.push({
        module: m, section: s,
        titleLower: s.title.toLowerCase(),
        contentLower: s.content.toLowerCase(),
        titleWords: tokenize(s.title),
        contentWords: tokenize(s.content),
      });
    }
  }
}

function scoreSection(it, q, synonyms) {
  if (it.titleLower.includes(q)) return { score: 1000, matched: q };
  for (const s of synonyms) if (it.titleLower.includes(s)) return { score: 700, matched: s };
  if (fuzzyWordMatch(q, it.titleWords)) return { score: 500, matched: q };
  if (it.contentLower.includes(q)) return { score: 300, matched: q };
  for (const s of synonyms) if (it.contentLower.includes(s)) return { score: 200, matched: s };
  if (fuzzyWordMatch(q, it.contentWords)) return { score: 100, matched: q };
  return null;
}

function runSearch(query) {
  const q = query.toLowerCase().trim();
  if (!q) return [];
  const synonyms = getSynonyms(q);
  const out = [];
  for (const it of SEARCH_INDEX) {
    const m = scoreSection(it, q, synonyms);
    if (m) out.push({ ...it, score: m.score, matched: m.matched });
  }
  out.sort((a, b) => b.score - a.score);
  return out;
}

function buildSuggestions(query) {
  if (!query || query.length < 2) return [];
  const q = query.toLowerCase().trim();
  const synonyms = getSynonyms(q);
  const ranked = [];
  for (const it of SEARCH_INDEX) {
    let score = 0; let matched = q;
    if (it.titleLower.includes(q)) score = 1000;
    else if (synonyms.some(s => it.titleLower.includes(s))) { score = 700; matched = synonyms.find(s => it.titleLower.includes(s)); }
    else if (fuzzyWordMatch(q, it.titleWords)) score = 500;
    if (score > 0) ranked.push({ it, score, matched });
  }
  ranked.sort((a, b) => b.score - a.score);
  return ranked.slice(0, 5);
}

function renderSuggestions() {
  const box = $("#searchSuggest"); if (!box) return;
  const q = $("#searchInput").value.trim();
  if (q.length < 2) { box.classList.remove("open"); box.innerHTML = ""; $("#searchInput").setAttribute("aria-expanded", "false"); return; }
  const sug = buildSuggestions(q);
  if (!sug.length) { box.classList.remove("open"); box.innerHTML = ""; $("#searchInput").setAttribute("aria-expanded", "false"); return; }
  box.innerHTML = sug.map(({ it }, i) =>
    '<div class="suggest-item" role="option" tabindex="-1" data-mod="' + escHtml(it.module.id) + '" data-sec="' + escHtml(it.section.id) + '">' +
      '<span class="s-icon" aria-hidden="true">' + escHtml(it.module.icon) + '</span>' +
      '<span class="s-title">' + escHtml(it.section.title) + '</span>' +
      '<span class="s-tag">' + escHtml(it.module.title) + '</span>' +
    '</div>'
  ).join("");
  box.querySelectorAll(".suggest-item").forEach(div => {
    div.addEventListener("mousedown", (e) => {
      e.preventDefault();
      const modId = div.getAttribute("data-mod");
      const secId = div.getAttribute("data-sec");
      openSection(modId, secId);
    });
  });
  box.classList.add("open");
  $("#searchInput").setAttribute("aria-expanded", "true");
}

function highlightExtra(text, primary, secondary) {
  let html = escHtml(text);
  const terms = [];
  if (primary && primary.length >= 2) terms.push(primary);
  if (secondary && secondary.length >= 2 && secondary !== primary) terms.push(secondary);
  for (const t of terms) {
    const re = new RegExp("(" + t.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&") + ")", "gi");
    html = html.replace(re, '<mark class="hl">$1</mark>');
  }
  return html;
}

function renderSearchPage(root) {
  const query = state.view.query;
  const matches = runSearch(query);
  root.appendChild(crumb([
    { label: "Home", onClick: goHome },
    { label: 'Zoekresultaten voor "' + query + '"', current: true }
  ]));
  root.appendChild(el("div", { class: "results-head", role: "status", "aria-live": "polite" },
    matches.length + ' resultaten voor "' + query + '"'));
  if (matches.length === 0) {
    const empty = el("div", { class: "empty-state" });
    const alt = ["aanmelden", "facturatie", "rapport", "allergie", "inschrijven"];
    empty.innerHTML =
      '<div class="ico" aria-hidden="true">🔎</div>' +
      '<div class="msg">Geen resultaten gevonden</div>' +
      '<div class="sub">Probeer een andere zoekterm of synoniem.</div>' +
      '<div class="alt-terms">Probeer ook: ' + alt.map(a => '<button data-q="' + escHtml(a) + '">' + escHtml(a) + '</button>').join("") + '</div>';
    empty.querySelectorAll("button[data-q]").forEach(b => {
      b.addEventListener("click", () => {
        $("#searchInput").value = b.getAttribute("data-q");
        triggerSearchInput();
      });
    });
    root.appendChild(empty);
    return;
  }
  for (const it of matches) {
    const needle = (it.matched || query).toLowerCase();
    const lower = it.section.content.toLowerCase();
    let pos = lower.indexOf(needle); if (pos < 0) pos = 0;
    const start = Math.max(0, pos - 60);
    const preview = (start > 0 ? "… " : "") + it.section.content.slice(start, start + 320);
    const card = el("button", {
      class: "result-card", role: "link",
      "aria-label": "Open " + it.module.title + " — " + it.section.title,
      onclick: () => openSection(it.module.id, it.section.id)
    });
    card.innerHTML =
      '<div class="result-meta">' +
        '<span class="result-emoji" aria-hidden="true">' + escHtml(it.module.icon) + '</span>' +
        '<span class="result-tag">' + escHtml(it.module.title) + '</span>' +
      '</div>' +
      '<div class="result-title">' + highlightExtra(it.section.title, it.matched, query) + '</div>' +
      '<div class="result-preview">' + highlightExtra(preview, it.matched, query) + '</div>';
    root.appendChild(card);
  }
}

// ===== Updates loader =====
function parseUpdates(text) {
  const stripped = text.split(/\r?\n/).filter(l => !/^\s*#/.test(l)).join("\n");
  const parts = stripped.split(/^---\s*Update\s+/m).map(s => s.trim()).filter(Boolean);
  const sections = [];
  parts.forEach((part, i) => {
    const lines = part.split(/\r?\n/);
    const header = (lines.shift() || "").replace(/-+\s*$/, "").trim();
    const body = lines.join("\n").trim();
    if (!header && !body) return;
    const subj = body.match(/^Onderwerp:\s*(.+)$/m);
    sections.push({
      id: "update-" + (i + 1),
      title: subj ? ("Update " + header + " — " + subj[1].trim()) : ("Update " + header),
      content: body,
    });
  });
  return sections;
}

function loadUpdates() {
  fetch("./kennisbank-updates.txt", { cache: "no-cache" })
    .then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r.text(); })
    .then(text => {
      state.updatesRawText = text;
      state.updatesLoaded = true;
      updatesModule = {
        id: "updates", title: "Updates & Nieuws", icon: "📝",
        description: "Recente updates aan de kennisbank.",
        sections: parseUpdates(text),
      };
      rebuildSearchIndex();
      renderSidebar();
      if (state.view.kind === "updates") renderMain();
    })
    .catch(err => {
      state.updatesError = err.message || "fetch failed";
      updatesModule = { id: "updates", title: "Updates & Nieuws", icon: "📝", description: "Recente updates.", sections: [] };
      rebuildSearchIndex();
      renderSidebar();
      if (state.view.kind === "updates") renderMain();
    });
}

// ===== Input handlers =====
function triggerSearchInput() {
  const q = $("#searchInput").value.trim();
  if (q.length >= 2) {
    state.view = { kind: "search", query: q };
    renderSidebar(); renderMain();
    renderSuggestions();
  } else {
    if (state.view.kind === "search") { goHome(); }
    renderSuggestions();
  }
}

function init() {
  rebuildSearchIndex();
  renderSidebar();
  renderMain();
  loadUpdates();

  $("#hamburger").addEventListener("click", () => {
    state.sidebarCollapsed = !state.sidebarCollapsed;
    $("#sidebar").classList.toggle("collapsed", state.sidebarCollapsed);
    $("#hamburger").setAttribute("aria-expanded", state.sidebarCollapsed ? "false" : "true");
  });

  const si = $("#searchInput");
  const sc = $("#searchClear");
  const ss = $("#searchSuggest");
  si.addEventListener("input", () => {
    sc.style.display = si.value ? "" : "none";
    triggerSearchInput();
  });
  si.addEventListener("focus", () => { renderSuggestions(); });
  si.addEventListener("blur", () => { setTimeout(() => ss.classList.remove("open"), 120); });
  si.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      si.value = ""; sc.style.display = "none";
      ss.classList.remove("open");
      if (state.view.kind === "search") goHome();
      si.blur();
    }
  });
  sc.addEventListener("click", () => {
    si.value = ""; sc.style.display = "none"; ss.classList.remove("open");
    if (state.view.kind === "search") goHome();
    si.focus();
  });

  // Global keyboard shortcuts: Ctrl+K and "/" focus the search bar
  document.addEventListener("keydown", (e) => {
    const inField = e.target && (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA");
    if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) {
      e.preventDefault(); si.focus(); si.select();
    } else if (e.key === "/" && !inField) {
      e.preventDefault(); si.focus(); si.select();
    } else if (e.key === "Escape" && ss.classList.contains("open")) {
      ss.classList.remove("open");
    }
  });

  const main = $("#main");
  const backTop = $("#backTop");
  main.addEventListener("scroll", () => {
    if (main.scrollTop > 320) backTop.classList.add("visible");
    else backTop.classList.remove("visible");
  });
  backTop.addEventListener("click", () => { main.scrollTo({ top: 0, behavior: "smooth" }); });
}

document.addEventListener("DOMContentLoaded", init);
</script>
</body>
</html>
"""

out = HTML.replace("__PAYLOAD_JSON__", PAYLOAD_JSON)
out = out.replace("__IMAGES_JSON__", IMAGES_JSON)
Path("Kwandoo_Kennisbank_v3.html").write_text(out, encoding="utf-8")
print(f"Wrote Kwandoo_Kennisbank_v3.html ({len(out):,} bytes)")
