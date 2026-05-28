# Claude Code — Kwandoo Kennisbank v2 (Final)

## Context

The existing `Kwandoo_Kennisbank_v2.html` is working well. Now build two final production versions plus a supporting update file. All content, styling and features stay the same as the existing file — only the changes described below are new.

---

## Deliver three files

### 1. `kennisbank-updates.txt`
A plain text file that non-technical staff can edit directly in GitHub to add new content. Structure:

```
# Kwandoo Kennisbank — Updates door Kevin Samyn
# Voeg nieuwe procedures, problemen en oplossingen toe onderaan dit bestand.
# Elk blok begint met een datum. Gebruik de structuur hieronder als voorbeeld.
# Na het opslaan is de website automatisch bijgewerkt binnen 1-2 minuten.

--- Update [datum] ---
Onderwerp: [titel]
Probleem: [beschrijving van het probleem]
Oplossing: [stap-voor-stap oplossing]

--- Update [datum] ---
Onderwerp: [titel]
Nieuwe procedure: [beschrijving]
```

Leave the file with only the header comments and one example block — no real content yet.

### 2. `Kwandoo_Kennisbank_v2.html` (no chatbot — production version)

Take the existing `Kwandoo_Kennisbank_v2.html` and make these changes:

**Add: dynamic loading of `kennisbank-updates.txt`**

On page load, fetch `kennisbank-updates.txt` from the same directory using:
```javascript
fetch('./kennisbank-updates.txt')
  .then(r => r.text())
  .then(text => { /* store as updateContent */ })
  .catch(() => { /* silently ignore if file not found */ })
```

Show the updates content in a new section visible in the sidebar under a module called "📝 Updates & Nieuws". Each `--- Update [datum] ---` block becomes a collapsible card, same styling as the other sections (🔴/⚠️/✅ blocks supported).

**Remove: chatbot entirely**
- Remove the floating chat button (💬)
- Remove the chat panel
- Remove the "+ Kennisbank" header button
- Remove all localStorage chat/knowledge logic
- Remove the Anthropic API call

**Keep everything else exactly as-is.**

### 3. `Kwandoo_Kennisbank_v2_DEMO.html` (with chatbot — demo version)

Take the existing `Kwandoo_Kennisbank_v2.html` and make these changes:

**Add: dynamic loading of `kennisbank-updates.txt`** (same as above)

**Add: API key settings modal**

Add a gear icon (⚙️) button in the header, right of the "+ Kennisbank" button. Clicking it opens a modal with:
- Title: "API Instellingen"
- Explanation (Dutch): "Voer je Anthropic API-key in om de chatbot te activeren. De key wordt lokaal opgeslagen in je browser en nergens naartoe verstuurd."
- Input field: type="password", placeholder="sk-ant-..."
- Save button: "Opslaan" (stores to localStorage key 'kwandoo-api-key')
- Clear button: "Verwijder key"
- Status indicator: green "✅ API key actief" or red "❌ Geen API key ingesteld"
- Close button

**Modify: chatbot API call**

Read the API key from localStorage('kwandoo-api-key') and add it as a header:
```javascript
headers: {
  'Content-Type': 'application/json',
  'x-api-key': apiKey,
  'anthropic-version': '2023-06-01',
  'anthropic-dangerous-direct-browser-access': 'true'
}
```

If no API key is set, show this Dutch message in the chat instead of calling the API:
"Geen API-key ingesteld. Klik op het ⚙️ icoon in de header om je Anthropic API-key in te voeren."

**Add: updates content to chatbot knowledge**

Append the loaded `kennisbank-updates.txt` content to the chatbot system prompt knowledge base, after the existing handleidingen content.

**Keep everything else exactly as-is.**

---

## GitHub Pages compatibility

Both HTML files must work when served via GitHub Pages at:
`https://[username].github.io/Kwandoo/`

This means:
- All paths must be relative (`./kennisbank-updates.txt`, not `/kennisbank-updates.txt`)
- No server-side dependencies
- The `fetch()` for `kennisbank-updates.txt` must handle CORS gracefully (GitHub Pages serves files with correct headers, so this works)
- For local file:// opening: the fetch will fail silently due to browser CORS restrictions — this is acceptable, show a subtle note in the Updates section: "Updates laden enkel via de webversie. Open de website via de GitHub Pages URL."

---

## Step-by-step for Claude Code

1. Read the existing `Kwandoo_Kennisbank_v2.html` fully
2. Create `kennisbank-updates.txt` with the template structure
3. Build `Kwandoo_Kennisbank_v2.html` (no chatbot + updates loader)
4. Build `Kwandoo_Kennisbank_v2_DEMO.html` (with chatbot + API key modal + updates loader)
5. Commit and push all three files to the current branch

## Critical notes

- Do NOT rewrite the entire HTML from scratch — modify the existing file
- Do NOT change any existing styling, colors, fonts or layout
- Do NOT change any existing module content or section rendering
- The updates section styling must match the existing section cards exactly
- Test that both files are valid HTML before committing
