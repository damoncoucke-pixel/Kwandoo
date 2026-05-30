# OneDrive structuur

De exacte mapstructuur per klant. Maak deze identiek aan voor elke klant. Geen afwijkingen, geen creativiteit. Voorspelbaarheid zodat elk teamlid weet waar wat staat.

---

## Mapstructuur per klant

```
Kolme/Klanten/[Klantnaam]/
├── Briefing.md                                  (output skill kolme-intake)
├── Scope-document.docx                          (getekend, zie scope-template.md)
├── Facturen/
│   ├── [Klantnaam]-F2025-001-aanbetaling.pdf
│   └── [Klantnaam]-F2025-002-saldo.pdf
├── Communicatie/
│   ├── [datum]-eerste-contact.md
│   └── [datum]-oplevering.md
├── Website/
│   ├── broncode/                                (export uit Lovable)
│   └── screenshots/                             (desktop + mobiel bij oplevering)
└── Opgeleverd/
    └── [datum]-finale-url.md
```

---

## Wat komt waar

### Briefing.md
De ingevulde briefing uit skill kolme-intake. Dit is het startpunt van het dossier en de input voor de Lovable prompt.

### Scope-document.docx
Het getekende scope-document. Pas opslaan als het ondertekend is. Een ongetekende scope hoort niet in dit dossier maar in een aparte concept-versie tot ze getekend is.

### Facturen/
Alle facturen als PDF, met de vaste naamgeving:
`[Klantnaam]-F[jaar]-[volgnummer]-[type].pdf`
- Voorbeeld: `SalonLieve-F2025-001-aanbetaling.pdf`
- Voorbeeld: `SalonLieve-F2025-002-saldo.pdf`

### Communicatie/
Belangrijke contactmomenten als markdown of opgeslagen mail, met de datum vooraan:
`[datum]-[onderwerp].md`
- Voorbeeld: `2025-03-12-eerste-contact.md`
- Voorbeeld: `2025-04-02-oplevering.md`

Niet elke mail bewaren, wel de mijlpalen: eerste contact, bevestiging, oplevering, belangrijke afspraken.

### Website/broncode/
De export uit Lovable. Doe dit bij oplevering en bij elke grote wijziging. Dit is het vangnet als er iets misgaat.

### Website/screenshots/
Screenshots van de opgeleverde site, desktop én mobiel. Bewijs van de staat bij oplevering en handig voor het portfolio.

### Opgeleverd/
De finale URL en opleveringsdetails:
`[datum]-finale-url.md`
Bevat: de live URL, de opleveringsdatum, de SEO-nulmeting (positie en snelheid), en welk pakket geleverd is.

---

## Naamgevingsregels

- **Klantnaam:** consistent schrijven, zonder spaties in bestandsnamen waar mogelijk (SalonLieve, niet "Salon Lieve").
- **Datums:** altijd als JJJJ-MM-DD, zodat bestanden chronologisch sorteren.
- **Facturen:** altijd het volgnummer en het type erbij.

## Regels

1. **Maak de volledige structuur aan bij een nieuwe klant**, ook de lege mappen. Zo is er altijd een vaste plek.
2. **Sla onderweg op, niet achteraf.** Een dossier dat je pas op het einde vult, mist altijd iets.
3. **Eén klant, één map.** Geen gedeelde bestanden tussen klanten.
4. **De broncode is heilig.** Exporteer bij elke oplevering, zodat je nooit afhankelijk bent van enkel Lovable.
