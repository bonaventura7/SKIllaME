---
name: xlsx-reverse-engineering
version: 1.0
description: Reverse engineering avanzato di file Excel/XLSX — decostruzione formule, mapping dati, ricostruzione logica, audit struttura fogli complessi. Skill locale Luca Consalter — Desktop.
agents: [main_agent, general_purpose, xlsx_skill]
triggers: [xlsx, Excel reverse, formula audit, spreadsheet analisi, reverse engineering Excel, decostruisci foglio, analisi formule, mappatura dati Excel]
---

# XLSX Reverse Engineering

Skill avanzata per il **reverse engineering completo di file Excel/XLSX**. Analizza, decostruisce e documenta fogli di calcolo complessi, ricostruisce la logica delle formule, mappa le dipendenze tra celle e fogli, e produce documentazione strutturata della logica applicativa nascosta nel file.

## Missione

Data un file XLSX (allegato o descritto), produrre:
1. **Mappa strutturale** — tutti i fogli, named ranges, tabelle, pivot, connessioni dati
2. **Audit formule** — tutte le formule non-banali con spiegazione in linguaggio naturale
3. **Grafo dipendenze** — quali celle/fogli dipendono da quali
4. **Logica business** — ricostruzione dell'intento funzionale (cos'è questo file? cosa calcola?)
5. **Bug / anomalie** — formule hard-coded, riferimenti circolari, errori #N/A, #REF, #DIV/0
6. **Output deliverable** — documentazione Markdown + possibile migrazione a Python/pandas

## Quando Usarla

- Ricevi un file Excel da un cliente/collega senza documentazione
- Devi validare formule di calcolo TP (berry ratio, TNMM, PLI, NCP)
- Devi migrare un modello Excel in Python, Power BI o altra piattaforma
- Stai facendo audit di fogli Excel usati in contenziosi fiscali o documentazione TP
- Vuoi capire come è costruito un template complesso di benchmark

## Trigger Keywords

`xlsx`, `Excel reverse`, `formula audit`, `spreadsheet analisi`, `reverse engineering Excel`, `decostruisci foglio`, `analisi formule`, `mappatura dati Excel`, `audit Excel`, `capire foglio`, `logica Excel`, `formula spiegazione`, `dipendenze celle`

## Processo Standard

```
1. INTAKE → ricevi file XLSX (allegato) o descrizione del contenuto
2. STRUTTURA → elenca tutti i fogli, tabelle, named ranges, pivot
3. AUDIT FORMULE → analizza ogni formula significativa
4. DIPENDENZE → costruisci grafo logico (quale foglio usa quale)
5. LOGICA BUSINESS → spiega in italiano cosa calcola il file
6. BUG/ANOMALIE → segnala hard-coding, errori, riferimenti rotti
7. DELIVERABLE → Markdown documentazione + suggerimenti refactoring
```

## Formato Output

### Sezione 1 — Struttura File

```
📁 File: [nome_file.xlsx]
├── 📄 Foglio: [Nome] — [descrizione breve]
│   ├── Tabelle: [elenco]
│   ├── Named Ranges: [elenco]
│   └── Pivot: [elenco]
...
```

### Sezione 2 — Audit Formule

| Cella | Formula | Spiegazione | Dipendenze | Anomalie |
|-------|---------|-------------|------------|----------|
| B12 | `=VLOOKUP(A2,Dati!$A:$C,3,0)` | Cerca il codice in A2 nel foglio Dati, colonna C | Foglio Dati | Nessuna |

### Sezione 3 — Logica Business

Descrizione narrativa dell'intento del file.

### Sezione 4 — Anomalie e Rischi

Elenco bug, hard-coding, celle senza formula ma con valore fisso critico.

### Sezione 5 — Raccomandazioni

Suggerimenti per refactoring, migrazione Python, o documentazione aggiuntiva.

## Integrazione TP

Questa skill è ottimizzata per file Excel di Transfer Pricing:
- Fogli di calcolo PLI (Net Cost Plus, Berry Ratio, ROCE, Operating Margin)
- Template di benchmark Orbis/Amadeus con filtri
- Modelli di documentazione TP con calcoli di range
- File di analisi comparabili con formule percentili

## Workaround / Limitazioni

- Se il file è protetto da password → chiedi la password o lavora sulla descrizione
- Se il file è troppo grande → focus sulle sezioni critiche indicate dall'utente
- Se le formule sono in VBA → analizza il codice VBA separatamente
- File `.xlsm` con macro → documenta le macro come sezione aggiuntiva

---

*Skill locale — Luca Consalter Desktop | Versione 1.0 | Giugno 2026*
*Integrazione con: tp-spreadsheet-reverse (#23), Design Photocopy Clone (#28)*
