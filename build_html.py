#!/usr/bin/env python3
"""Build Kwandoo_Kennisbank_v2.html — single self-contained HTML file."""
import json
from pathlib import Path

data = json.loads(Path("modules.json").read_text(encoding="utf-8"))
MODULES_JSON = json.dumps(data["modules"], ensure_ascii=False)
SUPPLEMENTARY_JSON = json.dumps(data["supplementary"], ensure_ascii=False)

SYSTEM_PROMPT = """Je bent een behulpzame interne assistent voor medewerkers van de Dienst Vrije Tijd van gemeente Ingelmunster. Je helpt hen met het gebruik van Kwandoo, het online inschrijvingssysteem voor speelpleinwerking, opvang, sportkampen en uitstappen.

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
[/KENNISBANK]"""

HTML = r"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kwandoo Kennisbank — Gemeente Ingelmunster</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; height: 100%; }
body {
  font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
  background: #F8F9FA;
  color: #202124;
  font-size: 14.5px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #dadce0; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #bdc1c6; }

/* ===== Header ===== */
.app-header {
  position: fixed; top: 0; left: 0; right: 0; height: 64px;
  background: linear-gradient(135deg, #2D6A4F 0%, #40916C 50%, #1A237E 100%);
  color: #fff;
  display: flex; align-items: center; gap: 16px;
  padding: 0 20px;
  z-index: 50;
  box-shadow: 0 2px 10px rgba(0,0,0,0.18);
}
.hamburger {
  width: 36px; height: 36px; border: none; background: rgba(255,255,255,0.12);
  color: #fff; border-radius: 8px; cursor: pointer; font-size: 18px;
  display: flex; align-items: center; justify-content: center;
  transition: background .15s;
}
.hamburger:hover { background: rgba(255,255,255,0.22); }

.brand { display: flex; align-items: center; gap: 12px; min-width: 0; }
.brand-logo {
  width: 34px; height: 34px; border-radius: 8px; background: #fff;
  color: #2D6A4F; font-weight: 900; font-size: 14px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.brand-text { line-height: 1.15; min-width: 0; }
.brand-text .title { font-weight: 800; font-size: 16px; white-space: nowrap; }
.brand-text .subtitle { font-size: 11px; opacity: 0.85; white-space: nowrap; }

.search-wrap {
  flex: 1; max-width: 480px; margin-left: auto; margin-right: 12px;
  position: relative;
}
.search-input {
  width: 100%; height: 38px;
  background: rgba(255,255,255,0.95); color: #202124;
  border: none; outline: none;
  border-radius: 10px; padding: 0 14px 0 40px;
  font-family: inherit; font-size: 14px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.search-input:focus { box-shadow: 0 0 0 3px rgba(255,255,255,0.35), 0 1px 3px rgba(0,0,0,0.1); }
.search-icon {
  position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
  font-size: 16px; opacity: 0.55; pointer-events: none;
}
.search-clear {
  position: absolute; right: 8px; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; font-size: 18px;
  color: #5f6368; padding: 4px 8px;
}

.add-kb-btn {
  height: 38px; padding: 0 14px; background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3); color: #fff; border-radius: 8px;
  cursor: pointer; font-family: inherit; font-weight: 700; font-size: 13px;
  white-space: nowrap; transition: background .15s;
}
.add-kb-btn:hover { background: rgba(255,255,255,0.28); }

/* ===== Layout ===== */
.layout {
  display: flex; height: 100vh; padding-top: 64px;
}
.sidebar {
  width: 230px; flex-shrink: 0;
  background: #fff; border-right: 1px solid #E8EAED;
  overflow-y: auto;
  transition: margin-left .22s ease;
}
.sidebar.collapsed { margin-left: -230px; }
.sidebar-inner { padding: 14px 10px; }
.sidebar-section-title {
  font-size: 10.5px; font-weight: 800; letter-spacing: 0.6px;
  color: #5f6368; text-transform: uppercase;
  padding: 6px 10px 8px;
}

.mod-item {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 10px; border-radius: 8px; cursor: pointer;
  color: #202124; font-weight: 600; font-size: 13.5px;
  border-left: 3px solid transparent;
  margin-bottom: 2px;
  transition: background .12s;
  user-select: none;
}
.mod-item:hover { background: #F1F3F4; }
.mod-item.active {
  background: #F0FAF3;
  border-left-color: #2D6A4F;
  font-weight: 800;
}
.mod-icon { font-size: 16px; }
.mod-label { flex: 1; min-width: 0; line-height: 1.2; }
.mod-chev { font-size: 10px; opacity: 0.55; transition: transform .15s; }
.mod-item.active .mod-chev { transform: rotate(90deg); }

.sub-list { padding: 2px 0 8px 8px; }
.sub-item {
  display: block; padding: 7px 10px 7px 24px;
  font-size: 12.8px; color: #3c4043;
  border-radius: 6px; cursor: pointer; margin-bottom: 1px;
  border-left: 3px solid transparent;
  line-height: 1.3;
}
.sub-item:hover { background: #F1F3F4; }
.sub-item.active {
  background: #E8EAF6;
  border-left-color: #1A237E;
  color: #1A237E; font-weight: 700;
}

/* ===== Main ===== */
.main {
  flex: 1; overflow-y: auto; padding: 28px 32px 80px;
  min-width: 0;
}
.main-inner { max-width: 920px; margin: 0 auto; }

.module-head {
  display: flex; gap: 16px; align-items: flex-start;
  margin-bottom: 8px;
}
.module-head .big-icon { font-size: 36px; line-height: 1; }
.module-head h1 {
  font-size: 26px; font-weight: 800; margin: 0; color: #1A237E;
}
.module-head p { color: #5f6368; margin: 4px 0 0; font-size: 14px; }

.quick-chips {
  display: flex; flex-wrap: wrap; gap: 8px;
  margin: 18px 0 22px;
}
.chip {
  background: #fff; border: 1px solid #E8EAED;
  padding: 6px 12px; border-radius: 999px; font-size: 12.5px;
  cursor: pointer; color: #3c4043; font-weight: 600;
  transition: all .15s;
}
.chip:hover {
  background: #F0FAF3; border-color: #2D6A4F; color: #2D6A4F;
}
.chip.active {
  background: #1A237E; border-color: #1A237E; color: #fff;
}

.section-card {
  background: #fff; border: 1px solid #E8EAED;
  border-radius: 12px; margin-bottom: 14px;
  overflow: hidden;
}
.section-header {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 18px;
  font-weight: 800; font-size: 15.5px; color: #202124;
  cursor: pointer; user-select: none;
  background: #fff;
  transition: background .15s;
}
.section-header.active { background: #E8EAF6; color: #1A237E; }
.section-header .sect-chev { margin-left: auto; font-size: 11px; opacity: 0.6; }
.section-body {
  padding: 6px 18px 16px;
  border-top: 1px solid #E8EAED;
}

/* Special blocks */
.note { padding: 10px 14px; border-left: 4px solid; border-radius: 6px; margin: 8px 0; font-size: 13.6px; line-height: 1.5; }
.note.red    { background: #FFEBEE; border-color: #C62828; color: #C62828; }
.note.orange { background: #FFF3E0; border-color: #F57C00; color: #B25500; }
.note.green  { background: #E8F5E9; border-color: #2E7D32; color: #1B5E20; }

.step { padding-left: 22px; margin: 3px 0; position: relative; }
.bullet { padding-left: 18px; margin: 3px 0; position: relative; }
.bullet::before { content: '•'; position: absolute; left: 6px; color: #2D6A4F; font-weight: 800; }
.content-table {
  border-collapse: collapse; width: 100%; margin: 10px 0;
  font-size: 13.2px; border-radius: 8px; overflow: hidden;
  border: 1px solid #E8EAED;
}
.content-table th, .content-table td {
  padding: 7px 11px; border: 1px solid #E8EAED; text-align: left; vertical-align: top;
}
.content-table th { background: #F0FAF3; color: #1B5E20; font-weight: 800; }

.para { margin: 4px 0; }
.spacer { height: 6px; }

mark.hl { background: #fff2a8; padding: 0 2px; border-radius: 2px; }

/* ===== Search results ===== */
.results-head { font-size: 13px; color: #5f6368; margin-bottom: 12px; font-weight: 600; }
.result-card {
  background: #fff; border: 1px solid #E8EAED; border-radius: 12px;
  padding: 14px 16px; margin-bottom: 12px; cursor: pointer;
  transition: border-color .15s, box-shadow .15s;
}
.result-card:hover { border-color: #2D6A4F; box-shadow: 0 2px 10px rgba(45,106,79,0.1); }
.result-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.result-tag {
  background: #E8F5E9; color: #1B5E20; padding: 2px 9px; border-radius: 999px;
  font-size: 11.5px; font-weight: 700;
}
.result-emoji { font-size: 14px; }
.result-title { font-weight: 800; font-size: 15px; margin: 4px 0; color: #1A237E; }
.result-preview { font-size: 13px; color: #3c4043; line-height: 1.45; }

.empty-state {
  text-align: center; padding: 60px 16px; color: #5f6368;
}
.empty-state .ico { font-size: 56px; opacity: 0.45; }
.empty-state .msg { font-size: 15px; font-weight: 700; margin-top: 10px; }
.empty-state .sub { font-size: 13px; margin-top: 4px; }

/* ===== Floating chat button ===== */
.fab {
  position: fixed; right: 24px; bottom: 24px;
  width: 56px; height: 56px; border-radius: 50%; border: none;
  background: linear-gradient(135deg, #2D6A4F, #1A237E);
  color: #fff; font-size: 22px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  transition: transform .18s;
  z-index: 60;
}
.fab:hover { transform: scale(1.1); }
.fab.hidden { display: none; }

/* ===== Chat panel ===== */
.chat-panel {
  position: fixed; right: 24px; bottom: 24px;
  width: 390px; height: 570px; max-height: calc(100vh - 48px);
  background: #fff; border-radius: 16px; border: 1px solid #E8EAED;
  box-shadow: 0 8px 40px rgba(0,0,0,0.2);
  z-index: 60;
  display: none; flex-direction: column; overflow: hidden;
}
.chat-panel.open { display: flex; }

.chat-header {
  background: linear-gradient(135deg, #2D6A4F, #1A237E);
  color: #fff;
  padding: 12px 14px;
  display: flex; align-items: center; gap: 10px;
  flex-shrink: 0;
}
.bot-avatar {
  width: 34px; height: 34px; border-radius: 9px;
  background: rgba(255,255,255,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
}
.bot-meta { line-height: 1.15; flex: 1; min-width: 0; }
.bot-meta .name { font-weight: 800; font-size: 14px; color: #fff; }
.bot-meta .status { font-size: 11px; opacity: 0.85; display: flex; align-items: center; gap: 5px; }
.dot-online { width: 7px; height: 7px; border-radius: 50%; background: #69F0AE; box-shadow: 0 0 0 2px rgba(105,240,174,0.4); }

.chat-head-btn {
  background: rgba(255,255,255,0.15); color: #fff; border: none;
  padding: 6px 10px; border-radius: 7px; cursor: pointer;
  font-family: inherit; font-size: 12px; font-weight: 700;
  display: flex; align-items: center; gap: 4px;
}
.chat-head-btn:hover { background: rgba(255,255,255,0.28); }
.chat-close {
  background: none; border: none; color: #fff;
  font-size: 22px; line-height: 1; cursor: pointer;
  padding: 2px 8px; border-radius: 6px;
}
.chat-close:hover { background: rgba(255,255,255,0.2); }

.messages {
  flex: 1; overflow-y: auto; padding: 14px 14px 6px;
  background: #FAFBFC;
  display: flex; flex-direction: column; gap: 10px;
}
.msg-row { display: flex; gap: 8px; align-items: flex-end; max-width: 100%; }
.msg-row.user { justify-content: flex-end; }
.msg-avatar {
  width: 26px; height: 26px; border-radius: 50%;
  background: #E8EAED; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px;
}
.bubble {
  max-width: 78%; padding: 9px 12px; font-size: 13.3px; line-height: 1.45;
  word-wrap: break-word; white-space: pre-wrap;
}
.msg-row.user .bubble {
  background: #1A237E; color: #fff;
  border-radius: 14px 4px 14px 14px;
}
.msg-row.assistant .bubble {
  background: #F1F3F4; color: #202124;
  border-radius: 4px 14px 14px 14px;
}
.msg-row.assistant .msg-avatar { background: linear-gradient(135deg, #2D6A4F, #1A237E); color: #fff; }
.typing { display: flex; gap: 4px; padding: 4px 0; }
.typing span { width: 7px; height: 7px; border-radius: 50%; background: #9aa0a6; animation: bounce 1s infinite; }
.typing span:nth-child(2) { animation-delay: .15s; }
.typing span:nth-child(3) { animation-delay: .30s; }
@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.6; }
  30% { transform: translateY(-5px); opacity: 1; }
}

.chat-input-row {
  display: flex; gap: 8px; padding: 10px 12px;
  background: #fff; border-top: 1px solid #E8EAED;
  flex-shrink: 0;
}
.chat-input {
  flex: 1; min-height: 38px; max-height: 110px;
  border: 1px solid #E8EAED; border-radius: 10px;
  padding: 9px 12px; font-family: inherit; font-size: 13.5px;
  resize: none; outline: none;
  background: #FAFBFC;
}
.chat-input:focus { border-color: #2D6A4F; background: #fff; }
.send-btn {
  width: 40px; height: 40px; flex-shrink: 0;
  border: none; border-radius: 10px; cursor: pointer;
  background: #DADCE0; color: #5f6368; font-size: 17px;
  display: flex; align-items: center; justify-content: center;
  transition: background .15s;
}
.send-btn.active {
  background: linear-gradient(135deg, #2D6A4F, #1A237E); color: #fff;
}
.send-btn:disabled { opacity: 0.55; cursor: not-allowed; }

/* ===== Modal (kennisbank uitbreiden) ===== */
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,0.42);
  z-index: 70; display: none;
  align-items: center; justify-content: center;
  padding: 16px;
}
.modal-backdrop.open { display: flex; }
.modal {
  background: #fff; border-radius: 14px; width: 100%; max-width: 540px;
  padding: 22px 24px; box-shadow: 0 16px 50px rgba(0,0,0,0.25);
}
.modal h2 { margin: 0 0 4px; font-size: 19px; color: #1A237E; }
.modal .desc { color: #5f6368; font-size: 13px; margin-bottom: 14px; }
.modal textarea {
  width: 100%; min-height: 180px;
  border: 1px solid #E8EAED; border-radius: 10px;
  padding: 12px; font-family: inherit; font-size: 13.5px;
  resize: vertical; outline: none; background: #FAFBFC;
}
.modal textarea:focus { border-color: #2D6A4F; }
.modal-actions {
  display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap;
}
.btn-primary {
  background: linear-gradient(135deg, #2D6A4F, #1A237E);
  color: #fff; border: none; padding: 10px 18px;
  border-radius: 8px; font-family: inherit; font-weight: 700;
  cursor: pointer; font-size: 13.5px;
}
.btn-secondary {
  background: #fff; color: #3c4043; border: 1px solid #DADCE0;
  padding: 10px 16px; border-radius: 8px; font-family: inherit;
  font-weight: 700; cursor: pointer; font-size: 13.5px;
}
.btn-danger {
  background: #fff; color: #C62828; border: 1px solid #F8BBD0;
  padding: 10px 16px; border-radius: 8px; font-family: inherit;
  font-weight: 700; cursor: pointer; font-size: 13.5px;
}
.kb-count {
  margin-left: auto; font-size: 12px; color: #5f6368; align-self: center;
  font-weight: 600;
}

@media (max-width: 720px) {
  .sidebar { position: fixed; top: 64px; bottom: 0; left: 0; z-index: 40; }
  .sidebar.collapsed { margin-left: -260px; }
  .main { padding: 22px 18px 80px; }
  .chat-panel { width: calc(100vw - 24px); right: 12px; bottom: 12px; height: calc(100vh - 88px); }
  .fab { right: 16px; bottom: 16px; }
  .brand-text .subtitle { display: none; }
}
</style>
</head>
<body>

<header class="app-header">
  <button class="hamburger" id="hamburger" aria-label="Toon/verberg menu">☰</button>
  <div class="brand">
    <div class="brand-logo">4i</div>
    <div class="brand-text">
      <div class="title">Kwandoo Kennisbank</div>
      <div class="subtitle">Dienst Vrije Tijd — Gemeente Ingelmunster</div>
    </div>
  </div>
  <div class="search-wrap">
    <span class="search-icon">🔍</span>
    <input id="searchInput" class="search-input" type="text" placeholder="Zoek in de kennisbank…" autocomplete="off">
    <button id="searchClear" class="search-clear" style="display:none">×</button>
  </div>
  <button class="add-kb-btn" id="openModalBtn">＋ Kennisbank</button>
</header>

<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-inner">
      <div class="sidebar-section-title">Modules</div>
      <nav id="modList"></nav>
    </div>
  </aside>
  <main class="main" id="main">
    <div class="main-inner" id="mainInner"></div>
  </main>
</div>

<button class="fab" id="fab" aria-label="Open Kwandoo Assistent">💬</button>

<section class="chat-panel" id="chatPanel" aria-label="Kwandoo Assistent">
  <div class="chat-header">
    <div class="bot-avatar">🤖</div>
    <div class="bot-meta">
      <div class="name">Kwandoo Assistent</div>
      <div class="status"><span class="dot-online"></span>Online</div>
    </div>
    <button class="chat-head-btn" id="exportLogsBtn" title="Exporteer alle gesprekken als CSV">📥 Export</button>
    <button class="chat-close" id="closeChatBtn" aria-label="Sluit chat">×</button>
  </div>
  <div class="messages" id="messages"></div>
  <div class="chat-input-row">
    <textarea id="chatInput" class="chat-input" rows="1" placeholder="Stel een vraag…"></textarea>
    <button class="send-btn" id="sendBtn" aria-label="Verzend">➤</button>
  </div>
</section>

<div class="modal-backdrop" id="modalBackdrop">
  <div class="modal" role="dialog" aria-modal="true">
    <h2>Kennisbank uitbreiden</h2>
    <p class="desc">Voeg extra informatie toe (procedures, FAQ-antwoorden, nieuwe afspraken). Deze tekst wordt automatisch aan de chatbot meegegeven bij elke vraag.</p>
    <textarea id="extraKbInput" placeholder="Bv. nieuwe afspraak rond herinneringsfrequentie, contactgegevens, FAQ…"></textarea>
    <div class="modal-actions">
      <button class="btn-primary" id="saveKbBtn">Opslaan</button>
      <button class="btn-secondary" id="closeModalBtn">Annuleren</button>
      <button class="btn-danger" id="clearKbBtn">Wissen</button>
      <span class="kb-count" id="kbCount"></span>
    </div>
  </div>
</div>

<script>
"use strict";
const MODULES = __MODULES_JSON__;
const SUPPLEMENTARY = __SUPPLEMENTARY_JSON__;
const SYSTEM_PROMPT_TEMPLATE = __SYSTEM_PROMPT__;

// ===== State =====
const state = {
  activeModuleId: MODULES[0].id,
  activeSectionId: null,
  sidebarCollapsed: false,
  searchQuery: "",
  conversation: [],
  loading: false,
};

// ===== Utils =====
function $(sel) { return document.querySelector(sel); }
function $$(sel) { return Array.from(document.querySelectorAll(sel)); }
function el(tag, attrs, ...children) {
  const e = document.createElement(tag);
  if (attrs) {
    for (const k in attrs) {
      if (k === "class") e.className = attrs[k];
      else if (k === "html") e.innerHTML = attrs[k];
      else if (k.startsWith("on") && typeof attrs[k] === "function") e.addEventListener(k.slice(2), attrs[k]);
      else if (attrs[k] !== false && attrs[k] != null) e.setAttribute(k, attrs[k]);
    }
  }
  for (const c of children) {
    if (c == null || c === false) continue;
    if (typeof c === "string") e.appendChild(document.createTextNode(c));
    else e.appendChild(c);
  }
  return e;
}
function escHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function escAttr(s) { return escHtml(s).replace(/"/g, "&quot;"); }
function highlight(text, query) {
  if (!query || query.length < 2) return escHtml(text);
  const re = new RegExp("(" + query.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&") + ")", "gi");
  return escHtml(text).replace(re, '<mark class="hl">$1</mark>');
}
function getModule(id) { return MODULES.find(m => m.id === id) || MODULES[0]; }

// ===== Content rendering =====
// Renders a section's content as HTML, handling 🔴 ⚠️ ✅ blocks, numbered steps,
// bullet points, blank-line spacers and simple table detection.
function renderContent(text) {
  if (!text) return "";
  const lines = text.split(/\r?\n/);
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const raw = lines[i];
    const line = raw.trim();
    if (!line) {
      out.push('<div class="spacer"></div>');
      i++;
      continue;
    }
    // Special blocks
    if (line.startsWith("🔴")) {
      out.push('<div class="note red">' + escHtml(line.replace(/^🔴\s*/, "🔴 ")) + "</div>");
      i++; continue;
    }
    if (line.startsWith("⚠️")) {
      out.push('<div class="note orange">' + escHtml(line.replace(/^⚠️\s*/, "⚠️ ")) + "</div>");
      i++; continue;
    }
    if (line.startsWith("✅")) {
      out.push('<div class="note green">' + escHtml(line.replace(/^✅\s*/, "✅ ")) + "</div>");
      i++; continue;
    }
    // Numbered steps
    if (/^\d+\.\s/.test(line) && line.length < 250) {
      out.push('<div class="step">' + escHtml(line) + "</div>");
      i++; continue;
    }
    // Bullets
    if (/^[•\-\*]\s/.test(line)) {
      out.push('<div class="bullet">' + escHtml(line.replace(/^[•\-\*]\s+/, "")) + "</div>");
      i++; continue;
    }
    // Sub-heading like "2.1 Stap voor stap"
    if (/^\d+\.\d+\b/.test(line) && line.length < 100) {
      out.push('<div class="para" style="font-weight:800;color:#1A237E;margin-top:10px">' + escHtml(line) + "</div>");
      i++; continue;
    }
    // Plain paragraph
    out.push('<div class="para">' + escHtml(line) + "</div>");
    i++;
  }
  return out.join("");
}

// ===== Sidebar =====
function renderSidebar() {
  const nav = $("#modList");
  nav.innerHTML = "";
  for (const m of MODULES) {
    const isActive = m.id === state.activeModuleId;
    const item = el("div", { class: "mod-item" + (isActive ? " active" : ""), onclick: () => selectModule(m.id) },
      el("span", { class: "mod-icon" }, m.icon),
      el("span", { class: "mod-label" }, m.title),
      el("span", { class: "mod-chev" }, "▸")
    );
    nav.appendChild(item);
    if (isActive) {
      const sub = el("div", { class: "sub-list" });
      for (const s of m.sections) {
        const sActive = state.activeSectionId === s.id;
        sub.appendChild(el("div", {
          class: "sub-item" + (sActive ? " active" : ""),
          onclick: (e) => { e.stopPropagation(); selectSection(m.id, s.id); }
        }, s.title));
      }
      nav.appendChild(sub);
    }
  }
}

function selectModule(id) {
  state.activeModuleId = id;
  state.activeSectionId = null;
  state.searchQuery = "";
  $("#searchInput").value = "";
  $("#searchClear").style.display = "none";
  renderSidebar();
  renderMain();
  $("#main").scrollTop = 0;
}

function selectSection(modId, sectId) {
  state.activeModuleId = modId;
  state.activeSectionId = sectId;
  state.searchQuery = "";
  $("#searchInput").value = "";
  $("#searchClear").style.display = "none";
  renderSidebar();
  renderMain();
  setTimeout(() => {
    const target = document.getElementById("sect-" + sectId);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 30);
}

// ===== Main content =====
function renderMain() {
  const root = $("#mainInner");
  root.innerHTML = "";
  if (state.searchQuery.length >= 2) {
    renderSearchResults(root);
    return;
  }
  const mod = getModule(state.activeModuleId);
  const head = el("div", { class: "module-head" },
    el("div", { class: "big-icon" }, mod.icon),
    el("div", null,
      el("h1", null, mod.title),
      el("p", null, mod.description)
    )
  );
  root.appendChild(head);

  // Quick chips
  const chips = el("div", { class: "quick-chips" });
  for (const s of mod.sections) {
    chips.appendChild(el("div", {
      class: "chip" + (state.activeSectionId === s.id ? " active" : ""),
      onclick: () => selectSection(mod.id, s.id)
    }, s.title));
  }
  root.appendChild(chips);

  for (const s of mod.sections) {
    const isActive = state.activeSectionId === s.id;
    const card = el("div", { class: "section-card", id: "sect-" + s.id });
    card.appendChild(el("div", {
      class: "section-header" + (isActive ? " active" : ""),
      onclick: () => { state.activeSectionId = (state.activeSectionId === s.id ? null : s.id); renderSidebar(); renderMain(); }
    },
      el("span", null, s.title),
      el("span", { class: "sect-chev" }, isActive ? "▲" : "▼")
    ));
    const body = el("div", { class: "section-body" });
    body.innerHTML = renderContent(s.content);
    card.appendChild(body);
    root.appendChild(card);
  }
}

// ===== Search =====
function buildSearchIndex() {
  const idx = [];
  for (const m of MODULES) {
    for (const s of m.sections) {
      idx.push({ module: m, section: s, hay: (s.title + "\n" + s.content).toLowerCase() });
    }
  }
  return idx;
}
const SEARCH_INDEX = buildSearchIndex();

function renderSearchResults(root) {
  const q = state.searchQuery.toLowerCase();
  const matches = SEARCH_INDEX.filter(it => it.hay.includes(q));
  root.appendChild(el("div", { class: "results-head" }, matches.length + ' resultaten voor "' + state.searchQuery + '"'));
  if (matches.length === 0) {
    const empty = el("div", { class: "empty-state" });
    empty.innerHTML = '<div class="ico">🔎</div><div class="msg">Geen resultaten</div><div class="sub">Probeer een andere zoekterm of trefwoord.</div>';
    root.appendChild(empty);
    return;
  }
  for (const it of matches) {
    // Build preview around the first match position
    const lower = it.section.content.toLowerCase();
    let pos = lower.indexOf(q);
    if (pos < 0) pos = 0;
    let start = Math.max(0, pos - 40);
    const preview = (start > 0 ? "… " : "") + it.section.content.slice(start, start + 220);
    const card = el("div", { class: "result-card", onclick: () => {
      state.searchQuery = "";
      $("#searchInput").value = "";
      $("#searchClear").style.display = "none";
      selectSection(it.module.id, it.section.id);
    }});
    card.innerHTML =
      '<div class="result-meta">' +
        '<span class="result-emoji">' + escHtml(it.module.icon) + "</span>" +
        '<span class="result-tag">' + escHtml(it.module.title) + "</span>" +
      "</div>" +
      '<div class="result-title">' + highlight(it.section.title, state.searchQuery) + "</div>" +
      '<div class="result-preview">' + highlight(preview, state.searchQuery) + "</div>";
    root.appendChild(card);
  }
}

// ===== Chat =====
const CONV_KEY = "kwandoo-chatbot-logs";
const KB_KEY = "kwandoo-extra-knowledge";
const MAX_CONVS = 100;
let currentConvId = null;

function loadConversations() {
  try { return JSON.parse(localStorage.getItem(CONV_KEY) || "[]"); } catch { return []; }
}
function saveConversations(list) {
  while (list.length > MAX_CONVS) list.shift();
  localStorage.setItem(CONV_KEY, JSON.stringify(list));
}
function persistCurrentConversation() {
  if (!currentConvId || state.conversation.length === 0) return;
  const list = loadConversations();
  const idx = list.findIndex(c => c.id === currentConvId);
  const entry = {
    id: currentConvId,
    startTime: idx >= 0 ? list[idx].startTime : new Date().toISOString(),
    messages: state.conversation.map(m => ({ role: m.role, content: m.content, timestamp: m.timestamp }))
  };
  if (idx >= 0) list[idx] = entry; else list.push(entry);
  saveConversations(list);
}

function getExtraKnowledge() { return localStorage.getItem(KB_KEY) || ""; }
function setExtraKnowledge(v) { localStorage.setItem(KB_KEY, v); }

function buildKnowledgeBase(extra) {
  const parts = [];
  for (const m of MODULES) {
    parts.push("\n\n=== " + m.title + " ===\n");
    for (const s of m.sections) {
      parts.push("\n--- " + s.title + " ---\n" + s.content + "\n");
    }
  }
  if (SUPPLEMENTARY) parts.push("\n\n[BIJKOMENDE BRONNEN]\n" + SUPPLEMENTARY);
  if (extra && extra.trim()) parts.push("\n\n[EXTRA INFO TOEGEVOEGD DOOR MEDEWERKER]\n" + extra.trim());
  return parts.join("");
}

function renderMessages() {
  const box = $("#messages");
  box.innerHTML = "";
  if (state.conversation.length === 0) {
    const intro = el("div", { class: "msg-row assistant" },
      el("div", { class: "msg-avatar" }, "🤖"),
      el("div", { class: "bubble" }, "Hallo! Ik ben de Kwandoo Assistent. Stel gerust een vraag over activiteiten, inschrijvingen, opvang, facturatie of rapportering — ik help je graag verder.")
    );
    box.appendChild(intro);
  }
  for (const m of state.conversation) {
    box.appendChild(el("div", { class: "msg-row " + m.role },
      m.role === "user"
        ? el("div", { class: "bubble" }, m.content)
        : el("div", { class: "msg-avatar" }, "🤖"),
      m.role === "user"
        ? el("div", { class: "msg-avatar" }, "👤")
        : el("div", { class: "bubble" }, m.content)
    ));
  }
  if (state.loading) {
    box.appendChild(el("div", { class: "msg-row assistant" },
      el("div", { class: "msg-avatar" }, "🤖"),
      el("div", { class: "bubble", html: '<div class="typing"><span></span><span></span><span></span></div>' })
    ));
  }
  box.scrollTop = box.scrollHeight;
}

async function sendChat() {
  const input = $("#chatInput");
  const text = input.value.trim();
  if (!text || state.loading) return;
  if (!currentConvId) currentConvId = "conv-" + Date.now() + "-" + Math.random().toString(36).slice(2, 8);
  state.conversation.push({ role: "user", content: text, timestamp: new Date().toISOString() });
  input.value = "";
  updateSendBtn();
  state.loading = true;
  renderMessages();
  persistCurrentConversation();

  const kb = buildKnowledgeBase(getExtraKnowledge());
  const systemPrompt = SYSTEM_PROMPT_TEMPLATE.replace("{KNOWLEDGE}", kb);
  const payload = {
    model: "claude-sonnet-4-20250514",
    max_tokens: 1000,
    system: systemPrompt,
    messages: state.conversation.map(m => ({ role: m.role, content: m.content }))
  };

  let assistantText = "";
  try {
    const resp = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-access": "true"
      },
      body: JSON.stringify(payload)
    });
    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error("API " + resp.status + ": " + errText.slice(0, 200));
    }
    const data = await resp.json();
    if (data && data.content && data.content.length > 0) {
      assistantText = data.content.map(c => c.text || "").join("\n").trim();
    } else {
      assistantText = "Sorry, ik heb geen antwoord ontvangen. Probeer het opnieuw.";
    }
  } catch (err) {
    console.error(err);
    assistantText = "Er ging iets mis bij het ophalen van een antwoord. Controleer je internetverbinding en probeer opnieuw.\n\n(" + (err.message || err) + ")";
  }
  state.conversation.push({ role: "assistant", content: assistantText, timestamp: new Date().toISOString() });
  state.loading = false;
  renderMessages();
  persistCurrentConversation();
}

function updateSendBtn() {
  const btn = $("#sendBtn");
  const has = $("#chatInput").value.trim().length > 0;
  if (has) btn.classList.add("active"); else btn.classList.remove("active");
  btn.disabled = state.loading;
}

function exportLogsCsv() {
  const convs = loadConversations();
  // Include the current conversation even if it hasn't been persisted yet
  if (state.conversation.length > 0 && !convs.some(c => c.id === currentConvId)) {
    convs.push({ id: currentConvId, startTime: new Date().toISOString(), messages: state.conversation });
  }
  const rows = [["Tijdstip", "Rol", "Bericht"]];
  for (const c of convs) {
    for (const m of c.messages) {
      rows.push([m.timestamp || c.startTime || "", m.role === "user" ? "Medewerker" : "Assistent", m.content || ""]);
    }
  }
  const escape = (v) => '"' + String(v).replace(/"/g, '""') + '"';
  const csv = "﻿" + rows.map(r => r.map(escape).join(",")).join("\r\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const today = new Date().toISOString().slice(0, 10);
  a.href = url; a.download = "kwandoo-chatlog-" + today + ".csv";
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ===== Modal (extra kennis) =====
function openModal() {
  $("#extraKbInput").value = getExtraKnowledge();
  updateKbCount();
  $("#modalBackdrop").classList.add("open");
}
function closeModal() { $("#modalBackdrop").classList.remove("open"); }
function updateKbCount() {
  const v = $("#extraKbInput").value.trim();
  const count = v ? v.split(/\n\s*\n+/).filter(s => s.trim().length > 0).length : 0;
  $("#kbCount").textContent = count > 0 ? (count + " actieve kennisblok" + (count === 1 ? "" : "ken")) : "";
}

// ===== Event wiring =====
function init() {
  renderSidebar();
  renderMain();
  renderMessages();
  updateSendBtn();

  $("#hamburger").addEventListener("click", () => {
    state.sidebarCollapsed = !state.sidebarCollapsed;
    $("#sidebar").classList.toggle("collapsed", state.sidebarCollapsed);
  });

  const searchInput = $("#searchInput");
  const searchClear = $("#searchClear");
  searchInput.addEventListener("input", () => {
    state.searchQuery = searchInput.value.trim();
    searchClear.style.display = state.searchQuery ? "" : "none";
    renderMain();
  });
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      searchInput.value = ""; state.searchQuery = "";
      searchClear.style.display = "none"; renderMain();
    }
  });
  searchClear.addEventListener("click", () => {
    searchInput.value = ""; state.searchQuery = "";
    searchClear.style.display = "none"; renderMain(); searchInput.focus();
  });

  $("#fab").addEventListener("click", () => {
    $("#chatPanel").classList.add("open");
    $("#fab").classList.add("hidden");
    setTimeout(() => $("#chatInput").focus(), 50);
  });
  $("#closeChatBtn").addEventListener("click", () => {
    $("#chatPanel").classList.remove("open");
    $("#fab").classList.remove("hidden");
  });
  $("#exportLogsBtn").addEventListener("click", exportLogsCsv);

  const chatInput = $("#chatInput");
  chatInput.addEventListener("input", () => {
    chatInput.style.height = "auto";
    chatInput.style.height = Math.min(110, chatInput.scrollHeight) + "px";
    updateSendBtn();
  });
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendChat();
    }
  });
  $("#sendBtn").addEventListener("click", sendChat);

  $("#openModalBtn").addEventListener("click", openModal);
  $("#closeModalBtn").addEventListener("click", closeModal);
  $("#modalBackdrop").addEventListener("click", (e) => { if (e.target === $("#modalBackdrop")) closeModal(); });
  $("#saveKbBtn").addEventListener("click", () => {
    setExtraKnowledge($("#extraKbInput").value);
    closeModal();
  });
  $("#clearKbBtn").addEventListener("click", () => {
    if (confirm("Alle extra kennis wissen?")) {
      setExtraKnowledge(""); $("#extraKbInput").value = ""; updateKbCount();
    }
  });
  $("#extraKbInput").addEventListener("input", updateKbCount);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && $("#modalBackdrop").classList.contains("open")) closeModal();
  });
}

document.addEventListener("DOMContentLoaded", init);
</script>
</body>
</html>
"""

# Substitute placeholders. Use replace (not format) to avoid {} issues in CSS/JS.
out = HTML.replace("__MODULES_JSON__", MODULES_JSON)
out = out.replace("__SUPPLEMENTARY_JSON__", SUPPLEMENTARY_JSON)
out = out.replace("__SYSTEM_PROMPT__", json.dumps(SYSTEM_PROMPT, ensure_ascii=False))

Path("Kwandoo_Kennisbank_v2.html").write_text(out, encoding="utf-8")
print(f"Wrote Kwandoo_Kennisbank_v2.html ({len(out):,} bytes)")
