---
name: xlsx-reverse-engineering
description: "Esegui reverse engineering, audit e analisi di file Excel esistenti (.xlsx, .xlsm) per estrarre struttura, formule, logica di business, dipendenze e architettura tecnica. Usa quando: (1) Un utente carica o riferisce un file Excel che vuole capire, decostruire o documentare; (2) I task richiedono analisi della complessità delle formule, rilevamento errori o audit dell'integrità del workbook; (3) Identificare logica di business, modelli finanziari o flussi di dati incorporati nei fogli; (4) Migrare o refactoring di soluzioni Excel esistenti; (5) Estrarre assunzioni, KPI o catene di calcolo dai workbook; (6) Generare documentazione tecnica da fogli non documentati. Completa la skill xlsx per task di creazione/modifica."
license: Apache-2.0
---

# Excel Reverse Engineering (Versione Italiana)

Analizza e decostruisci workbook Excel esistenti per estrarre la loro architettura strutturale, logica e di business.

Questa skill segue una pipeline strutturata in 4 fasi che produce sia artefatti JSON che un report Excel di documentazione professionale finale.

## Stack Tecnologico

- **Python 3** con `openpyxl` (introspezione principale del workbook)
- **Script inclusi**: `inspect_xlsx.py`, `formula_audit.py`, `extract_logic.py`, `generate_report.py`
- **Supporto low-level**: `unpack_xlsx.py` (per ispezione OOXML di fogli nascosti, protezioni, rilevamento macro)
- **Riutilizzo**: Pattern e recalc dalla skill `xlsx` dove utile

## Workflow Raccomandato (4 Fasi)

### Fase 1: ISPEZIONE STRUTTURALE
Esegui analisi strutturale per ottenere inventario fogli, conteggio formule, named ranges, tabelle, protezioni, rilevamento macro/connessioni.

```bash
python scripts/inspect_xlsx.py <file.xlsx> --pretty
```

### Fase 2: AUDIT DELLE FORMULE
Analisi profonda di ogni formula per complessità, dipendenze, uso di funzioni, funzioni volatili e problemi.

```bash
python scripts/formula_audit.py <file.xlsx> --pretty
```

### Fase 3: ESTRAZIONE DELLA LOGICA
Identifica pattern di business, tipo di modello, assunzioni e flussi di dati.

```bash
python scripts/extract_logic.py <file.xlsx> --pretty
```

### Fase 4: GENERAZIONE REPORT
Combina gli output delle fasi 1-3 in un workbook Excel di documentazione multi-foglio professionale.

```bash
python scripts/generate_report.py <file.xlsx> <report.xlsx> [inspect.json] [audit.json] [logic.json]
```

## Riferimento agli Script

### `inspect_xlsx.py` — Analisi Strutturale
Estrae metadati, inventario fogli (inclusi hidden/veryHidden), conteggio formule, named ranges, tabelle, stato protezioni, rilevamento macro/connessioni.

### `formula_audit.py` — Analisi Profonda Formule
Analizza complessità (scala 1-100), catene di dipendenze, uso funzioni, funzioni volatili (INDIRECT, OFFSET...), rischi Excel 365+.

### `extract_logic.py` — Estrazione Logica di Business
Rileva tipi di modello (three_statement_financial_model, budget_forecast, dcf_valuation...), pattern finanziari, assunzioni, flussi di dati cross-sheet, indicatori di rischio.

### `generate_report.py` — Generazione Documentazione
Produce un report Excel multi-foglio professionale con:
- Copertina / Executive Summary
- Sheet Inventory
- Formula Analysis
- Issues & Warnings (con colori per severità)
- Business Logic
- Dependencies
- Named Ranges
- Recommendations

## Integrazione con la skill xlsx

Questa skill è **solo per analisi e reverse engineering**.

- Per creare nuovi file o modificare → passa alla skill `xlsx`.
- Dopo l'analisi, puoi passare gli insight alla skill `xlsx` per refactoring o ricreazione del workbook.

## Pattern Comuni

- **Audit Modello Finanziario**
- **Documentazione Workbook Legacy**
- **Valutazione Migrazione** (rileva macro, connessioni esterne, score di complessità)

## File di Esempio per Test

In `examples/`:
- `sample_re_test.xlsx`
- `sample_financial_re.xlsx`
- `sample_pivot_macro_re.xlsx` (molti SUMIFS, simulazione macro, veryHidden, dipendenze complesse)

Esegui la pipeline completa su uno di essi per generare un report completo.

## Runner di Comodità

Per comodità usa l'orchestratore:

```bash
python scripts/run_full_analysis.py tuo_file.xlsx --output-dir ./analisi --data-only
```

Esegue tutte le fasi e genera il report finale.

## File già ricalcolati

Se hai già eseguito il ricalcolo (tramite xlsx skill):

```bash
python scripts/run_full_analysis.py file.xlsx --data-only
```

Carica i valori calcolati invece delle formule.
