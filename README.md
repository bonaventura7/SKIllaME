# SKIllaME 🧠 v3.2

> Repository di **skill e istruzioni per agenti AI** — ottimizzato per:
> **Copilot · Perplexity · ChatGPT · Gemini CLI · Claude Code · Cursor · Codex · OpenHands**

**Autore**: Senior Tributarista & Solutions Architect | Transfer Pricing · Fiscalità Internazionale · Workflow HA
**Studio**: Biscozzi Nobili & Partners | Boves (CN), Piemonte

> 🔍 **Audit Giugno 2026**: il repo contiene ~110 contenuti. SKILL-INDEX copre ora 31 skill attive + 40+ community. Vedi [`SKILL-INDEX.md`](./SKILL-INDEX.md).

---

## 🗺️ Navigazione Rapida

| Vuoi... | Vai a... |
|---------|----------|
| Vedere tutte le skill con URL pronti | [`SKILL-INDEX.md`](./SKILL-INDEX.md) |
| File compatto per ChatGPT/Perplexity | [`ALL-SKILLS-COMPACT.md`](./ALL-SKILLS-COMPACT.md) |
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
├── SKILL-INDEX.md                     ← Master index + URL raw ✨
├── ALL-SKILLS-COMPACT.md             ← File unico per ChatGPT/Perplexity ✨ NUOVO
├── .cursorrules                       ← Cursor IDE
├── chatgpt-setup.md                   ← Guida ChatGPT (3 metodi)
├── perplexity-setup.md                ← Guida Perplexity
├── README.md                          ← Questo file
├── .github/
│   ├── copilot-instructions.md
│   ├── workflows/validate-skills.yml     ← CI/CD validation ✨ NUOVO
│   └── skills/                           ← Wrapper auto-discovered
└── Skill Claude/                      ← Archivio originale (~110 contenuti)
    ├── Agenti 00tot/                  (7 agenti AI)
    ├── Lavoro/TP/                     (12 skill TP + casi reali)
    ├── Lavoro/                        (bilancio, longform-book, spreadsheet)
    ├── claude-skills-llm-council/     ✨ CENSITA
    ├── design-photocopy-clone/        ✨ CENSITA
    ├── pptx/                          ✨ CENSITA
    ├── Personali/photo-perfect-slim/  ✨ CENSITA
    ├── CopyONEwriter.md               ✨ CENSITA
    └── Scaricate/                     (~40 community skills)
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
| **Perplexity** | `AGENTS.md` + `CLAUDE.md` + `ALL-SKILLS-COMPACT.md` | Vedi `perplexity-setup.md` | ⚙️ Config |
| **ChatGPT** | `ALL-SKILLS-COMPACT.md` (upload) | Vedi `chatgpt-setup.md` | ⚙️ Config |

---

## 🚀 Quick Start

### 1 comando per tutti gli agenti CLI
```bash
gh skill install bonaventura7/SKIllaME --all
```

### Per ChatGPT — upload file unico
1. Scarica [`ALL-SKILLS-COMPACT.md`](./ALL-SKILLS-COMPACT.md)
2. Caricalo come Knowledge nel tuo MyGPT
3. Oppure incolla il contenuto come Custom Instructions

### Per Perplexity Space — 6 URL essenziali
```
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/ALL-SKILLS-COMPACT.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/Skill%20Claude/Lavoro/TP/tp-toolbox-v2.4.0.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/pillar-two/SKILL.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/fiscalita-internazionale/SKILL.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/Skill%20Claude/Lavoro/TP/skill_TP_screening_comparabili_ADAPTIVE_GENERIC_v3_1.md
```

---

## 📋 Changelog

### v3.2 (Giugno 2026) ✨ Audit Completo
- **BUG FIX**: rimosso entry #28 duplicata (Swiss Steel)
- **BUG FIX**: rimossi 3 stub vuoti dall’index attivo (general-tp, pillar2-compliance, tp-valbruna-stub)
- **NUOVO**: 7 skill censite nell’audit (LLM Council, Design Clone, PPTX, Photo Perfect, CopyONE, Bilancio, Longform)
- **NUOVO**: sezione Community Skills (~40 skill da terzi)
- **NUOVO**: `ALL-SKILLS-COMPACT.md` — file unico per ChatGPT/Perplexity
- **NUOVO**: GitHub Action CI/CD `.github/workflows/validate-skills.yml`
- **FIX**: versione ora coerente v3.2 ovunque
- **FIX**: colonna Stato (Produzione/Draft/Stub) aggiunta a tutte le tabelle

### v3.1 (Giugno 2026)
- 28 skill indicizzate, multi-piattaforma

### v3.0 (Giugno 2026)
- 12 wrapper SKILL.md, SKILL-INDEX master, AGENTS.md, README
