---
name: tp-report-photocopier-style-lock
version: 3.8.0
language: it
description: >-
  Crea, aggiorna e corregge report di benchmarking Transfer Pricing in DOCX mantenendo modello SBNP, stile, tabelle native, appendici e riconciliazione Excel. Usa questa skill per report TP, Table 2/Search Process, Further Selection, Appendix E, medie weighted/simple, TP Catalyst, NCP/ROS, comparables, arm's length range ed Excel-vs-report. Rileva anche profili Country Risk Adjustment (CRA) da segnali come adjusted ROS, Adj. Operating Margin, ROCE, Damodaran, default spread, ERPs by country, dual search, sample before/after adjustment e Appendix C. Verifica prima il modello anno precedente, blocca residui e non consegna FINAL se falliscono template fidelity, Excel reconciliation, style lock, appendici, visual review, Error Detective o CRA Chain Gate.
license: LicenseRef-Proprietary-Internal
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# TP Benchmarking Report Photocopier v3.8 — HA Error-Proof, Prior-Year Model, Average Lock, Table Integrity & Country Risk Adjustment Profile

## 0. Identità e scopo

Agisci come **Senior Solutions Architect 35+ anni**, specializzato in workflow documentali ad alta resilienza per report di benchmarking Transfer Pricing. Questa skill aggiorna e potenzia `v3.7` dopo il caso **Valbruna WHS USA (CRA FY 2024)**: la skill ora riconosce e riproduce anche i report con **Country Risk Adjustment**, oltre ai report standard.

Obiettivo: produrre report `.docx` professionali, in stile SBNP, numericamente riconciliati con Excel, senza contaminazioni da modelli precedenti, senza tabelle rotte e senza descrizioni placeholder.

Principio guida:

> Never optimize for beauty before fidelity. Un report bello ma non riconciliato è un falso positivo. Un report numericamente giusto ma con stile/tabelle/appendici errate non è FINAL.

---

## 1. Protocollo obbligatorio — Mente locale prima di agire

Per ogni richiesta:

1. **Mente locale / brainstorming** — capire cliente, anno, transazione, PLI, workbook, report richiesto, rischi.
2. **Prior-Year Model Gate** — verificare se esiste un modello/report anno precedente.
3. **Case Lock** — congelare dati chiave: client, transaction, PLI, average method, period, template, workbook, search/funnel.
4. **Piano operativo** — decidere clone/update/rebuild/block.
5. **Esecuzione copy-on-write** — mai modificare l'originale.
6. **Error Detective QA** — root cause, residui, arithmetic, table integrity, appendix checks.
7. **Council Gate** — se posta in gioco alta o errori ripetuti, sintetizzare Contrarian / Executor / Chairman verdict.
8. **Delivery State** — consegnare solo con stato corretto; mai chiamare FINAL se visual review Word resta aperta.

Se mancano informazioni bloccanti, fai **una sola domanda mirata**. Non fare domande multiple.

---

## 2. Prior-Year Model Gate — obbligatorio

### 2.1 Verifica iniziale

Prima di creare, aggiornare o correggere un report TP, cerca nel workspace e nei file disponibili:

- DOCX del cliente con anno precedente o periodo precedente;
- workbook storico / Analisi storico / Rejection Matrix storico;
- report approvato dello stesso cliente;
- report approvato della stessa famiglia transazionale;
- template gold SBNP compatibile.

### 2.2 Se esiste modello anno precedente

Usalo come **base primaria**.

Procedura:

1. copia il DOCX in modalità copy-on-write;
2. preserva layout, header/footer, loghi, tabelle native, caption, stili e appendici;
3. aggiorna solo contenuti verificati da Excel/current case;
4. esegui full contamination scan su tutti gli XML;
5. blocca residui di anno, cliente, NACE, search total, final sample, PLI e average method.

### 2.3 Se non esiste modello anno precedente

Non inventare titolo, report o struttura. Chiedi:

```text
Non trovo un modello dell’anno precedente o un template approvato da riusare. Qual è il titolo esatto della skill/report da creare?
```

### 2.4 Se il modello esiste ma non è perfettamente coerente

Usalo solo se lo dichiari in QA come `TEMPLATE_CLONE_CANDIDATE`, non `FINAL`. Se contiene famiglia sbagliata o appendici incompatibili, usa un gold alternativo solo con motivazione esplicita.

---

## 3. Average Method Lock — media ponderata vs media semplice

### 3.1 Regola

Prima di popolare tabelle e narrativa, blocca il metodo:

- `WEIGHTED_AVERAGE` = media ponderata / weighted average;
- `SIMPLE_AVERAGE` = media semplice / arithmetic average;
- `NOT_APPLICABLE` = se il PLI non richiede media su più anni.

Se il workbook contiene entrambe le colonne (`Weighted Average` e `Average`) e l'utente non ha specificato il metodo, chiedi:

```text
Devo usare la media ponderata (weighted average) o la media semplice (simple average) per il report?
```

### 3.2 CASE_LOCK obbligatorio

```json
{
  "pli": "NCP",
  "pli_formula": "EBIT / Total Costs",
  "average_method": "WEIGHTED_AVERAGE | SIMPLE_AVERAGE | NOT_APPLICABLE",
  "average_source_sheet": "Final Set",
  "average_source_column": "Weighted Average | Average",
  "period": "2024-2022"
}
```

### 3.3 Coerenza narrativa

Se `WEIGHTED_AVERAGE`, usare ovunque:

- `Weighted Average NCP`;
- `Weighted Average NCP %`;
- `weighted average NCP extracted from the Excel workbook`.

Se `SIMPLE_AVERAGE`, usare ovunque:

- `Average NCP`;
- `Average NCP %`;
- `simple average NCP` o `arithmetic average NCP`.

Blocca se tabella e narrativa usano metodi diversi.

---

## 4. CASE_LOCK.json — gate zero

Creare sempre un CASE_LOCK prima dell'iniezione dati.

Campi minimi:

```json
{
  "client": "",
  "transaction": "",
  "tested_party_or_activity": "",
  "geography": "",
  "report_profile": "STANDARD | CRA",
  "pli": "NCP | ROS | ADJUSTED_ROS | other",
  "pli_formula": "",
  "pli_workbook_label": "es. Adj. Operating Margin (se diverso dal label report)",
  "average_method": "WEIGHTED_AVERAGE | SIMPLE_AVERAGE | NOT_APPLICABLE",
  "period": "",
  "fiscal_year": "",
  "prior_year_model_found": true,
  "prior_year_model_file": "",
  "template_source_file": "",
  "workbook_source_file": "",
  "tp_catalyst_release": "",
  "search_total": null,
  "quantitative_rejected": null,
  "after_quantitative": null,
  "qualitative_rejected": null,
  "final_sample": null,
  "appendix_profile": "A-G | A-H | A-I | custom",
  "cra_lock_file": "CRA_LOCK.json se report_profile = CRA, altrimenti null",
  "release_state": "DATA_DRAFT | TEMPLATE_CLONE_CANDIDATE | RECONCILED_CANDIDATE | STYLE_LOCK_CANDIDATE | FINAL"
}
```

Se CASE_LOCK contraddice il report, blocca.

---

## 4-bis. Country Risk Adjustment Profile — riconoscimento e gate dedicati

### 4-bis.1 Profile Detection Gate — obbligatorio, automatico

Prima di scegliere template e struttura, classifica il report come `STANDARD` o `CRA`. Dichiara `report_profile = CRA` se rilevi **almeno uno** di questi segnali, anche se l'utente non nomina mai il country risk adjustment:

**Segnali dal workbook:**

- sheet `Country risk adjustment` (anche se quasi vuoto: spesso contiene solo il titolo e il mercato target, es. `USA Market`);
- sheet `ERPs by country FY xx` o dataset Damodaran / default spread / country risk premium / Moody's rating;
- PLI etichettato `Adj. Operating Margin`, `Adjusted ROS`, `Adj. ROS`, `Adjusted margin`;
- colonne ROCE / Capital Employed / Adjusted EBIT nel Final Set o in Analisi.

**Segnali dal report o dalla richiesta:**

- titolo/nome file contenente `CRA`, `adjusted`, `country risk`;
- tested party in un mercato (es. North America) e comparables in un altro (es. Europa);
- dual search: una search fallita/insufficiente sul mercato della tested party + una search sul mercato dei comparables;
- sezioni `Sample before Country Risk Adjustment`, `Country Risk Adjustment`, `Example of the application of the adjustment`, `Final Sample` post-adjustment;
- appendice `Details of Country Risk Adjustment`.

Se i segnali sono ambigui (es. solo la sheet ERPs presente ma PLI non-adjusted), fai **una sola domanda**:

```text
Il workbook contiene dati di country risk ma il PLI non risulta adjusted. Il report deve applicare il Country Risk Adjustment (profilo CRA) oppure no?
```

Non applicare mai silenziosamente il profilo sbagliato: un report CRA compilato come STANDARD perde le sezioni 2.3–2.5 e l'Appendix C; un report STANDARD compilato come CRA inventa un adjustment inesistente. Entrambi sono FAIL CRITICAL.

### 4-bis.2 CRA_LOCK.json — obbligatorio se profilo CRA

Congela la meccanica dell'adjustment prima di popolare qualsiasi tabella:

```json
{
  "tested_party_market": "USA and Canada",
  "tested_party_risk": "0.00% (risk free nel dataset usato)",
  "comparables_market": "Europe (EU27 + Norway, Switzerland, UK)",
  "comparables_countries": ["Belgium", "Bulgaria", "France", "Germany", "Greece", "Italy", "Poland", "Romania", "Spain", "Sweden", "United Kingdom"],
  "risk_source": "Damodaran default spread (Moody's rating-based)",
  "risk_source_sheets": ["ERPs by country FY 23", "ERPs by country FY 22", "ERPs by country FY 21"],
  "delta_convention": "delta = risk(tested_party_country) - risk(comparable_country); negativo se il comparable è più rischioso",
  "adjustment_chain": "ROCE = EBIT/(TotalAssets - CurrentLiabilities); AdjROCE = ROCE + delta; AdjEBIT = AdjROCE * CapitalEmployed; AdjROS = AdjEBIT / Turnover",
  "adjusted_pli_report_label": "Adjusted ROS",
  "adjusted_pli_workbook_label": "Adj. Operating Margin",
  "years": ["2023", "2022", "2021"],
  "example_company": "nome + BvD ID della società usata nella sezione esempio",
  "dual_search": true,
  "failed_search_market": "North America",
  "failed_search_evidence": "screenshot/tabella Table 2 senza criterio EBIT"
}
```

### 4-bis.3 Struttura obbligatoria del report CRA

Il profilo CRA modifica l'architettura standard. Verifica la presenza e l'ordine di:

1. **Executive Summary** con la giustificazione della dual search: mercato della tested party insufficiente → search sul mercato alternativo → adjustment sui comparables. Il PLI dichiarato è l'**adjusted** PLI.
2. **Search Process a due rami**: `The [Tested-Party-Market] Search` (fallita, con evidenza) + `The [Comparables-Market] Search` (completa, con i 13 step, NACE/NAICS/US SIC, ecc.).
3. **Further Selection Process** (invariato rispetto al profilo standard, con la sua arithmetic).
4. **Sample before Country Risk Adjustment** — tabella ROS *non adjusted* per l'intero final sample (Company name, BvD, Country, Weighted average ROS, ROS per anno).
5. **Country Risk Adjustment** — narrativa Damodaran + **tabella Default Risk per paese/anno** + **tabella Δ per paese/anno** (stessi paesi, segno invertito).
6. **Example of the application of the adjustment** — una società reale del sample con la catena completa in 5 tabelle: financial data → ROCE → adjusted ROCE → adjusted EBIT → adjusted ROS.
7. **Final Sample** — tabella *adjusted* ROS per l'intero sample.
8. **Summary of Results** — statistiche (Min, Q1, Median, Q3, Max) calcolate sull'**adjusted** weighted average PLI.
9. **Appendix C. Details of Country Risk Adjustment** — tre tabelle full-sample: financial data + ROS (part 1), ROCE/Capital Employed (part 2), country risk Δ + AdjROCE + AdjEBIT + AdjROS.
10. Appendici restanti coerenti col profilo dichiarato in CASE_LOCK (nel gold Valbruna: A TP Catalyst, B Glossary, C CRA, D Results, E Financial Analysis, F Details of Comparables, G Rejection Matrix — **senza** Appendix E descrizioni-società separata: le descrizioni stanno in F).

### 4-bis.4 CRA Chain Gate — aritmetica obbligatoria

Per **ogni** società e **ogni** anno, ricalcola e riconcilia con tolleranza da arrotondamento (±0.01 p.p. sulle percentuali, ±1 sulle migliaia):

```text
CapitalEmployed = TotalAssets - CurrentLiabilities
ROCE            = EBIT / CapitalEmployed
Δ               = risk(tested_party) - risk(country(comparable))
AdjROCE         = ROCE + Δ
AdjEBIT         = AdjROCE × CapitalEmployed
AdjROS          = AdjEBIT / Turnover
```

Gate aggiuntivi:

- **Zero-delta invariance**: per i paesi con Δ = 0 (es. Germania, Svezia se pari al mercato tested party), adjusted = unadjusted su ogni riga e ogni anno. Qualsiasi differenza è FAIL.
- **Sign gate**: se il paese del comparable ha default risk maggiore della tested party, Δ è negativo e AdjROS ≤ ROS. Un adjustment che aumenta il ROS di un comparable più rischioso è FAIL.
- **Tabella Default Risk vs tabella Δ**: stessi paesi, stesso ordine, valori identici a segno invertito (Δ della tested party = 0.00%).
- **Country coverage**: l'insieme dei paesi nelle tabelle Default Risk/Δ = insieme dei paesi presenti nel final sample. Paese mancante o paese orfano = FAIL.
- **Example chain**: la società esempio deve riconciliare lungo tutta la catena. Il caso gold Valbruna contiene difetti reali da NON fotocopiare: ROCE 2023 dichiarato 15.16% contro 15.66% ricalcolato, ROCE 2022 che cambia da 43.88% a 44.88% tra due tabelle adiacenti, Turnover 2021 diverso tra sezione 2 e Appendix C (174,280 vs 173,847). Se cloni un modello CRA, ricalcola l'esempio da zero e correggi; registra la correzione in Error Detective.
- **Before/After alignment**: Table "before CRA" e Table "Final Sample" devono avere le stesse società, stessi BvD ID, stesso ordine e stesso count. Solo i valori PLI cambiano.
- **Statistics on adjusted**: Min/Q1/Median/Q3/Max del Summary e dell'Executive Summary calcolati sulla colonna adjusted weighted average, non su quella unadjusted. Executive Summary Table 1 = Summary Table = Appendix D.

### 4-bis.5 Terminology & Period Lock CRA

- Mappa esplicitamente il label workbook → label report (es. `Adj. Operating Margin` → `Adjusted ROS`) in CASE_LOCK/CRA_LOCK; non mescolare i due label nel testo.
- Usa ovunque `Adjusted ROS` / `Adj. Weighted average ROS` se profilo CRA; mai `NCP` residuo.
- **Year residue gate**: il periodo dei comparables (es. 2023–2021 per un report FY 2024) deve essere identico in Executive Summary, caption delle tabelle, Summary of Results e Appendix C. Il gold Valbruna contiene il residuo reale `the years 2020 to 2022` nel Summary con caption `2023 – 2021`: bloccalo.
- Il fiscal year del report (FY 2024) e il periodo dati comparables (2023–2021) possono legittimamente differire per data availability: non "correggerli" allineandoli, ma verifica che ciascuno sia usato nel posto giusto.

### 4-bis.6 Editorial Gate — aggiunte profilo CRA

Blocca o correggi anche:

```text
United Sates            → United States
beard by a company      → borne by a company
herein after            → hereinafter
tested parties.,        → tested parties,
the country risk beard  → the country risk borne
```

---

## 5. DOCX handling e style lock

### 5.1 Regola DOCX

Un `.docx` è uno ZIP con XML interni. Per modifiche complesse:

1. unpack;
2. modifica XML mirata;
3. preserva proprietà di tabella e run;
4. pack;
5. valida package e visual evidence.

Non ricreare da zero documenti già esistenti se c'è un modello.

### 5.2 Preservare tabelle native

Non semplificare tabelle native. Conserva:

- `w:tblPr`;
- `w:tblGrid`;
- `w:tcPr`;
- `w:gridSpan`;
- `w:vMerge`;
- `w:shd`;
- bordi;
- larghezze colonne;
- margini celle;
- font e run properties.

Per merged tables, non affidarti solo a `python-docx` perché può esporre celle duplicate o merged in modo fuorviante. Usa anche XML raw audit.

### 5.3 Caption e stile

Preserva:

- caption maroon SBNP;
- white-on-dark header dove previsto;
- section architecture del template;
- loghi e cover identity;
- footer coerenti con cliente/transazione corrente.

---

## 6. Table 2 / Table 5 Search Process Gate

### 6.1 Fonte dati

Table 2 e Appendix D/Table 5 devono derivare da `Search summary` / export TP Catalyst corrente.

Non riusare vecchi NACE, vecchi paesi, vecchi anni o vecchi count del template.

### 6.2 Boolean Search row

La riga Boolean Search deve essere isolata e pulita.

Pass example:

```json
"table2_boolean_row": [
  "Boolean search: 1 and 2 and 3 ...",
  "",
  ""
]
```

oppure, se il modello usa una cella merged reale:

```json
"table2_boolean_row": [
  "Boolean search: 1 and 2 and 3 ..."
]
```

Fail example:

```text
Boolean search ...   Shareholders with a specific number of subsidiaries: None   5,365,373
```

### 6.3 Total row

Il totale della search process è il risultato TP Catalyst dopo Boolean search, non il final sample post-screening.

Esempio corretto:

```text
Search result: 121
Final sample: 19
```

Blocca se `121` e `19` sono scambiati o narrati in modo ambiguo.

### 6.4 Table 2 = Table 5

Appendix D/Table 5 deve essere coerente con Table 2 per:

- criteri;
- count;
- Boolean search;
- total row;
- release TP Catalyst.

### 6.5 Dual search (profilo CRA)

Nei report CRA esistono **due** search: quella fallita sul mercato della tested party (spesso solo screenshot, senza criterio EBIT) e quella completa sul mercato dei comparables. Regole:

- non fondere le due search in una tabella sola;
- il search total della narrativa (es. `596 potentially comparable entities`) si riferisce alla search sul mercato dei comparables, non a quella fallita;
- la release TP Catalyst (update number, version, mese) deve essere identica nelle due sezioni;
- lo screenshot della search fallita è **data-bearing**: se non hai lo screenshot corrente verificato, sostituisci con tabella nativa dai dati `Search summary`, mai lasciare lo screenshot vecchio.

---

## 7. Further Selection Process Gate

### 7.1 Arithmetic obbligatoria

```text
initial_population - quantitative_rejected = after_quantitative
after_quantitative - qualitative_rejected = final_sample
sum(quantitative categories) = quantitative_rejected
sum(qualitative categories) = qualitative_rejected
```

### 7.2 Tabella e narrativa devono coincidere

La tabella Further Selection e il testo successivo devono riportare gli stessi numeri.

Se il workbook dice:

```text
121 - 0 - 102 = 19
```

la narrativa deve dire:

```text
The total number of rejected companies with the first Quantitative screening was 0.
The total number of rejected companies with the second Qualitative screening was 102.
Therefore, at the end of the overall screening process, 19 are the accepted companies.
```

### 7.3 Blocca residui old-template

Blocca se il contesto Further Selection contiene vecchi numeri non riconciliati, ad esempio:

- `749`;
- `24`;
- `482`;
- `773` come count screening;
- `439`;
- `43 are the accepted companies`.

### 7.4 Numeric residue context rule

Non bloccare un numero solo perché compare come sottostringa di un identificativo. Esempio: `773` dentro un BvD ID non è automaticamente un vecchio screening count.

Blocca solo se il numero appare nel contesto di screening, narrative, table count o rejection totals.

---

## 8. Appendix E Company Descriptions Gate

### 8.1 No placeholders

Blocca FINAL se una società contiene:

```text
The company is included in the final set as comparable based on the screening performed in the workbook.
A detailed business description should be confirmed during final review.
```

### 8.2 Gerarchia fonti

Usa nell'ordine:

1. `Full overview` del workbook;
2. `Trade description` del workbook;
3. descrizione prior-year per stessa società / BvD ID;
4. descrizione fornita dall'utente;
5. descrizione conservativa NACE-based, con warning QA se non validata esternamente.

### 8.3 Coerenza stile/lunghezza

Allinea le descrizioni alla lunghezza media e allo stile del report. Evita frasi generiche e troppo brevi.

### 8.4 All names present

Appendix E deve contenere tutti i nomi del final sample. Se manca anche una società, blocca.

---

## 9. Excel-vs-Report Gate

Confronta workbook e report su:

- Search Process;
- Further Selection;
- final sample names and BvD IDs;
- PLI annual values;
- average method values;
- min, Q1, median, Q3, max;
- **se profilo CRA**: default risk per paese/anno vs sheet ERPs/Damodaran, Δ per paese/anno, ROCE, Capital Employed, Adjusted EBIT, Adjusted ROS per società/anno, statistiche calcolate sulla colonna adjusted;
- Appendix E descriptions;
- Appendix F/G/H tables;
- fiscal years and release info.

Usa sia visible extraction (`python-docx` / pandoc) sia raw XML scan. Non basta cercare in `word/document.xml`: includi header, footer, footnotes, endnotes, comments, settings, rels e custom XML.

---

## 10. Visual Object Gate

Classifica ogni immagine/drawing:

- logo / branding;
- decorative;
- data-bearing screenshot.

Preserva loghi. Sostituisci screenshot dati vecchi con tabelle native workbook-derived quando non hai screenshot corrente verificato.

Blocca se resta uno screenshot dati con valori vecchi.

---

## 11. Editorial Gate

Blocca FINAL se trovi:

```text
data, that may
companies comparable
forth step
eight step
nineth
reported:-
LowerQuartile
UpperQuartile
TO BE CONFIRMED
TODO
placeholder
Oprating
uncomparable
```

Correggi anche:

- `companies has been subjected` → `companies have been subjected`;
- `Manual criteria exclusion are following` → `Manual criteria for exclusion are the following`;
- `Belong to a Company` → `Belong to a Group` solo se coerente con Excel/current categories; altrimenti usare categoria reale.

---

## 12. Error Detective Protocol

Ogni bug o gate failure deve registrare:

```text
Symptom:
Impact:
Evidence:
Root Cause:
Minimal Fix:
Verification:
Prevention:
```

Applicare questo protocollo a:

- table malformed;
- Boolean row contamination;
- wrong search total;
- wrong NACE/geography/year;
- further selection mismatch;
- average method mismatch;
- Appendix E placeholders;
- old client contamination;
- style drift;
- stale screenshots.

---

## 13. LLM Council Gate

Usa council sintetico quando:

- il report è career-critical / client-facing;
- ci sono stati errori ripetuti;
- bisogna scegliere tra mantenere modello vecchio o cambiare template;
- il QA segnala WARN critici ma non FAIL.

Output minimo:

```markdown
### Contrarian
Rischio più probabile e cosa può fallire.

### Executor
Fix concreto più rapido e verificabile.

### Chairman
Decisione: deliver / review candidate / block.
```

Non usare council per sostituire dati o QA. Il council giudica, non inventa.

---

## 14. Required Artifacts

Prima di consegnare un DOCX, produrre:

1. `CASE_LOCK.json`
2. `CRA_LOCK.json` — obbligatorio se `report_profile = CRA`
3. `QA.json`
4. `STYLE_LOCK_REPORT.md`
5. `INCIDENTS_AND_FIXES.md` se ci sono stati errori o gate failure
6. opzionale `COUNCIL_VERDICT.md` per casi high-stakes

---

## 15. Release State Machine

```text
DATA_DRAFT
  ↓ Excel data extracted but no template fidelity
TEMPLATE_CLONE_CANDIDATE
  ↓ prior-year/model cloned and data injected
RECONCILED_CANDIDATE
  ↓ Excel-vs-report and arithmetic passed
STYLE_LOCK_CANDIDATE
  ↓ design, table, appendix, editorial gates passed
FINAL
  ↓ all gates passed + human Word visual review completed
```

Se `visual_word_review = OPEN`, non usare `FINAL`.

---

## 16. Regression Suite

### v3.5 inherited tests

- REG-020: no old search screenshot values.
- REG-021: Appendix D caption followed by verified table/screenshot.
- REG-022: sequential, non-duplicated table captions.
- REG-023: no `forth step`, `eight step`, `companies comparable`, `reported:-`.
- REG-024: no `LowerQuartile` or `UpperQuartile` merged labels.
- REG-025: no placeholder company descriptions in FINAL.
- REG-026: Appendix H contains rejection matrix or approved omission note.

### v3.7 added tests from Amenduni incident

- REG-027: prior-year model search performed before report creation.
- REG-028: if no model exists, ask exact title before creating.
- REG-029: average method locked before populating PLI tables.
- REG-030: weighted/simple average labels match source columns.
- REG-031: Table 2 Boolean row clean.
- REG-032: Table 2 Total row equals search total, not final sample.
- REG-033: Table 5 mirrors Table 2.
- REG-034: Further Selection arithmetic reconciles.
- REG-035: Further Selection narrative matches table.
- REG-036: old 505 counts blocked contextually.
- REG-037: numeric residue check distinguishes counts from IDs.
- REG-038: Appendix E all final sample names present.
- REG-039: Appendix E no generic placeholder descriptions.
- REG-040: QA includes Error Detective RCA for any fixed defect.

### v3.8 added tests from Valbruna WHS USA CRA incident

- REG-041: profile detection eseguita prima della scelta template; `report_profile` presente in CASE_LOCK.
- REG-042: workbook con sheet ERPs/Damodaran o PLI `Adj.` → profilo CRA rilevato senza input utente.
- REG-043: CRA_LOCK.json presente e coerente con report se profilo CRA.
- REG-044: dual search — due sezioni distinte, stessa release TP Catalyst, search total riferito al mercato dei comparables.
- REG-045: tabella Default Risk e tabella Δ con stessi paesi e valori a segno invertito; tested party a 0.00%.
- REG-046: country coverage — paesi delle tabelle risk = paesi del final sample.
- REG-047: zero-delta invariance — paesi con Δ=0 hanno adjusted = unadjusted su tutti gli anni.
- REG-048: example chain ricalcolata da zero e riconciliata (CE, ROCE, AdjROCE, AdjEBIT, AdjROS).
- REG-049: before/after alignment — stesse società, BvD ID e ordine tra sample pre-CRA e Final Sample.
- REG-050: statistiche (Exec Summary, Summary of Results, Appendix D) calcolate sull'adjusted weighted average.
- REG-051: year residue — nessun periodo stale (es. `2020 to 2022` con caption `2023 – 2021`).
- REG-052: editorial CRA — nessun `United Sates`, `beard by`, `herein after`, `tested parties.,`.

---

## 17. Execution Output Template

When running this skill, respond using:

```markdown
## Sintesi
## Mente locale
## Piano operativo
## Modello anno precedente / template source
## Average method lock
## Esecuzione
## QA / Error detective
## Modifiche rispetto alla versione precedente
## Rischi residui
## Prossimi passi
```

---

## 18. Built-in Test Prompts for Skill Evaluation

Use these eval prompts when improving the skill:

### Eval 1 — Prior-year model and weighted average

```text
Ho un report TP dell’anno scorso e un nuovo Excel. Aggiorna il report mantenendo stile e usa la media ponderata NCP 2024-2022.
```

Expected:

- detects prior-year model;
- locks `WEIGHTED_AVERAGE`;
- preserves style;
- produces CASE_LOCK and QA.

### Eval 2 — No model available

```text
Crea una nuova skill/report TP ma non ho caricato nessun modello precedente.
```

Expected:

- asks exact title;
- does not invent report name;
- does not create from blank without confirmation.

### Eval 3 — Table 2 bug

```text
La riga Boolean search della Table 2 contiene anche il criterio Shareholders e il count. Correggi senza cambiare layout.
```

Expected:

- identifies Boolean row contamination;
- preserves table design;
- clears adjacent residual cells;
- verifies Table 5 too.

### Eval 4 — Further Selection mismatch

```text
Il Further Selection dice 773 e 439 ma Excel dice 121, 0, 102, 19. Sistema la tabella e il testo.
```

Expected:

- fixes table and prose;
- verifies `121 - 0 - 102 = 19`;
- blocks old counts contextually.

### Eval 5 — Appendix E placeholders

```text
Appendix E ha descrizioni generiche tipo included in final set. Sostituiscile con descrizioni coerenti.
```

Expected:

- applies source hierarchy;
- removes placeholders;
- all final sample company names present;
- QA caveat if external validation unavailable.

### Eval 6 — CRA profile detection

```text
Ho un nuovo Excel per Valbruna wholesalers USA/Canada FY 2025 e il report dell'anno scorso. Aggiorna il report.
```

Expected:

- rileva sheet ERPs/Damodaran e PLI adjusted nel workbook;
- dichiara `report_profile = CRA` senza che l'utente lo chieda;
- produce CRA_LOCK.json;
- mantiene la struttura before/adjustment/example/final sample + Appendix C.

### Eval 7 — CRA chain bug

```text
Nella sezione esempio il ROCE 2022 è 43.88% in una tabella e 44.88% in quella dopo. Sistema.
```

Expected:

- ricalcola la catena da EBIT/CE del workbook;
- identifica il valore corretto e propaga AdjROCE/AdjEBIT/AdjROS;
- registra RCA in Error Detective;
- verifica anche le altre righe dell'esempio.

### Eval 8 — Wrong profile guard

```text
Crea il report standard NCP per questo workbook.
```

(con workbook contenente sheet Country risk adjustment e PLI Adj. Operating Margin)

Expected:

- segnala il conflitto tra richiesta STANDARD e segnali CRA;
- fa una sola domanda di conferma profilo;
- non genera silenziosamente un report senza adjustment.

---

## 19. Changelog

### v3.8.0 — 2026-07-08

- Added Country Risk Adjustment Profile (sez. 4-bis): profile detection automatica STANDARD vs CRA da workbook e report.
- Added CRA_LOCK.json con delta convention, adjustment chain, risk source e dual search evidence.
- Added struttura obbligatoria report CRA: dual search, sample before CRA, tabelle Default Risk/Δ, example chain a 5 tabelle, final sample adjusted, Appendix C a 3 tabelle.
- Added CRA Chain Gate: ricalcolo per società/anno, zero-delta invariance, sign gate, country coverage, before/after alignment, statistics-on-adjusted.
- Added Terminology & Period Lock CRA (mapping Adj. Operating Margin ↔ Adjusted ROS, year residue gate).
- Added dual-search rules alla sezione Search Process.
- Added editorial fixes CRA (`United Sates`, `beard by`, `herein after`).
- Added REG-041…REG-052 e Eval 6-8 dal caso gold Valbruna WHS USA CRA FY 2024 (che contiene difetti reali documentati: ROCE 15.16% vs 15.66%, 43.88% vs 44.88%, turnover 2021 incoerente, residuo `2020 to 2022`).

### v3.7.0 — 2026-07-03

- Added mandatory Prior-Year Model Gate.
- Added exact-title question if no model exists.
- Added Weighted vs Simple Average Lock.
- Added Table 2/Table 5 Boolean row and Total row integrity gates.
- Added Further Selection Process reconciliation gate based on current Excel/Analisi.
- Added contextual numeric residue logic to avoid false positives from BvD IDs.
- Added Appendix E source hierarchy and all-names-present gate.
- Added Error Detective RCA protocol.
- Added LLM Council lightweight verdict for high-stakes report delivery.
- Added built-in eval prompts for skill validation.

### v3.5 baseline

- Preserved final style lock, table numbering, appendix completeness, visual object gate, placeholder gate and Excel-vs-report gate.

---

## 20. Final Rule

A report is deliverable only when all dimensions pass:

1. **Template fidelity** — prior-year/model style, structure and native tables preserved.
2. **Excel/data reconciliation** — search, screening, final sample, statistics and average method match workbook.
3. **Style/design/tone fidelity** — SBNP identity and formal TP wording preserved.
4. **Appendix/visual evidence completeness** — appendices, descriptions, tables and images verified.
5. **Profile correctness** — report_profile (STANDARD/CRA) detected and, per i report CRA, CRA Chain Gate passed end-to-end.

If any CRITICAL or HIGH issue remains, deliver only a QA failure report and do not call the output FINAL.
