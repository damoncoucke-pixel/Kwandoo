# Prompt architectuur

De vaste basisstructuur die elke Lovable prompt volgt. Schrijf de prompt in het Engels. De zichtbare website-copy vraag je in het Nederlands (of NL+EN volgens briefing). Bouw de prompt op in deze blokken, in deze volgorde.

---

## Blok 0 — Opening en context

Begin elke prompt met wie de klant is en wat de site moet doen. Eén of twee zinnen in het Engels.

> Build a website for [business name], a [sector] in [municipality], Belgium. The business is [unique angle in one line]. The main goal of the site is to get visitors to [primary action].

## Blok 1 — Technisch blok (altijd identiek)

Plak dit blok in elke prompt:

> Technical requirements:
> - React with Tailwind CSS
> - Mobile-first, fully responsive (test at 375px, 768px, 1280px)
> - Sticky navigation bar that stays visible on scroll
> - Smooth scroll to anchor sections
> - Phone numbers as clickable tel: links everywhere they appear
> - Contact form with client-side validation (required fields, valid email)
> - No Lovable badge
> - No dark mode unless explicitly requested
> - Fast loading: optimize images, no heavy libraries
> - Accessible: proper heading hierarchy, alt text on every image, sufficient color contrast

## Blok 2 — Onepager vs multipage beslisboom

Bepaal het type en zet het in de prompt.

**Onepager** wanneer:
- Pakket = Starter
- Eenvoudige zaak met een duidelijke hoofdactie
- 3 diensten of minder
- Klant wil iets simpels en snel vindbaar

**Multipage** wanneer:
- Pakket = Pro of Premium
- Meer dan 3 diensten die elk uitleg verdienen
- Boekings- of reservatiesysteem
- Klant wil per dienst of doelgroep een aparte pagina
- SEO over meerdere zoekwoorden gewenst (aparte pagina's ranken op aparte termen)

Twijfel tussen de twee bij Pro? Kies multipage als er meer dan 3 diensten zijn, anders een lange onepager met anchor-navigatie.

In de prompt schrijf je expliciet: "Build this as a single-page site with anchor navigation" of "Build this as a multi-page site with these pages: [...]".

## Blok 3 — Taalblok

- Standaard: alle zichtbare copy in het Nederlands.
- EN-toggle alleen als de briefing buitenlandse klanten vermeldt.

> Language: all visible copy in Dutch (Flemish, informal "je/jij" tone unless stated otherwise).

Met EN-toggle:

> Add a language toggle (NL/EN) in the top right of the navigation. Default language is Dutch. Provide an English translation of all content. Persist the choice during the session.

## Blok 4 — Kleurenpalet blok

Neem het palet uit `sectorpaletten.md`. Geef altijd hex-codes mee.

> Color palette:
> - Primary: [hex] ([name/use])
> - Accent: [hex] ([name/use])
> - Background: [hex]
> - Text: [hex]
> Use these consistently. Do not give every section a different background color. Let white space breathe.

## Blok 5 — Secties blok

Exacte volgorde uit `sectie-templates.md` voor deze sector. Beschrijf per sectie wat erin komt, met de echte copy of een duidelijke instructie voor de copy. Verwijs naar echte foto's waar mogelijk (placeholder met instructie als de klant nog moet aanleveren).

## Blok 6 — Copy principes blok (altijd)

Plak een verkorte versie van `copy-regels.md`:

> Copy principles:
> - Speak to the visitor (je/jij), not about the business
> - Benefits over features
> - No corporate jargon, no buzzwords
> - Never use dashes as punctuation marks in the copy
> - Short sentences
> - One strong headline that names the visitor's situation or need
> - Every CTA is benefit-driven, not "Submit"

## Blok 7 — Footer blok

**Onepager:** AV, PV en cookiebeleid als anchor-secties onderaan, of als modals/aparte ankers. Volledige teksten uit `av-pv-cookie-templates.md`, placeholders ingevuld.

> Footer: business name, address, phone (tel: link), email, opening hours. Below that, links to Algemene Voorwaarden, Privacyverklaring and Cookiebeleid as anchor sections (or accessible pages). Include the full legal text provided below.

**Multipage:** AV, PV en cookiebeleid als aparte pagina's met volledige inhoud.

> Create separate pages for Algemene Voorwaarden, Privacyverklaring and Cookiebeleid, each with the full text provided below. Link them from the footer on every page.

## Blok 8 — Cookiebanner (altijd)

> Cookie banner: show on first visit at the bottom of the screen. Two buttons: "Accepteren" and "Alleen noodzakelijk". Remember the choice. Link to the Cookiebeleid. Do not load analytics until consent is given.

---

## Volgorde van de prompt samengevat

1. Opening en context
2. Technisch blok
3. Onepager/multipage beslissing
4. Taalblok
5. Kleurenpalet
6. Secties (de body)
7. Copy principes
8. Footer
9. Cookiebanner
10. Juridische teksten (volledig, onderaan de prompt geplakt)
