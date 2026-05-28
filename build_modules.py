#!/usr/bin/env python3
"""Build modules.json from extracted .txt handleidingen and supplementary docs.

Post-processes section content to inject markers for proper table rendering
(@@TABLE@@<json>) and inline screenshots (@@IMG@@<filename>@@), which the
JS renderContent() turns into <table> and <img> elements at view time.
"""
import json
import re
from pathlib import Path

EXTR = Path("extracted")

MODULES_SPEC = [
    {
        "id": "activiteiten",
        "title": "Activiteiten",
        "icon": "🎯",
        "description": "Aanmaken, bewerken, dupliceren en beheren van activiteiten",
        "file": "Handleiding_activiteiten_v4_mei2026.txt",
    },
    {
        "id": "inschrijvingen",
        "title": "Inschrijvingen & Deelnemers",
        "icon": "📋",
        "description": "Loket, inschrijvingen beheren, kind- en ouderprofielen",
        "file": "Handleiding_inschrijvingen_deelnemers_v4_mei2026.txt",
    },
    {
        "id": "opvang",
        "title": "Opvang & Tijdsregistraties",
        "icon": "⏱️",
        "description": "Tijdsregistraties, noodopvang, aftekenlijst en datavalidatie",
        "file": "Handleiding_opvang_tijdsregistraties_v4_mei2026.txt",
    },
    {
        "id": "facturatie",
        "title": "Facturatie & Betalingen",
        "icon": "💶",
        "description": "Facturatieruns, herinneringen, terugbetalingen en tarieven",
        "file": "Handleiding_facturatie_betalingen_v4_mei2026.txt",
    },
    {
        "id": "rapportering",
        "title": "Rapportering",
        "icon": "📊",
        "description": "Rapporten genereren, Kind & Gezin, inschrijvingslijsten",
        "file": "Handleiding_rapportering_v4_mei2026.txt",
    },
    {
        "id": "communicatie",
        "title": "Communicatie",
        "icon": "✉️",
        "description": "Mailings, communicaties en GDPR-e-mails",
        "file": "Handleiding_communicatie_v4_mei2026.txt",
    },
    {
        "id": "gebruikers",
        "title": "Gebruikers & Organisaties",
        "icon": "⚙️",
        "description": "Gebruikersbeheer, rollen, platformconfiguratie en GDPR",
        "file": "Handleiding_gebruikers_organisaties_v4_mei2026.txt",
    },
]

# ---------------------------------------------------------------------------
# Tables to extract. Each entry specifies (module, section title prefix, header
# lines that mark the start of the table, end-anchor that marks the line right
# after the table, and column count).
# ---------------------------------------------------------------------------
TABLES = [
    # Inschrijvingen §5 Drie types ouderprofielen
    {
        "module": "inschrijvingen", "section_starts": "5.",
        "headers": ["Type", "Kenmerken", "Beschikbare acties"],
        "stop_marker": "Activatiemail versturen",
    },
    # Opvang §4.2 Noodopvang — 7 redenen
    {
        "module": "opvang", "section_starts": "4.",
        "headers": ["Reden", "Toelichting"],
        "stop_marker": "⚠️",
    },
    # Facturatie §2 Menustructuur
    {
        "module": "facturatie", "section_starts": "2.",
        "headers": ["Menu-item", "Gebruik"],
        "stop_marker": "✅",
    },
    # Facturatie §3 Twee types facturatie
    {
        "module": "facturatie", "section_starts": "3.",
        "headers": ["Type", "Gebaseerd op", "Wanneer gebruiken?"],
        "stop_marker": None,  # runs to end of section
    },
    # Facturatie §10 Tarieven types (10.1 Overzicht)
    {
        "module": "facturatie", "section_starts": "10.",
        "headers": ["Type", "Gebruik"],
        "stop_marker": "✅",
    },
    # Rapportering §7 Prioritaire rapporten per taak
    {
        "module": "rapportering", "section_starts": "7.",
        "headers": ["Taak", "Rapport", "Categorie"],
        "stop_marker": None,
    },
    # Gebruikers §3.1 Rollenmatrix — functie naar Kwandoo-rol
    {
        "module": "gebruikers", "section_starts": "3.",
        "headers": ["Functie", "Kwandoo-rollen", "Beschrijving"],
        "stop_marker": "3.2 Wat kan elke rol?",
    },
    # Gebruikers §3.2 Wat kan elke rol?
    {
        "module": "gebruikers", "section_starts": "3.",
        "headers": ["Rol", "Functionaliteit"],
        "stop_marker": "⚠️",
    },
    # Gebruikers §5 Beheer organisatie — 20-row table
    {
        "module": "gebruikers", "section_starts": "5.",
        "headers": ["Sub-item", "Wat het beheert", "Frequentie"],
        "stop_marker": None,
    },
]


def extract_table(content: str, headers: list, stop_marker: str | None):
    """Find a table whose first three lines are the given headers; group the
    following lines into rows of len(headers) columns until stop_marker (or
    end of content). Return (new_content, table_data) or (content, None) if
    not found.
    """
    cols = len(headers)
    header_pat = "\n".join(re.escape(h) for h in headers)
    m = re.search(r"(^|\n)\s*" + header_pat + r"\s*\n", content)
    if not m:
        return content, None
    start = m.start()
    body_start = m.end()
    if stop_marker:
        idx = content.find(stop_marker, body_start)
        if idx < 0:
            return content, None
        # Walk back to start of the line containing the stop marker
        line_start = content.rfind("\n", 0, idx)
        body_end = line_start + 1 if line_start >= 0 else idx
    else:
        body_end = len(content)

    body = content[body_start:body_end]
    raw_cells = [c.strip() for c in body.split("\n") if c.strip()]
    # Trim to a multiple of `cols`
    extra = len(raw_cells) % cols
    if extra:
        raw_cells = raw_cells[: len(raw_cells) - extra]
    rows = [raw_cells[i : i + cols] for i in range(0, len(raw_cells), cols)]
    if not rows:
        return content, None
    table_data = [headers] + rows
    marker = "@@TABLE@@" + json.dumps(table_data, ensure_ascii=False)
    # Preserve any leading whitespace/newline before the headers, drop the
    # original table block, and re-emit the marker on its own line.
    prefix = content[: start]
    suffix = content[body_end:]
    new_content = prefix.rstrip("\n") + "\n\n" + marker + "\n\n" + suffix.lstrip("\n")
    return new_content, table_data


# ---------------------------------------------------------------------------
# Screenshots to inline. Each entry maps a section onto an anchor substring;
# images are inserted on a new line immediately after the line containing the
# anchor. Anchors are picked to match a unique substring of the v4 handleiding.
# ---------------------------------------------------------------------------
IMAGES = [
    {
        "module": "activiteiten", "section_starts": "2.",
        "anchor": "Minimum leeftijd (jongste kind dat mag deelnemen)",
        "files": ["M1_S4_nieuwe_activiteit_formulier_deel1.png"],
    },
    {
        "module": "activiteiten", "section_starts": "3.",
        "anchor": "Vergeet je 'Publiceer activiteit' te klikken",
        "files": ["M1_S3_bewerk_activiteit_status_na_klik_deel1.png"],
    },
    {
        "module": "activiteiten", "section_starts": "5.",
        "anchor": "bekijk de gekoppelde vragenlijst voor de volledige legenda",
        "files": [
            "M1_S7_beheer_aanwezigheden_deel1.png",
            "M1_S7_beheer_aanwezigheden_deel2.png",  # substitute for M1_S7b
        ],
    },
    {
        "module": "inschrijvingen", "section_starts": "2.",
        "anchor": "Selecteer de gewenste dag(en) via de paginanummers en klik op 'Reserveer'.",
        "files": [
            "M2_S7_loket_vervolledig_reservaties.png",
            "M2_S9_loket_kind_geselecteerd.png",
        ],
    },
    {
        "module": "inschrijvingen", "section_starts": "6.",
        "anchor": "Als medewerker is het handig om te weten wat een ouder ziet",
        "files": ["M4_S7_klantenzone_als_dylan_claeys.png"],
    },
    {
        "module": "opvang", "section_starts": "4.",
        "anchor": "Een fout hier leidt tot fouten in de facturatie.",
        "files": [
            "M3_S1_tijdsregistraties_overzicht.png",
            "M3_S2_nieuwe_tijdsregistratie.png",
        ],
    },
    {
        "module": "facturatie", "section_starts": "5.",
        "anchor": "Verwijdert de afrekening — enkel mogelijk bij niet-afgeronde runs",
        "files": [
            "M5_S1_facturatie_menu_dropdown.png",
            "M5_S4_afrekening_detail_deel1.png",
            "M5_S4_afrekening_detail_deel2.png",
        ],
    },
    {
        "module": "rapportering", "section_starts": "3.",
        "anchor": "Je kan deze gepinde URL bookmarken voor sneller gebruik.",
        "files": [
            "M6_S2_rapportering_algemeen_deel1.png",
            "M6_S2_rapportering_algemeen_deel2.png",
        ],
    },
]


def insert_images(content: str, anchor: str, files: list) -> tuple[str, bool]:
    idx = content.find(anchor)
    if idx < 0:
        return content, False
    end_of_line = content.find("\n", idx)
    if end_of_line < 0:
        end_of_line = len(content)
    markers = "\n".join("@@IMG@@" + f + "@@" for f in files)
    new = content[: end_of_line] + "\n\n" + markers + "\n" + content[end_of_line:]
    return new, True


# ---------------------------------------------------------------------------
# Section splitter (unchanged from v1)
# ---------------------------------------------------------------------------

def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:60] or "section"


SECTION_RE = re.compile(r"^(\d+)\.\s+([A-ZÉÖa-zé].+)$")


def split_sections(text: str):
    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if SECTION_RE.match(line.strip()):
            start = i
            break
    sections = []
    current = None
    for line in lines[start:]:
        stripped = line.strip()
        m = SECTION_RE.match(stripped)
        # Top-level section titles never end with a sentence period; numbered
        # list items ("1. Zoek de ouder.") do — that's how we tell them apart.
        if m and len(stripped) < 90 and not stripped.endswith(".") and not stripped.endswith(".csv'"):
            num = int(m.group(1))
            title_text = m.group(2).strip()
            if current is not None:
                sections.append(current)
            current = {
                "id": slugify(f"{num}-{title_text}"),
                "title": f"{num}. {title_text}",
                "content_lines": [],
            }
        else:
            if current is None:
                current = {"id": "intro", "title": "Inleiding", "content_lines": []}
            current["content_lines"].append(line)
    if current is not None:
        sections.append(current)
    out = []
    for s in sections:
        content = "\n".join(s["content_lines"]).strip()
        content = re.sub(
            r"\n*Handleiding [^\n]+ v2\.0 — .+\n*Opgesteld door.+$",
            "",
            content,
            flags=re.MULTILINE,
        )
        out.append({"id": s["id"], "title": s["title"], "content": content.strip()})
    return out


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
modules = []
for spec in MODULES_SPEC:
    text = (EXTR / spec["file"]).read_text(encoding="utf-8")
    sections = split_sections(text)
    modules.append(
        {
            "id": spec["id"],
            "title": spec["title"],
            "icon": spec["icon"],
            "description": spec["description"],
            "sections": sections,
        }
    )

# Apply table extraction
for spec in TABLES:
    mod = next((m for m in modules if m["id"] == spec["module"]), None)
    if not mod:
        continue
    matched = False
    for sec in mod["sections"]:
        if not sec["title"].startswith(spec["section_starts"]):
            continue
        new_content, table = extract_table(sec["content"], spec["headers"], spec.get("stop_marker"))
        if table:
            sec["content"] = new_content
            matched = True
            print(f"  ✓ Table in {mod['id']} / {sec['title']}: {len(table)-1} rows × {len(spec['headers'])} cols")
            break
    if not matched:
        print(f"  ✗ Table NOT FOUND: {spec['module']} / {spec['section_starts']} / {spec['headers']}")

# Apply image insertion
for spec in IMAGES:
    mod = next((m for m in modules if m["id"] == spec["module"]), None)
    if not mod:
        continue
    matched = False
    for sec in mod["sections"]:
        if not sec["title"].startswith(spec["section_starts"]):
            continue
        new_content, ok = insert_images(sec["content"], spec["anchor"], spec["files"])
        if ok:
            sec["content"] = new_content
            matched = True
            print(f"  ✓ Images in {mod['id']} / {sec['title']}: {spec['files']}")
            break
    if not matched:
        print(f"  ✗ Image anchor NOT FOUND: {spec['module']} / {spec['section_starts']} / {spec['anchor'][:60]}")

# Supplementary knowledge (unchanged)
supplementary = []
for fname in [
    "Rollenmatrix_Kwandoo_Ingelmunster.txt",
    "ASIS_Kwandoo_Medewerkersperspectief_v3.txt",
    "ASIS_Kwandoo_Ouderperspectief_v3.txt",
    "TOBE_Kwandoo_v2_mei2026 (1).txt",
]:
    p = EXTR / fname
    if p.exists():
        supplementary.append(f"\n\n=== SUPPLEMENT: {fname} ===\n")
        supplementary.append(p.read_text(encoding="utf-8"))

result = {"modules": modules, "supplementary": "".join(supplementary)}
Path("modules.json").write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
print(f"\nTotal JSON: {len(json.dumps(result, ensure_ascii=False))} bytes")
