# Claude Code (Opus) — Kwandoo Knowledge Base & Chatbot

## Project context

Build a complete internal knowledge base website with integrated AI chatbot for the Leisure Services Department (Dienst Vrije Tijd) of the municipality of Ingelmunster, Belgium. The tool is used by staff who work daily with Kwandoo — an online registration system for after-school care, holiday camps, sports activities and day trips.

Two prototype files exist already (`Kwandoo_Kennisbank.html` and `Kwandoo_Helpdesk_Chatbot.html`). Use them as style and structure references only. Build everything from scratch — cleaner, more complete, more functional.

**All UI text, content, chatbot responses and labels must be in Dutch (Belgian Dutch).** Only this prompt and code comments are in English.

---

## Technical requirements

Deliver a **single self-contained HTML file** that opens directly in Chrome/Edge without any server, build step or installation. Use the `web-artifacts-builder` skill (React 18 + TypeScript + Vite + Tailwind + shadcn/ui) and bundle everything into one HTML file via the skill's bundle script.

The file must work fully offline except for:
- Google Fonts (Nunito, loaded via CDN link)
- Anthropic API calls for the chatbot (requires internet)

All content, styles and logic must be inlined in the single HTML file.

---

## Features — complete specification

### 1. Layout & navigation
- Fixed left sidebar (230px wide) listing all 7 modules
- Each module is a clickable item; clicking expands its subsections inline below it
- Active module and active subsection are visually highlighted
- Sidebar is collapsible via a hamburger button in the header
- Main content area scrolls independently of the sidebar
- Header fixed at top: logo + title + search bar + "Kennisbank +" button

### 2. Search
- Search input in the header, full width up to 480px
- Starts searching at 2 characters, live results replace the main content area
- Each result card shows: module emoji + module tag (green badge) + section title + content preview (first 220 chars)
- Search terms highlighted in yellow in results (like Google)
- Clicking a result navigates to that module+section and clears the search
- Pressing Escape clears the search
- "X results for [query]" shown above results
- Empty state with magnifying glass emoji if no results

### 3. Manual content display
- Sections rendered as collapsible cards
- Section header: title left, ▲/▼ chevron right, light blue background when active
- Section body always visible (no collapse needed — keep all sections open by default)
- Three special block types rendered with colored left borders + tinted backgrounds:
  - Lines starting with `🔴` → red left border (#C62828), background #FFEBEE, text in red
  - Lines starting with `⚠️` → orange left border (#F57C00), background #FFF3E0, text in orange
  - Lines starting with `✅` → green left border (#2E7D32), background #E8F5E9, text in green
- Numbered steps (`1.`, `2.`, etc.) have slight left indent
- Bullet points (`•`, `-`) have slight left indent
- Blank lines become 6px spacers
- Tables in content are rendered as proper HTML `<table>` elements with header row styling
- Quick-link chips below the module title jump to subsections on click

### 4. Floating chatbot button
- Fixed position: bottom 24px, right 24px
- 56×56px circle, gradient background: `linear-gradient(135deg, #2D6A4F, #1A237E)`
- Chat bubble emoji (💬) centered, font-size 22px
- Box shadow: `0 4px 20px rgba(0,0,0,0.25)`
- Scale to 1.1 on hover (CSS transition)
- Hidden when chat panel is open

### 5. Chat panel
- Fixed position: bottom 24px, right 24px
- Dimensions: 390px wide × 570px tall
- Border-radius 16px, white background, subtle border
- Box shadow: `0 8px 40px rgba(0,0,0,0.2)`

**Panel header:**
- Gradient background matching the floating button
- Robot avatar (🤖) in a semi-transparent rounded square
- Title: "Kwandoo Assistent" (bold, white, 14px)
- Subtitle: green dot + "Online" (11px, semi-transparent white)
- Right side: "📥 Export" button + "×" close button

**Messages area:**
- User messages: right-aligned, blue background (#1A237E), white text, rounded corners (14px 4px 14px 14px)
- Assistant messages: left-aligned, light grey background (#F1F3F4), dark text, rounded corners (4px 14px 14px 14px)
- Each message has a small avatar circle (👤 for user, 🤖 for assistant)
- Auto-scroll to latest message
- Typing indicator: three bouncing grey dots while waiting for API response

**Input area:**
- Textarea (1 row, resizable) + send button (➤)
- Send on Enter; Shift+Enter = new line
- Send button uses gradient when input has text, grey when empty
- Disabled while loading

### 6. Chatbot — API integration

Call `https://api.anthropic.com/v1/messages` with:
```javascript
{
  model: "claude-sonnet-4-20250514",
  max_tokens: 1000,
  system: SYSTEM_PROMPT, // see §Chatbot system prompt below
  messages: conversationHistory // full history for context
}
```

No API key needed in the code — it is injected automatically by the proxy.

Keep the full conversation history in React state and send it with every request.

Handle errors gracefully: show a Dutch error message in the chat on network failure.

### 7. Conversation logging
- Save every conversation to `localStorage` under key `kwandoo-chatbot-logs`
- Each entry: `{ id, startTime, messages: [{role, content, timestamp}] }`
- Maximum 100 conversations (drop oldest when limit exceeded)
- Export button in chat header downloads all logs as CSV:
  - Columns: `Tijdstip`, `Rol`, `Bericht`
  - Filename: `kwandoo-chatlog-YYYY-MM-DD.csv`
  - UTF-8 BOM included for correct Excel rendering

### 8. Knowledge base extension (admin feature)
- Button "+ Kennisbank" in the page header (right side)
- Opens a modal overlay (540px wide)
- Textarea for entering new information (procedures, FAQ answers, new agreements)
- Saves to `localStorage` under key `kwandoo-extra-knowledge`
- Extra knowledge is appended to every chatbot system prompt automatically
- Shows count of active knowledge blocks when content exists
- "Wissen" button to clear all extra knowledge

---

## Brand & visual design

```
Primary green:    #2D6A4F  (Gemeente Ingelmunster)
Secondary green:  #40916C
Blue:             #1A237E  (Kwandoo)
Header gradient:  linear-gradient(135deg, #2D6A4F 0%, #40916C 50%, #1A237E 100%)
Page background:  #F8F9FA
Card background:  #FFFFFF
Card border:      #E8EAED
Border radius:    12px (cards), 8px (buttons), 10px (inputs)
Font:             Nunito (Google Fonts) — weights 400, 600, 700, 800, 900
Scrollbar:        6px wide, color #dadce0
```

**Logo in header:** White rounded square (34×34px, border-radius 8px) containing the text "4i" in #2D6A4F, bold — this is the Ingelmunster municipality logo.

**Sidebar active states:**
- Active module: green left border (3px, #2D6A4F) + light green background (#F0FAF3)
- Active subsection: blue left border (3px, #1A237E) + light blue background (#E8EAF6)

---

## Chatbot system prompt

Use this exact Dutch system prompt in every API call (replace `{KNOWLEDGE}` dynamically):

```
Je bent een behulpzame interne assistent voor medewerkers van de Dienst Vrije Tijd van gemeente Ingelmunster. Je helpt hen met het gebruik van Kwandoo, het online inschrijvingssysteem voor speelpleinwerking, opvang, sportkampen en uitstappen.

Richtlijnen:
- Antwoord altijd in het Nederlands
- Wees kort en praktisch — medewerkers zitten midden in hun werk
- Verwijs naar concrete stappen uit de handleiding waar mogelijk
- Als je het antwoord niet zeker weet, zeg dat dan eerlijk
- Gebruik opsommingstekens voor stappen
- Verwijs bij complexe procedures naar de volledige handleiding

Bekende valkuilen — vermeld altijd als relevant:
- Standaarddienst staat op 'Bibliotheek' bij nieuwe activiteit — altijd aanpassen naar de juiste dienst
- Betaler werkt NIET retroactief — stel betalers in vóór je opvanginschrijvingen aanmaakt
- 'Publiceer activiteit' vergeten na bewerken = activiteit onzichtbaar voor ouders
- PDF's worden niet automatisch vernieuwd na facturatiewijziging — altijd handmatig hergenereren
- 'Aanmelden als ouder' = live omgeving, ook vanuit testomgeving — alle acties zijn echt

[KENNISBANK]
{KNOWLEDGE}
[/KENNISBANK]
```

Build a `buildKnowledgeBase(extraKnowledge: string): string` function that:
1. Concatenates all module content (title + sections with their full text)
2. Appends `extraKnowledge` from localStorage if present
3. Returns the full string to inject into `{KNOWLEDGE}`

---

## Content data — the 7 modules

Read ALL content from the v4 `.docx` files listed in §Files. Use `extract-text` or Python XML parsing to extract the full text including tables, warnings and tips. Do not summarize or shorten — include everything.

Structure the content as:
```typescript
interface Section { id: string; title: string; content: string }
interface Module { id: string; title: string; icon: string; description: string; sections: Section[] }
```

The 7 modules:
| # | Icon | Dutch title | Description |
|---|------|-------------|-------------|
| 1 | 🎯 | Activiteiten | Aanmaken, bewerken, dupliceren en beheren van activiteiten |
| 2 | 📋 | Inschrijvingen & Deelnemers | Loket, inschrijvingen beheren, kind- en ouderprofielen |
| 3 | ⏱️ | Opvang & Tijdsregistraties | Tijdsregistraties, noodopvang, aftekenlijst en datavalidatie |
| 4 | 💶 | Facturatie & Betalingen | Facturatieruns, herinneringen, terugbetalingen en tarieven |
| 5 | 📊 | Rapportering | Rapporten genereren, Kind & Gezin, inschrijvingslijsten |
| 6 | ✉️ | Communicatie | Mailings, communicaties en GDPR-e-mails |
| 7 | ⚙️ | Gebruikers & Organisaties | Gebruikersbeheer, rollen, platformconfiguratie en GDPR |

---

## Files to read

All files are in the current working directory. Use bash to read them — do not ask the user to upload anything.

**Recommended extraction method for .docx files:**
```bash
# Option 1 — if extract-text is available:
extract-text Handleiding_activiteiten_v4_mei2026.docx

# Option 2 — Python fallback:
python3 -c "
import zipfile, re
with zipfile.ZipFile('Handleiding_activiteiten_v4_mei2026.docx') as z:
    xml = z.read('word/document.xml').decode('utf-8', errors='ignore')
    texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', xml)
    print(' '.join(texts))
"
```

Run `ls *.docx *.html` first to confirm all files are present before starting.

**Primary — v4 handleidingen (read fully, use as module content):**
```
Handleiding_activiteiten_v4_mei2026.docx
Handleiding_inschrijvingen_deelnemers_v4_mei2026.docx
Handleiding_opvang_tijdsregistraties_v4_mei2026.docx
Handleiding_facturatie_betalingen_v4_mei2026.docx
Handleiding_rapportering_v4_mei2026.docx
Handleiding_communicatie_v4_mei2026.docx
Handleiding_gebruikers_organisaties_v4_mei2026.docx
```

**Supplementary — additional chatbot knowledge (read and append to knowledge base string):**
```
Overzicht_Automatische_Emails_Kwandoo.docx       — which emails fire when
Rollenmatrix_Kwandoo_Ingelmunster.docx            — roles and permissions per function
Template_herinneringsmails.docx                   — reminder email templates
ASIS_Kwandoo_Medewerkersperspectief_v3.docx       — known pain points and context
TOBE_Kwandoo_v2_mei2026.docx                     — status per pain point + recommendations
Verslag_gesprek_20mei2026.docx                    — decisions and agreements (May 2026)
Verslag_gesprek_12_mei.docx                       — decisions and agreements (May 2026)
Uitleg_en_oplossing__emails__en_gdpr_toestanden.docx — GDPR explanation
```

**Reference only (open and read for style/structure inspiration — do not copy content):**
```
Kwandoo_Helpdesk_Chatbot.html    — existing chatbot UI reference
Kwandoo_Kennisbank.html          — existing knowledge base prototype reference
```

---

## Step-by-step instructions for Claude Code

1. **Verify files** — run `ls *.docx *.html` to confirm all required files are present in the working directory.
2. **Read all v4 handleidingen** — use `extract-text` or the Python zipfile method shown in §Files. Read each file in full and store the text per module. Do not truncate.
3. **Read all supplementary files** — extract text from each and concatenate into a single `supplementaryKnowledge` string.
4. **Initialize the React project** — run `bash /mnt/skills/examples/web-artifacts-builder/scripts/init-artifact.sh kwandoo-kennisbank` and `cd kwandoo-kennisbank`.
5. **Write `src/data/modules.ts`** — structure all extracted handleiding content as TypeScript Module/Section constants. Full text, nothing omitted.
6. **Build `src/App.tsx`** — implement all features from this spec.
7. **Handle pnpm build scripts** — if pnpm warns about ignored build scripts, run `pnpm approve-builds` or use `npx vite build` directly.
8. **Bundle** — run `bash /mnt/skills/examples/web-artifacts-builder/scripts/bundle-artifact.sh` or `npx vite build --outDir dist-bundle`.
9. **Inline into one file** — use Node.js to read `dist-bundle/index.html`, inline the CSS and JS, and write the result as `Kwandoo_Kennisbank_v2.html`.
10. **Verify** — open the file and confirm search works for "loket", "facturatie" and "noodopvang".

**Critical implementation notes:**
- Do NOT use `<form>` tags anywhere — use `onClick` handlers
- localStorage works correctly in locally opened HTML files
- No API key in the code — the proxy injects it automatically
- Google Fonts CDN link is the only allowed external dependency besides the API
- After bundling, verify the file opens correctly by checking for obvious errors
- Test search with at least 3 queries: "loket", "facturatie", "noodopvang"
- All Dutch special characters (é, ë, ï, ij, oe, etc.) must render correctly — use UTF-8

---

## Expected output

**Filename:** `Kwandoo_Kennisbank_v2.html`
**Size:** 400–700KB (all content inlined)
**Compatibility:** Chrome 100+, Edge 100+
**Requirement:** Opens and works fully by double-clicking — no server, no npm, no installation
