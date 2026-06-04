---
name: pillar-two
description: >-
  Analisi e compliance Pillar Two / GloBE (Global Anti-Base Erosion Rules).
  Usa quando si lavora con imposta minima globale 15%, IIR, UTPR, QDMTT,
  STTR, calcolo ETR per giurisdizione, D.Lgs. 209/2023 (recepimento italiano).
tags: [pillar-two, GloBE, imposta-minima, IIR, UTPR, QDMTT, STTR, BEPS, multinazionali]
---

# Skill: Pillar Two / GloBE Rules

## Quando Usarla

Attiva questa skill per:
- Calcolo ETR (Effective Tax Rate) per giurisdizione
- Verifica applicabilità: gruppi con ricavi consolidati ≥ €750M
- IIR (Income Inclusion Rule) — regola principale
- UTPR (Undertaxed Profits Rule) — regola secondaria / backstop
- QDMTT (Qualified Domestic Minimum Top-up Tax) — imposta integrativa italiana
- STTR (Subject to Tax Rule) — trattati bilaterali
- Impatto su strutture TP e holding esistenti
- Compliance reporting: GloBE Information Return (GIR)

---

## Framework Decisionale Pillar Two

### Step 1 — Verifica Soglia
```
Ricavi consolidati gruppo ≥ €750M in almeno 2 degli ultimi 4 anni fiscali?
  SÌ → Continua
  NO → Pillar Two non applicabile (verifica eccezioni de minimis)
```

### Step 2 — Calcolo ETR per Giurisdizione
```
ETR = Adjusted Covered Taxes / GloBE Income

ETR < 15%?
  SÌ → Top-up Tax dovuta = (15% - ETR) × GloBE Income
  NO → Nessuna imposta integrativa
```

### Step 3 — Meccanismi di Riscossione (gerarchia)

| Priorità | Meccanismo | Chi applica | Note |
|----------|------------|-------------|------|
| 1° | **QDMTT** | Stato della controllata | Imposta integrativa locale — accreditata vs IIR |
| 2° | **IIR** | Stato della capogruppo (o controllante intermedia) | Regola principale |
| 3° | **UTPR** | Tutti gli altri Stati del gruppo | Backstop se IIR non applicata |

### Step 4 — Eccezioni e Safe Harbour

```
Transitional CbCR Safe Harbour (fino a 2026):
  - ETR semplificata da CbCR ≥ 15% → OK (no calcolo GloBE completo)
  - Routine Profits Test: profitto ≤ sostanza economica → OK
  - De minimis: ricavi giurisdizione < €10M e profitto < €1M → OK

Permanent Safe Harbour:
  - Substance-based income exclusion (SBIE):
    5% payroll + 5% tangible assets (a regime)
    → Riduce GloBE Income soggetto a top-up tax
```

### Step 5 — Impatto su Transfer Pricing
```
Verifica coerenza TP ↔ Pillar Two:
- Margini TP che abbassano ETR sotto 15% → rischio top-up
- Strutture IP in giurisdizioni low-tax → rivalutare
- Cost sharing agreements → impatto su SBIE payroll
- Intercompany financing → Adjusted Covered Taxes
```

---

## Normativa di Riferimento

### Italia
- **D.Lgs. 209/2023** — recepimento Pillar Two (GloBE Rules) in Italia
- **Circ. AdE** — circolari applicative (aggiornamento continuo 2024-2026)
- **Art. 1 co. 98-110 L. 213/2023** (Legge di Bilancio 2024) — QDMTT italiana

### OCSE / Internazionale
- **OECD Pillar Two Model Rules** (Dicembre 2021)
- **OECD Commentary on Pillar Two** (Marzo 2022)
- **Administrative Guidance** (Febbraio 2023, Luglio 2023, Dicembre 2023, Giugno 2024)
- **GloBE Information Return (GIR)** — standard reporting

### UE
- **Direttiva 2022/2523/UE** (22 Dicembre 2022) — recepita da tutti gli Stati UE

---

## Checklist Compliance Annuale

```
□ Verifica soglia €750M (media 2 anni su 4)
□ Mappa entità del gruppo per giurisdizione
□ Calcola ETR GloBE per ogni giurisdizione
□ Identifica giurisdizioni sotto soglia 15%
□ Applica SBIE (substance-based income exclusion)
□ Verifica QDMTT in ogni Stato UE del gruppo
□ Verifica Transitional Safe Harbour (se ancora applicabile)
□ Prepara GloBE Information Return (GIR)
□ Allinea politica TP con ETR post-Pillar Two
□ Aggiorna documentazione TP (Masterfile) con sezione GloBE
□ Verifica trattati bilaterali con clausola STTR
```

---

## Output Atteso

1. Analisi applicabilità Pillar Two per il gruppo
2. Calcolo ETR semplificato per giurisdizione
3. Identificazione top-up tax dovuta
4. Impatto su struttura TP esistente
5. Roadmap compliance con timeline
6. Memo per il CdA / CFO
