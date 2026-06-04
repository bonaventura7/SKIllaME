# SKIllaME 🧠

> Repository di skill e istruzioni per agenti AI — leggibile da Copilot, Perplexity, Gemini CLI, Claude Code, Cursor, Codex.

## Cosa Contiene

| File | Letto da | Scopo |
|------|----------|-------|
| `AGENTS.md` | Tutti gli agenti (standard universale) | Istruzioni globali |
| `CLAUDE.md` | Claude Code, Perplexity Space | Regole specifiche Claude |
| `.github/copilot-instructions.md` | GitHub Copilot | Custom instructions Copilot |
| `.github/skills/transfer-pricing/` | Copilot, Gemini, Claude | Skill TP modulare |
| `.github/skills/fiscalita-internazionale/` | Copilot, Gemini, Claude | Skill fiscalità intl |
| `.github/skills/architettura-workflow/` | Copilot, Gemini, Claude | Skill workflow HA |

## Installazione Rapida

```bash
# Copilot CLI
gh skill install bonaventura7/SKIllaME transfer-pricing
gh skill install bonaventura7/SKIllaME fiscalita-internazionale
gh skill install bonaventura7/SKIllaME architettura-workflow

# Claude Code (dal tuo progetto)
gh skill install bonaventura7/SKIllaME transfer-pricing --agent claude-code

# Gemini CLI
gh skill install bonaventura7/SKIllaME transfer-pricing --agent gemini
```

## Configurare Perplexity Space

1. Vai nelle impostazioni dello Space
2. Aggiungi come fonte:
   - `https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md`
   - `https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/CLAUDE.md`
3. Gli agenti leggeranno automaticamente le istruzioni

## Struttura

```
SKIllaME/
├── AGENTS.md                              ← Standard universale
├── CLAUDE.md                              ← Claude / Perplexity
├── README.md                              ← Questo file
└── .github/
    ├── copilot-instructions.md            ← GitHub Copilot
    └── skills/
        ├── transfer-pricing/SKILL.md
        ├── fiscalita-internazionale/SKILL.md
        └── architettura-workflow/SKILL.md
```

## Autore

Senior Solutions Architect & Tributarista — Transfer Pricing & Fiscalità Internazionale  
Studio Biscozzi Nobili & Partners | Boves (CN), Piemonte
