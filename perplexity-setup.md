# Come Usare SKIllaME con Perplexity

> Guida per connettere le skill di questo repository a Perplexity AI (Space).

---

## Metodo 1 — Space Sources (consigliato)

### Passo 1: Apri le impostazioni dello Space
Vai nello Space → icona impostazioni → **Sources**

### Passo 2: Aggiungi questi URL come fonti

```
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/CLAUDE.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/transfer-pricing/SKILL.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/fiscalita-internazionale/SKILL.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/pillar-two/SKILL.md
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/architettura-workflow/SKILL.md
```

### Passo 3: Configura le istruzioni dello Space
Nelle impostazioni Space → **Instructions**, incolla:

```
Sei il mio assistente per Transfer Pricing, fiscalità internazionale e architettura workflow.
Leggi e applica sempre le istruzioni da AGENTS.md e CLAUDE.md nelle fonti.
Rispondi in italiano. Prima mente locale, poi piano, poi soluzione.
Cita sempre la normativa applicabile (TUIR, OCSE, Direttive UE).
Skill disponibili: transfer-pricing, fiscalita-internazionale, pillar-two, architettura-workflow.
```

---

## Metodo 2 — Prompt Diretto

All'inizio di ogni chat Perplexity:

```
Prima di rispondere leggi:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md
Applica quelle istruzioni per tutta la sessione.
```

---

## URL Raw Utili (copia-incolla rapido)

| File | URL Raw |
|------|---------|
| Istruzioni globali | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md` |
| Claude/Perplexity | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/CLAUDE.md` |
| Transfer Pricing | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/transfer-pricing/SKILL.md` |
| Fiscalità intl | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/fiscalita-internazionale/SKILL.md` |
| Pillar Two | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/pillar-two/SKILL.md` |
| Architettura | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/architettura-workflow/SKILL.md` |
