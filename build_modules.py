#!/usr/bin/env python3
"""Build modules.json from extracted .txt handleidingen and supplementary docs."""
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


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:60] or "section"


SECTION_RE = re.compile(r"^(\d+)\.\s+([A-ZÉÖa-zé].+)$")


def split_sections(text: str, title_prefix: str):
    """Split the handleiding text into top-level numbered sections."""
    lines = text.splitlines()
    # Skip the first three lines (title, subtitle, version)
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
        # Treat as top-level section only if number < 30 and line is short-ish
        if m and len(stripped) < 90 and not stripped.endswith(".csv'"):
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

    # Trim trailing footer lines (last section often contains author footer)
    out = []
    for s in sections:
        content = "\n".join(s["content_lines"]).strip()
        # Drop FAQ footer line that often appears at end
        content = re.sub(
            r"\n*Handleiding [^\n]+ v2\.0 — .+\n*Opgesteld door.+$",
            "",
            content,
            flags=re.MULTILINE,
        )
        out.append({"id": s["id"], "title": s["title"], "content": content.strip()})
    return out


modules = []
full_chatbot_kb = []

for spec in MODULES_SPEC:
    text = (EXTR / spec["file"]).read_text(encoding="utf-8")
    sections = split_sections(text, spec["title"])
    modules.append(
        {
            "id": spec["id"],
            "title": spec["title"],
            "icon": spec["icon"],
            "description": spec["description"],
            "sections": sections,
        }
    )
    full_chatbot_kb.append(f"\n\n=== MODULE: {spec['title']} ===\n")
    for s in sections:
        full_chatbot_kb.append(f"\n--- {s['title']} ---\n{s['content']}\n")

# Supplementary knowledge for chatbot only (not shown as modules)
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

result = {
    "modules": modules,
    "supplementary": "".join(supplementary),
}

Path("modules.json").write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
print(f"Modules: {len(modules)}")
for m in modules:
    print(f"  {m['icon']} {m['title']}: {len(m['sections'])} sections")
print(f"Total JSON: {len(json.dumps(result, ensure_ascii=False))} bytes")
