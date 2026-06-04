---
name: transfer-pricing
description: >-
  Analizza, documenta e valida operazioni di Transfer Pricing per gruppi
  multinazionali. Usa questa skill quando si lavora con prezzi infragruppo,
  analisi di comparabilità, documentazione TP (Masterfile/Local File),
  OCSE Guidelines, Pillar Two, MAP, APA.
tags: [transfer-pricing, fiscalita, OCSE, multinazionali, documentazione-TP]
---

# Skill: Transfer Pricing

## Quando Usarla

Attiva questa skill quando la richiesta riguarda:
- Prezzi di trasferimento infragruppo (beni, servizi, IP, finanziamenti, garanzie)
- Documentazione TP: Masterfile e Local File (D.Lgs. 471/97 e Provv. 23/11/2020)
- Analisi funzionale e di rischio (FAR analysis)
- Selezione del metodo OCSE più appropriato
- Benchmark / analisi di comparabilità (database Bureau van Dijk, etc.)
- Procedura amichevole (MAP) e accordi preventivi (APA / ruling)
- Pillar Two e impatto sui gruppi italiani
- Contestazioni dell'Agenzia delle Entrate in materia TP

## Processo Operativo

### Step 1 — Classificazione della Transazione
```
Tipo: [ ] Beni materiali  [ ] Servizi  [ ] IP/Intangibles  
       [ ] Finanziamenti  [ ] Garanzie  [ ] Cost sharing
Flusso: [ ] Italia → Estero  [ ] Estero → Italia  [ ] Estero → Estero
Controparte: _____________  Paese: _____________  
Importo annuo: _____________  Valuta: _____________
```

### Step 2 — Analisi Funzionale (FAR)
- **Funzioni** svolte da ciascuna entità (produzione, distribuzione, R&D, marketing...)
- **Asset** utilizzati (tangibili, intangibili, finanziari)
- **Rischi** assunti (mercato, credito, inventario, valuta, R&D)

### Step 3 — Selezione Metodo OCSE

| Metodo | Acronimo | Quando preferirlo |
|--------|----------|-------------------|
| Confronto del Prezzo | CUP | Commodity, prestiti, royalty con comparables |
| Prezzo di Rivendita | RPM | Distribuzione pura, no valore aggiunto |
| Costo Maggiorato | CPM | Produzione a contratto, servizi |
| Margine Netto | TNMM | Più usato in pratica, robusto |
| Ripartizione Utili | PSM | Transazioni integrate, IP unici |

### Step 4 — Benchmark
- Database: Bureau van Dijk (Orbis/Amadeus), TP Catalyst, RoyaltyStat
- Criteri di ricerca: SIC/NACE code, size filter, geography, independency
- Range interquartile: 25° → 75° percentile (median come punto di riferimento)
- Aggiornamento: ogni 3 anni (dati pluriennali preferibili)

### Step 5 — Documentazione
```
Masterfile:
  - Struttura organizzativa e legale del gruppo
  - Descrizione attività e value chain
  - Intangibles e loro gestione
  - Politiche finanziarie infragruppo
  - Posizione fiscale consolidata

Local File (per ciascuna entità italiana):
  - Descrizione entità locale
  - Transazioni infragruppo (una sezione per tipo)
  - FAR analysis dettagliata
  - Metodo TP selezionato e applicato
  - Benchmark study
  - Informazioni finanziarie
```

### Step 6 — Verifica Compliance
- [ ] Soglie documentazione obbligatoria (art. 1 co. 6 D.Lgs. 471/97: ≥ €30M ricavi o transazioni ≥ €1M)
- [ ] Firma del legale rappresentante entro termine dichiarazione
- [ ] Comunicazione in dichiarazione dei redditi (quadro RS)
- [ ] Country-by-Country Report (CbCR) se ricavi consolidati ≥ €750M

## Normativa di Riferimento

- **Italia**: Art. 110 co. 7 TUIR; D.Lgs. 471/1997 art. 1 co. 6; Provvedimento AdE 23/11/2020
- **OCSE**: Transfer Pricing Guidelines for Multinational Enterprises (2022 edition)
- **UE**: Direttiva 2022/2523 (Pillar Two — GloBE rules)
- **MLI**: Multilateral Instrument (strumento multilaterale OCSE)

## Output Atteso

Se richiesto, genera:
1. Bozza struttura Masterfile/Local File
2. Template FAR analysis
3. Memo di posizionamento TP
4. Checklist compliance documentazione
5. Risk assessment contestazioni AdE
