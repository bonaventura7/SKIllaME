# SKIllaME 🧠 v3.0

> Repository di **skill e istruzioni per agenti AI** — ottimizzato per:
> **Copilot · Perplexity · ChatGPT · Gemini CLI · Claude Code · Cursor · Codex · OpenHands**

**Autore**: Senior Tributarista & Solutions Architect | Transfer Pricing · Fiscalità Internazionale · Workflow HA
**Studio**: Biscozzi Nobili & Partners | Boves (CN), Piemonte

---

## 🗺️ Navigazione Rapida

| Vuoi... | Vai a... |
|---------|----------|
| Vedere tutte le skill con URL pronti | [`SKILL-INDEX.md`](./SKILL-INDEX.md) |
| Configurare ChatGPT | [`chatgpt-setup.md`](./chatgpt-setup.md) |
| Configurare Perplexity | [`perplexity-setup.md`](./perplexity-setup.md) |
| Istruzioni per tutti gli agenti | [`AGENTS.md`](./AGENTS.md) |
| Istruzioni Claude/Perplexity | [`CLAUDE.md`](./CLAUDE.md) |

---

## 📁 Struttura Completa

```
SKIllaME/
├── AGENTS.md                          ← Universale (TUTTI gli agenti)
├── CLAUDE.md                          ← Claude Code + Perplexity
├── SKILL-INDEX.md                     ← Master index + URL raw pronti ✨
├── .cursorrules                       ← Cursor IDE
├── chatgpt-setup.md                   ← Guida ChatGPT (3 metodi)
├── perplexity-setup.md                ← Guida Perplexity
├── README.md                          ← Questo file
├── .github/
│   ├── copilot-instructions.md        ← GitHub Copilot (auto)
│   └── skills/                        ← Skill standard (auto-discovered)
│       ├── transfer-pricing/
│       ├── fiscalita-internazionale/
│       ├── pillar-two/                 ✨
│       ├── architettura-workflow/
│       ├── tp-screening-comparabili/  ✨
│       ├── tp-report-benchmark/       ✨
│       ├── tp-intercompany-segregation/ ✨
│       ├── tp-toolbox/                ✨
│       ├── tp-valuation-advisor/      ✨
│       ├── tp-manual-review/          ✨
│       ├── tp-populate-fin/           ✨
│       ├── tp-architect-omni/         ✨
│       ├── tp-spreadsheet-reverse/    ✨
│       ├── agente-tp-benchmark/       ✨
│       ├── agente-conta-ore/          ✨
│       └── agente-file-mapper/        ✨
└── Skill Claude/                      ← Archivio originale (sorgenti)
    ├── Agenti 00tot/
    ├── Lavoro/TP/
    ├── Personali/
    └── Scaricate/
```

---

## 🤖 Compatibilità Agenti

| Agente | File Letto | Setup | Auto? |
|--------|-----------|-------|-------|
| **GitHub Copilot** | `.github/copilot-instructions.md` + `.github/skills/` | `gh skill install bonaventura7/SKIllaME --all` | ✅ Auto |
| **Gemini CLI** | `AGENTS.md` + `.github/skills/` | `gh skill install --all --agent gemini` | ✅ Auto |
| **Claude Code** | `CLAUDE.md` + `AGENTS.md` + `.github/skills/` | `gh skill install --all --agent claude-code` | ✅ Auto |
| **Cursor** | `.cursorrules` + `.github/skills/` | File presente nel repo | ✅ Auto |
| **OpenHands** | `AGENTS.md` | Imposta repo come contesto | ✅ Auto |
| **Codex CLI** | `AGENTS.md` | `gh skill install --agent codex` | ✅ Auto |
| **Perplexity** | `AGENTS.md` + `CLAUDE.md` + skill scelte | Vedi `perplexity-setup.md` | ⚙️ Config |
| **ChatGPT** | Tutti (manuale) | Vedi `chatgpt-setup.md` | ⚙️ Config |

---

## 🚀 Quick Start

### 1 comando per tutti gli agenti CLI
```bash
gh skill install bonaventura7/SKIllaME --all
```

### Per ChatGPT/Perplexity
→ Apri [`SKILL-INDEX.md`](./SKILL-INDEX.md) e copia gli URL raw delle skill che ti servono.

---

## 📋 Changelog

### v3.0 (Giugno 2026) ✨
- 12 nuovi wrapper SKILL.md per tutte le skill caricate
- `SKILL-INDEX.md` master index con URL raw pronti per copia-incolla
- `AGENTS.md` aggiornato con tabella completa 17 skill + trigger keywords
- `README.md` con navigazione rapida e struttura completa

### v2.0 (Giugno 2026)
- Skill pillar-two, .cursorrules, guide ChatGPT e Perplexity

### v1.0 (Giugno 2026)
- Struttura base: AGENTS.md, CLAUDE.md, 3 skill core
