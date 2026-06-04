# SKIllaME 🧠 v2.0

> Repository di **skill e istruzioni per agenti AI** — ottimizzato per Copilot, Perplexity, ChatGPT, Gemini CLI, Claude Code, Cursor, Codex, OpenHands.

**Autore**: Senior Tributarista & Solutions Architect — Transfer Pricing, Fiscalità Internazionale, Workflow HA  
**Studio**: Biscozzi Nobili & Partners | Boves (CN), Piemonte

---

## 📁 Struttura del Repository

```
SKIllaME/
├── AGENTS.md                                   ← Standard universale (TUTTI gli agenti)
├── CLAUDE.md                                   ← Claude Code + Perplexity
├── .cursorrules                                ← Cursor IDE
├── chatgpt-setup.md                            ← Guida setup ChatGPT
├── perplexity-setup.md                         ← Guida setup Perplexity
├── README.md                                   ← Questo file
└── .github/
    ├── copilot-instructions.md                 ← GitHub Copilot (auto)
    └── skills/
        ├── transfer-pricing/SKILL.md           ← Skill TP
        ├── fiscalita-internazionale/SKILL.md   ← Skill fiscalità intl
        ├── pillar-two/SKILL.md                 ← Skill Pillar Two / GloBE ✨ NEW
        └── architettura-workflow/SKILL.md      ← Skill workflow HA
```

---

## 🤖 Compatibilità Agenti

| Agente | File Letto | Setup | Auto? |
|--------|-----------|-------|-------|
| **GitHub Copilot** | `.github/copilot-instructions.md` + `.github/skills/` | `gh skill install` | ✅ Auto |
| **Claude Code** | `CLAUDE.md` + `AGENTS.md` + `.github/skills/` | Esegui dalla cartella repo | ✅ Auto |
| **Cursor** | `.cursorrules` + `.github/skills/` | File presente nel repo | ✅ Auto |
| **Gemini CLI** | `AGENTS.md` + `.github/skills/` | `gh skill install --agent gemini` | ✅ Auto |
| **OpenHands** | `AGENTS.md` | Imposta repo come contesto | ✅ Auto |
| **Perplexity** | `AGENTS.md` + `CLAUDE.md` | Vedi `perplexity-setup.md` | ⚙️ Config |
| **ChatGPT** | Tutti (manual) | Vedi `chatgpt-setup.md` | ⚙️ Config |
| **Codex CLI** | `AGENTS.md` | `gh skill install --agent codex` | ✅ Auto |

---

## 🚀 Quick Start

### GitHub Copilot CLI
```bash
gh skill install bonaventura7/SKIllaME transfer-pricing
gh skill install bonaventura7/SKIllaME fiscalita-internazionale
gh skill install bonaventura7/SKIllaME pillar-two
gh skill install bonaventura7/SKIllaME architettura-workflow
```

### Claude Code / OpenHands
```bash
gh skill install bonaventura7/SKIllaME --all --agent claude-code
```

### Gemini CLI
```bash
gh skill install bonaventura7/SKIllaME --all --agent gemini
```

### ChatGPT
→ Segui la guida in [`chatgpt-setup.md`](./chatgpt-setup.md)

### Perplexity
→ Segui la guida in [`perplexity-setup.md`](./perplexity-setup.md)

---

## 📚 Skill Disponibili

### 1. `transfer-pricing`
Analisi e documentazione Transfer Pricing: metodi OCSE (TNMM, CUP, RPM, CPM, PSM), FAR analysis, benchmark, Masterfile/Local File, compliance italiana.

### 2. `fiscalita-internazionale`
CFC (art. 167 TUIR), stabile organizzazione (art. 162 TUIR), MAP, APA (art. 31-ter DPR 600/73), trattati contro doppia imposizione, BEPS, holding UE.

### 3. `pillar-two` ✨
GloBE Rules: calcolo ETR per giurisdizione, IIR/UTPR/QDMTT/STTR, D.Lgs. 209/2023, safe harbour, impatto su strutture TP, GloBE Information Return.

### 4. `architettura-workflow`
Workflow HA: n8n, automazione, agenti AI, retry/circuit breaker/bulkhead/DLQ, Python FastAPI, monitoring OpenTelemetry, workaround pragmatici.

---

## 🔗 URL Raw per Integrazioni

```
AGENTS.md (universale):
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md

Transfer Pricing:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/transfer-pricing/SKILL.md

Pillar Two:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/pillar-two/SKILL.md

Fiscalità internazionale:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/fiscalita-internazionale/SKILL.md

Architettura workflow:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/architettura-workflow/SKILL.md
```

---

## 📋 Changelog

### v2.0 (Giugno 2026)
- ✨ Aggiunta skill `pillar-two` (GloBE, D.Lgs. 209/2023)
- ✨ Aggiunto `.cursorrules` per Cursor IDE
- ✨ Aggiunta guida `chatgpt-setup.md` (3 metodi)
- ✨ Aggiunta guida `perplexity-setup.md`
- 🔧 `AGENTS.md` v2.0: trigger keywords, tabella skill, emoji struttura
- 🔧 `CLAUDE.md` v2.0: yaml config, skill trigger map
- 🔧 `copilot-instructions.md` v2.0: tabella trigger, skill map
- 🔧 `README.md` completo con compatibilità agenti e URL raw

### v1.0 (Giugno 2026 — iniziale)
- Struttura base: AGENTS.md, CLAUDE.md, 3 skill, copilot-instructions
