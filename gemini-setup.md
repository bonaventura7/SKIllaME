# Come Usare SKIllaME con Google Gemini

> Guida per connettere le skill di questo repository a Google Gemini (AI Studio, Gems, API).

---

## Metodo 1 — Gem Personalizzato in Google AI Studio (consigliato, permanente)

Un **Gem** è un agente Gemini personalizzato con istruzioni e knowledge base fisse — equivalente ai MyGPT di ChatGPT.

### Passo 1: Apri Google AI Studio
Vai su [aistudio.google.com](https://aistudio.google.com) → sezione **Gems** → **Crea nuovo Gem**

### Passo 2: Configura le istruzioni del Gem

Nel campo **Instructions** incolla esattamente questo:

```
Sei il mio assistente personale per Transfer Pricing, fiscalità internazionale e architettura di workflow.

PROFILO UTENTE:
Sono un tributarista e solutions architect italiano, Studio Biscozzi Nobili & Partners.
Specializzazioni: Transfer Pricing (art. 110 TUIR, OCSE Guidelines 2022), fiscalità internazionale,
workflow ad alta resilienza (HA), Pillar Two / GloBE (D.Lgs. 209/2023).

METODO OBBLIGATORIO:
1. Fai sempre mente locale e brainstorming prima di rispondere
2. Proponi un piano strutturato con step numerati
3. Poi esegui con soluzione concreta e minimale
4. Includi sempre: workaround/fallback + rischi + prossimi passi

STILE:
- Rispondi sempre in italiano
- Tono: diretto, professionale, Senior level — niente fuffa
- Cita sempre la normativa (art. + fonte + anno)
- Disclaimer obbligatorio su posizioni fiscali

SKILL DISPONIBILI:
- Transfer Pricing: metodi OCSE (TNMM, CUP, RPM, CPM, PSM), FAR analysis, benchmark, documentazione TP
- Fiscalità internazionale: CFC (art. 167 TUIR), MAP, APA, trattati, WHT, BEPS, holding
- Pillar Two / GloBE: ETR, IIR, UTPR, QDMTT, STTR, D.Lgs. 209/2023, safe harbour
- Architettura workflow: n8n, automazione, HA, retry, circuit breaker, agenti AI

VINCOLI:
- Mai dati sensibili di clienti reali
- Mai posizioni fiscali definitive senza disclaimer
- Soluzioni sempre reversibili con rollback plan
```

### Passo 3: Carica i file Knowledge

Nel campo **Knowledge** carica (scarica dal repo o usa gli URL raw):

- [`AGENTS.md`](https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md)
- [`.github/skills/transfer-pricing/SKILL.md`](https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/transfer-pricing/SKILL.md)
- [`.github/skills/fiscalita-internazionale/SKILL.md`](https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/fiscalita-internazionale/SKILL.md)
- [`.github/skills/pillar-two/SKILL.md`](https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/pillar-two/SKILL.md)
- [`.github/skills/architettura-workflow/SKILL.md`](https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/architettura-workflow/SKILL.md)

### Passo 4: Finalizza
- **Nome suggerito:** `TP & Tax Architect`
- **Modello consigliato:** `Gemini 2.5 Pro` (massima profondità ragionamento)
- Salva → disponibile da [gemini.google.com](https://gemini.google.com) nella sidebar **Gems**

---

## Metodo 2 — Gemini App (gemini.google.com) con Prompt di Sessione

All'inizio di ogni nuova chat Gemini incolla:

```
Prima di rispondere, leggi e applica queste istruzioni per tutta la sessione:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md

Per domande su Transfer Pricing, applica anche:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/transfer-pricing/SKILL.md

Per Pillar Two / GloBE:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/pillar-two/SKILL.md
```

> ⚠️ Gemini legge i file raw da URL pubblici direttamente nel contesto. Assicurati che il repo sia pubblico o usa i file scaricati.

---

## Metodo 3 — API Gemini + GitHub Actions (automazione avanzata)

Per integrare Gemini nei workflow del repo:

### Passo 1: Ottieni la API Key
- Vai su [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → **Crea API Key**

### Passo 2: Aggiungi il Secret al repo GitHub
- Nel repo: `Settings → Secrets and variables → Actions → New repository secret`
- Nome: `GEMINI_API_KEY`

### Passo 3: Crea il workflow `.github/workflows/gemini-review.yml`

```yaml
name: Gemini AI Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  gemini-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Gemini Code Review
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          curl -s \
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=$GEMINI_API_KEY" \
            -H 'Content-Type: application/json' \
            -d '{
              "contents":[{
                "parts":[{
                  "text":"Sei un senior tax architect. Analizza le modifiche di questo PR e fornisci feedback in italiano."
                }]
              }]
            }'
```

---

## URL Raw Utili (copia-incolla rapido)

| File | URL Raw |
|------|---------|
| Istruzioni globali | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md` |
| Config Claude/Gemini | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/CLAUDE.md` |
| Transfer Pricing | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/transfer-pricing/SKILL.md` |
| Fiscalità intl | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/fiscalita-internazionale/SKILL.md` |
| Pillar Two | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/pillar-two/SKILL.md` |
| Architettura | `raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/architettura-workflow/SKILL.md` |

---

## Confronto Metodi

| Metodo | Tempo setup | Persistenza | Skill caricabili | Consigliato per |
|--------|-------------|-------------|-----------------|-----------------|
| Gem (AI Studio) | 10 min | Permanente, Gem dedicato | ✅✅ (file upload) | Massima potenza |
| Prompt sessione | 30 sec | Solo quella sessione | ✅ (URL) | Test rapidi |
| API + GitHub Actions | 20 min | Automatico su ogni PR | ✅✅ (workflow) | Automazione CI/CD |
