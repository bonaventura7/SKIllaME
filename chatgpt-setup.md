# Come Usare SKIllaME con ChatGPT

> Guida rapida per connettere le skill di questo repository a ChatGPT.

---

## Metodo 1 — Custom Instructions (immediato, 2 minuti)

Vai su: **ChatGPT → Profilo → Personalizza ChatGPT → Istruzioni personalizzate**

Nel campo **"Come dovrebbe risponderti ChatGPT?"** incolla esattamente questo:

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

---

## Metodo 2 — MyGPT (più potente, permanente)

1. Vai su [chatgpt.com/gpts](https://chatgpt.com/gpts)
2. Clicca **"Crea un GPT"**
3. Nella sezione **Instructions** incolla il blocco sopra
4. Nella sezione **Knowledge** carica questi file (scaricali dal repo):
   - `AGENTS.md`
   - `.github/skills/transfer-pricing/SKILL.md`
   - `.github/skills/fiscalita-internazionale/SKILL.md`
   - `.github/skills/pillar-two/SKILL.md`
   - `.github/skills/architettura-workflow/SKILL.md`
5. Nome suggerito: **"TP & Tax Architect"**
6. Visibilità: **Solo io** (privato)
7. Salva → usa direttamente dalla sidebar di ChatGPT

---

## Metodo 3 — Prompt di Sessione (workaround rapido)

All'inizio di ogni nuova chat incolla:

```
Leggi e applica queste istruzioni per tutta la sessione:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/AGENTS.md

Per domande su Transfer Pricing, applica anche:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/transfer-pricing/SKILL.md

Per Pillar Two / GloBE:
https://raw.githubusercontent.com/bonaventura7/SKIllaME/main/.github/skills/pillar-two/SKILL.md
```

---

## Confronto Metodi

| Metodo | Tempo setup | Persistenza | Skill caricabili | Consigliato per |
|--------|-------------|-------------|-----------------|------------------|
| Custom Instructions | 2 min | Permanente su tutti i chat | ✅ (testo) | Uso quotidiano |
| MyGPT | 10 min | Permanente, un GPT dedicato | ✅✅ (file upload) | Massima potenza |
| Prompt sessione | 30 sec | Solo quella sessione | ✅ (URL) | Test rapidi |
