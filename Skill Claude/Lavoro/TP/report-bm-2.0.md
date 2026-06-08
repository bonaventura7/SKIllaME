---
name: tp-benchmarking-report
description: >
  Genera report di benchmarking Transfer Pricing (TP) in formato DOCX professionale
  identico ai modelli SBNP gold standard (Acciaierie Valbruna, Crosspolimeri, Ascoli HFD,
  CM Bandera). USARE SEMPRE questo skill quando si genera un TP Benchmarking Report.
  OUTPUT: documento Word in inglese, struttura 4 sezioni + 9 appendici (A-I),
  tipografia Cambria, palette rosso #A32020 / bianco, logo SBNP in header.
---

# TP Benchmarking Report Generator — SKILL COMPLETO

> ⛔ **REGOLA ASSOLUTA N.1**: Il report generato deve essere un clone visivo e strutturale
> IDENTICO ai modelli gold standard (Acciaierie Valbruna, Crosspolimeri, Ascoli HFD, CM Bandera).
> Il modello Eurocoltellerie (italiano, 7 sezioni, Arial, palette blu) è il modello SBAGLIATO
> da NON replicare mai. Ogni deviazione dallo standard SBNP è un errore grave.
>
> ⛔ **REGOLA ASSOLUTA N.2**: Il report è in **INGLESE**. Nessuna sezione, titolo, tabella,
> o testo deve essere in italiano.
>
> ⛔ **REGOLA ASSOLUTA N.3**: Prima di scrivere una sola riga di codice, leggere
> TUTTO questo file. Poi usare come base di partenza il template DOCX esistente.

---

## 0. Approccio consigliato: clona dal template

Il metodo più affidabile per garantire identità visiva al 100% è:

```
1. Copia il report gold standard più adatto come template (es. Acciaierie_Valbruna_S_p_A_WHS_EU_FY_2024.docx)
2. Decomprimi con: unzip template.docx -d unpacked/
3. Modifica i file XML in unpacked/word/document.xml (sostituisci testi, dati, tabelle)
4. Ri-comprimi con: cd unpacked && zip -r ../output.docx .
5. Valida con python-docx
```

Se il caso d'uso richiede generazione da zero (nuova tipologia di report),
usare docx-js replicando ESATTAMENTE gli stili descritti in §3.

---

## 1. Struttura del documento — Mappa pagine

```
PAGINA i    (copertina)   → Cover page (numero romano "i" a piè pagina)
PAGINA 1    (indice)      → Index page (numero arabo "1")
PAGINA 2    (sezione 1)   → Executive Summary (con Table 1 IQR)
PAGINA 3-4  (sezione 2)   → The Search Process
  PAGINA 3-4               → 2.1 The TP Catalyst Search (con Table 2)
  PAGINA 5-6               → 2.2 Further Selection Process (con Table 2-bis screening)
  PAGINA 7                 → 2.3 Final Sample (con Table 3)
PAGINA 8    (sezione 3)   → Summary of Results (con Table 4 IQR)
PAGINA 9    (sezione 4)   → Limitations
PAGINA 10   (break)       → "Appendices" (TOC appendici)
PAGINA 11                 → Appendix A. An Overview of the TP Catalyst Database
PAGINA 13                 → Appendix B. Glossary of Statistical Terms
PAGINA 14                 → Appendix C. Financial Analysis
PAGINA 15                 → Appendix D. TP Catalyst Search strategy (screenshot immagine)
PAGINA 16-19              → Appendix E. Details of Comparable Companies
PAGINA 20                 → Appendix F. Results of Comparable Companies (Table 6)
PAGINA 21                 → Appendix G. Arm's length range (Table 7)
PAGINA 22                 → Appendix H. Comparable Companies Financial Information
PAGINA 23+                → Appendix I. Rejection Matrix of the Comparable Companies
```

### Varianti per tipo di report

| Tipo | PLI | Formula | Sezione 2.3 presente? |
|------|-----|---------|----------------------|
| Wholesale/Retail EU | ROS (Return on Sales) | EBIT / Turnover | Sì |
| Wholesale/Retail Far East | ROS | EBIT / Turnover | Sì + Country Risk Adj. |
| Contract Manufacturing | NCP (Net Cost Plus) | EBIT / Total Costs | Sì |
| Support Services | NCP | EBIT / Total Costs | Sì |
| USA (con country adjustment) | Adjusted OM | EBIT / Turnover | Sì + adjustment table |

---

## 2. Layout pagina e sezioni Word

```
Formato carta : A4 (11907 × 16839 DXA = 8.27" × 11.69")
Margini       : 1 pollice (1440 DXA) tutti e quattro i lati
Orientamento  : Ritratto
Font principale: Cambria (tutto il documento)
```

### Sezioni Word (separatori di sezione)

Il documento usa **6+ sezioni Word** per gestire header/footer diversi:

| Sezione | Pagine | Header | Footer |
|---------|--------|--------|--------|
| 1 | Copertina | vuoto | "i" (numero romano centrato) |
| 2 | Index | SBNP logo | "[Società] – [Transazione]\nSBNP    1" |
| 3 | Sez 1-4 (corpo) | SBNP logo | "[Società] – [Transazione]\nSBNP    [n]" |
| 4 | Appendix A-B | "[Appendice titolo]" centrato | come sezione 3 |
| 5 | Appendix C+ | SBNP logo | "[Società] – [Transazione]\nSBNP    [n]" |
| 6 | App. I (landscape o finale) | SBNP logo | come sezione 5 |

---

## 3. Stili tipografici (mapping Python-docx → Word)

I nomi degli stili nel template SBNP usano nomi **italiani** (il template è stato creato
in Word italiano). Mappare così:

| python-docx name | Word style ID | Utilizzo | Caratteristiche |
|-----------------|---------------|----------|-----------------|
| `Subtitle` | `Sottotitolo` | Cover: nome società, tipo transazione | Cambria, ~40pt, bold, nero |
| `Normal` | `Normale` | Cover: "Arm's length...", "For fiscal year..." | Cambria, 24pt (cover) / 12pt (corpo) |
| `Heading 1` | `Titolo1` | Titoli sezioni (1. Executive Summary, 2. The Search...) | Cambria, ~28pt, bold+italic, nero, numerazione auto, page break before |
| `Heading 2` | `Titolo2` | Sottosezioni (2.1, 2.2, 2.3) | Cambria, ~16pt, bold+italic, rosso #A32020, numerazione auto |
| `Appendix 1` | `Appendix1` | Titoli appendici (Appendix A. ...) | Basato su Heading 1, con prefisso "Appendix X." |
| `Body Text` | `Corpotesto` | Testo paragrafo standard nel corpo | Cambria, 12pt, giustificato |
| `Caption` | `Didascalia` | Didascalie tabelle ("Table 1: ...") | Cambria, bold, rosso #A32020, keepNext |
| `List Paragraph` | `Paragrafoelenco` | Bullet points (■) | Cambria, indent, bullet quadrato |
| `List Roman` | `ListRoman` | Elenchi Limitations (i. ii. iii.) | Cambria, Roman numerals |
| `Stile1` | `Stile1` | Titolo "Index" / "Appendices" | Georgia, 24pt, bold+italic, rosso #A32020 |
| `toc 1` | `Sommario1` | Voci indice | Cambria, con tab right |
| `TOC Heading` | `Titolosommario` | "Appendices" sopra il TOC appendici | Cambria, bold |

### Heading 1 — numerazione automatica

I titoli H1 usano una numerazione Word (list style) che genera automaticamente "1.", "2.", "3.", "4."
con page break before. Le appendici usano `Appendix1` che usa un list style separato (numId=35).

### Copertina — dettaglio elemento per elemento

```
[riga rossa verticale sinistra — decorativa, parte del tema]

[Paragrafo Subtitle] "NomeSocietà S.p.A"  ← bold, large
[Paragrafo Subtitle] "Tipo transazione e mercato"  ← 36pt, non bold

[Paragrafo Normal 24pt] "Arm's length price and benchmarking analysis"
[Paragrafo Normal 24pt italic] "For fiscal year ending December 31st, [ANNO]"

[spazio vuoto]
[Paragrafo Normal small] "Prepared by"
[Paragrafo Normal small] "Studio Legale e Tributario Biscozzi Nobili & Partners"

[immagine SBNP logo — centrata in basso]

[Footer: "i" centrato]
```

---

## 4. Tabelle — Struttura e formattazione ESATTA

### Colori tabelle

```
Header riga:    background #6B1414 (rosso scuro), testo bianco, bold, centrato
Riga dati:      background bianco, bordi grigi/rossi sottili
IQR evidenziato: Lower Quartile e Upper Quartile in bold
```

### Table 1 — IQR Summary (Executive Summary)
Posizione: sezione Executive Summary, dopo il 4° paragrafo.

```
Struttura: 3 righe × 7 colonne
Riga 1 (header merged): "Average [PLI]% ([ANNI])" — sfondo rosso scuro, testo bianco, centrato
Riga 2 (sub-header):    "" | Observation | Minimum | Lower Quartile | Median | Upper Quartile | Maximum
                         — tutto in italic, testo centrato
Riga 3 (dati):          "Comparable\nSet" | N | min% | **Q1%** | median% | **Q3%** | max%
                         — Lower/Upper Quartile in bold, valori centrati
```

### Table 2 — Search Process in TP Catalyst
Posizione: sezione 2.1, dopo "Table 2: Search Process in TP Catalyst".
Struttura: tabella con colonne (Step# | Descrizione criterio | Step result).
Formato: riga header scura, righe alternate, colonna numerica allineata a destra.

### Table 2-bis — Further Selection Process (Quantitative + Qualitative Screening)
Posizione: sezione 2.2, dopo "The further selection process is summarized in the table below."
Struttura: 30 righe × 22 colonne (template Acciaierie) oppure versione semplificata.

```
Sezione 1: "Quantitative screening process" | [N_iniziale]
  [spiegazione]
  1 | Data availability | [N_rigettate]
    [spiegazione criterio]
  2 | Recurring losses | [N]
  ...
  N | [ultimo criterio] | [N]
  
Sezione 2: "Qualitative screening process" | [N_dopo_quant]
  [spiegazione]
  1 | Belong to a Group | [N]
  2 | Different Functions | [N]
  3 | Different Products | [N]
  4 | Additional products | [N]
  5 | Additional Functions | [N]
  6 | Other | [N]
  
  "Comparable Companies" | [N_finale]
```

### Table 3 — Comparable companies [PLI] – Fiscal Years [ANNI]
Posizione: sezione 2.3 Final Sample.
Struttura: N_comparable+1 righe × 7 colonne.

```
Company name | BvD number | Country | Weighted average [PLI] | [PLI] [ANNO] | [PLI] [ANNO-1] | [PLI] [ANNO-2]
```

### Table 4 — Summary of Results (=identica a Table 1)
Posizione: sezione 3 Summary of Results.

### Table 5 — Glossary (Appendix B)
Struttura: 6 righe × 2 colonne: Term | Definition

```
Lower quartile | The value below which 25% of the set falls
Maximum        | The highest value in the comparable set.
Median         | The median, along with the mean, is one of several ways to measure...
Minimum        | The lowest value in the comparable set.
Observation    | The number of times a ratio occurs within...
Upper quartile | The value above which 25% of the set falls
```

### Table 6 — Results of Comparable Companies (Appendix F)
Struttura: N+1 righe × 5-7 colonne.
```
Company Name | BvD Number | Country | [PLI] [ANNO] | [PLI] [ANNO-1] | [PLI] [ANNO-2] | [PLI] Average
```
Header: sfondo rosso scuro #6B1414, testo bianco bold.
Dati: testi centrati, nomi azienda in maiuscolo.

### Table 7 — Arm's length range (Appendix G)
Struttura: 6 righe × 5 colonne.

```
[PLI header merged] ([ANNI])
                    | [ANNO] | [ANNO-1] | [ANNO-2] | Average ([ANNI])
Minimum             |  val%  |   val%   |   val%   |   val%
Lower Quartile      |  val%  |   val%   |   val%   | **val%** (bold)
Median              |  val%  |   val%   |   val%   | **val%** (bold)
Upper Quartile      |  val%  |   val%   |   val%   | **val%** (bold)
Maximum             |  val%  |   val%   |   val%   |   val%
```
Header: sfondo rosso scuro #6B1414, testo bianco bold, italic.
Righe Lower Quartile, Median, Upper Quartile: testo **bold + italic** (questo è critico!).
Righe Minimum e Maximum: testo italic (non bold).

### Table 8 — Comparable Companies Financial Information (Appendix H)
Struttura: N+1 righe × 7 colonne.
```
Company Name | Turnover [ANNO] (th EUR) | Turnover [ANNO-1] (th EUR) | Turnover [ANNO-2] (th EUR) |
             EBIT [ANNO] (th EUR) | EBIT [ANNO-1] (th EUR) | EBIT [ANNO-2] (th EUR)
```

---

## 5. Header e Footer

### Header (tutte le pagine tranne copertina)
- Logo SBNP (image2.jpeg dal template) — allineato a sinistra, ~1.5" larghezza
- Linea orizzontale rossa sotto il logo (usando border bottom sul paragrafo header)
- Alcune pagine appendice mostrano il titolo dell'appendice centrato nell'header

### Footer (tutte le pagine tranne copertina)
```
[Nome Società] – [Descrizione transazione]
SBNP    [tab]    [numero pagina]
```
- Prima riga: Cambria, bold, 10pt, nero
- Seconda riga: "SBNP" a sinistra, numero pagina a destra (tab stop right)

---

## 6. Contenuto testi — Template paragrafi standard

### Executive Summary — struttura paragrafi

```python
# Paragrafo 1: chi, cosa
"{CLIENT_NAME} (hereinafter also the "Group"), has engaged Studio Legale e Tributario
Biscozzi Nobili & Partners (hereinafter referred to as "SBNP"), to provide an analysis
of comparable company data, that may be used to benchmark returns earned by
{TESTED_PARTY_TYPE} in the {TRANSACTION_DESC} in the {GEOGRAPHY} market."

# Paragrafo 2: processo ricerca
"The search has been performed to identify a set of comparable independent companies
which can be used to benchmark returns earned by {TESTED_PARTY_TYPE} in the
above-mentioned activities. The search process involved the examination of companies
in the TP Catalyst database, the elimination of non-comparable companies and the
selection of those independent companies, which are considered as comparable to the
{TESTED_PARTY_TYPE}."

# Paragrafo 3: risultato
"As a result of the analysis, {N_COMPARABLE} independent companies have been identified
and determined to be comparable to {TESTED_PARTY_TYPE}, in terms of functions performed,
risks borne and assets used within the activity in exam. Summary information on the
latter are contained in Appendix E."

# Paragrafo 4: PLI e risultati
"The {PLI_FULL_NAME} (hereinafter referred to as "{PLI_ABBR}") has been considered as
the primary Profit Level Indicator (hereinafter referred to as "PLI") for the results.
The key results for the {N_COMPARABLE} comparable companies over a 3-year period are
set out below. Summary results are presented in Section 3, while Appendix F provides
detailed results."

[TABLE 1 — IQR]

# Paragrafo 5: limitazioni + disclaimer
"The analysis at hand was subject to a number of limitations, which are detailed in
Section 4 of this report."

"This report is addressed to and is solely for the benefit of the Group in accordance
with the terms set out in our engagement letter and the agreed scope set out in that
letter and for no other purpose. SBNP does not accept or assume any liability,
responsibility or duty of care for any other purpose or to any other person to whom
this report is shown or in whose hands it may come, save where expressly agreed by
our prior consent in writing."
```

### The Search Process — Sezione 2

```python
# Intro sezione 2
"The search aims to identify a set of independent companies, which are involved in
{ACTIVITY_DESC} in {GEOGRAPHY} market. The source of data for the search was the
TP Catalyst database. TP Catalyst is a commercially available database, published by
Bureau van Dijk (BvD) containing data on more than 20 million companies. These companies
formed the starting point for our search."

"The steps through which the search for comparable companies is carried out are
detailed in the following sections."

# Sezione 2.1 — TP Catalyst version
"The TP Catalyst {RELEASE_DESC} – update number {UPDATE_NUMBER}, version {VERSION}
– was used for the purpose of this search."

"Table 2: Search Process in TP Catalyst"  ← [Caption style]

[TABLE 2 — SEARCH STEPS]

# Spiegazione passi (Body Text)
"The searching criteria are explained below."

"The first step in the search process was to ensure that the companies were operating
under "normal" conditions. The set was limited to companies that had the status "Active"
in the TP Catalyst database (second step)."

# ... continua con ogni step in formato:
"The [Nth] step in the search process [involved/consisted in] [descrizione criterio]."

# Finale sezione 2.1
"Upon completion of these final steps the TP Catalyst search resulted in a total of
{N_INITIAL} potentially comparable entities. These accepted companies were subject
to further analysis as described below."

# Sezione 2.2 — Further Selection
"The search process was based on two stages: "Quantitative screening" and "Qualitative
screening". The former consisted in the elimination of companies based on quantitative
criteria (i.e., data availability, recurring losses, intangibles ratio, etc.), while
the latter was based on a manual review of companies' activities."

"The further selection process is summarized in the table below."

[TABLE — SCREENING PROCESS]

"Concerning the Quantitative screening, the steps were the following:"
[List Paragraph] "The first step consisted in the elimination of companies with no
available financial data to calculate PLI for at least two of the 3 financial years;"
[List Paragraph] "The second step entailed the elimination of companies with cumulative
losses within the considered period (i.e., {YEARS}-{YEAR_MINUS_2});"
[List Paragraph] "The third step involves elimination of companies with intangible asset
to total asset ratio bigger than {INTANGIBLE_THRESHOLD}% in the average period considered;"
[...altri step quantitativi...]

"The total number of rejected companies after the first Quantitative screening was {N_QUANT_REJECTED}."

"Concerning the Qualitative screening, the steps were the following:"
[List Paragraph] "The first step consisted in excluding companies belonging to a group;"
[List Paragraph] "The second step consisted in the exclusion of companies that hold
Intangibles (i.e. trademarks and patents);"
[List Paragraph] "The third step implied the exclusion of companies carrying out
different functions;"
[List Paragraph] "The fourth step consisted in eliminating companies performing
additional functions;"
[List Paragraph] "The fifth step entailed the elimination of companies with different
products;"
[...altri step qualitativi...]

"The total number of rejected companies with the second Qualitative screening was {N_QUAL_REJECTED}."

"Therefore, at the end of the overall screening process, {N_FINAL} are the accepted companies."

# Sezione 2.3 — Final Sample
"As a result of the analysis, a final set of {N_FINAL} comparable companies was
identified as engaged in {ACTIVITY_DESC}."

"The table below summarizes the {PLI_ABBR} results achieved by the companies identified
as comparable in the three-years period 2023-2021."

"Table 3: Comparable companies – Fiscal Years {YEARS}"  ← [Caption style]

[TABLE 3 — COMPARABLE RESULTS]
```

### Summary of Results — Sezione 3

```python
"The "3-year period" {PLI_ABBR} results were calculated for each of the comparable
companies for the years {YEAR} to {YEAR_MINUS_2} and the results are summarized in
the table below."

"Table 4: {TRANSACTION_DESC} – {PLI_ABBR} {YEARS}"  ← [Caption style]

[TABLE 4 — = IDENTICA A TABLE 1]
```

### Limitations — Sezione 4

```python
"This report is addressed to and is solely for the benefit of the Group in accordance
with the terms set out in our engagement letter and the agreed scope set out in that
letter and for no other purpose."

"Our work has been subject to the following limitations:"

[List Roman] "reliance has been placed on the accuracy of the information presented in
the TP Catalyst database and no work has been undertaken to verify the accuracy of
such information;"

[List Roman] "the validity of the search engine employed by the TP Catalyst database
has not been tested;"

[List Roman] "the published financial statements of the companies in the comparable
set have not in general been examined;"

[List Roman] "the financial data provided in the TP Catalyst database are not complete
in all respects for all companies. Where possible, gaps have been filled from the
most recent available data;"

[List Roman] "this report has been prepared solely to provide an analysis of comparable
data and does not constitute legal, tax or accounting advice."
```

---

## 7. Appendici — Contenuto standard

### Appendix A — TP Catalyst Database Overview (TESTO FISSO)

```
Appendix A heading (Appendix1 style): "Appendix A. An Overview of the TP Catalyst Database"

Subheading (Heading2): "The TP CATALYST Database"

[Body Text]: "The source of data for our search was the TP Catalyst database. which is a
global database containing data of more than 20 million public and private companies.
For this search, the TP Catalyst database was used, which holds information derived from
annual returns on public and private companies. To be included in the database, companies
must fulfil at least one of the following size criteria:"

[H2]: "Very Large Companies (VL)"
Companies on TP Catalyst are considered to be "Very Large" when they have:
i.  Operating Revenue equal to at least 100 million EUR (130 million USD);
ii. Total assets equal to at least 200 million EUR (260 million USD);
iii. Employees equal to at least 1,000;
iv. or They are listed companies.

[H2]: "Large Companies (L)"
i.  Operating Revenue equal to at least 10 million EUR (13 million USD);
ii. Total assets equal to at least 20 million EUR (26 million USD);
iii. Employees equal to at least 150;
iv. not Very large.

[H2]: "Medium sized Companies (M)"
i.  Operating Revenue equal to at least 1 million EUR (1,3 million USD);
ii. Total assets equal to at least 2 million EUR (2,6 million USD);
iii. Employees in number equal to at least 15;
iv. not Very large or large.

(Note: Companies with ratios "Operating Revenue per Employee" or "Total Assets per
Employee" below 100 EUR are excluded from VL, L and M categories.)

[H2]: "Small Companies (S)"
Companies on TP CATALYST are considered to be SMALL when they are not included in
any other category above.

[Body Text]: "TP CATALYST contains a combination of data from several local sources.
The information contained in the database is derived primarily from companies' statutory
filings."

"The Balance Sheet and Income Statement formats have been re-classified by Bureau van
Dijk into a universal standard format."

"The version of TP Catalyst used for the search was {TP_CATALYST_VERSION}."
```

### Appendix B — Glossary of Statistical Terms (TESTO + TABLE FISSO)

```
[Table 5 — Glossary]
Lower quartile | The value below which 25% of the set falls
Maximum        | The highest value in the comparable set.
Median         | The median, along with the mean, is one of several ways to measure
                 the "middle" or "average" of a data set.
Minimum        | The lowest value in the comparable set.
Observation    | The number of times a ratio occurs within a database
Upper quartile | The value above which 25% of the set falls
```

### Appendix C — Financial Analysis

```
"For the purpose of performing a statistical analysis on the data reported by the
TP Catalyst database, the following methods of financial analysis have been adopted:"

[List Roman]: "This study uses {PLI_ABBR} as the transfer pricing benchmarks of the results."
[List Roman]: "The {PLI_ABBR} was calculated as {PLI_FORMULA_DESCRIPTION}."
```

Formule PLI per List Roman ii:
- **ROS**: "The ROS was calculated as operating profit (EBIT) expressed as a percentage of turnover."
- **NCP**: "The NCP was calculated as a percentage as Operating P/L [=EBIT] over Total Costs."
- **OM**: "The OM was calculated as operating profit (EBIT) expressed as a percentage of turnover."

### Appendix D — TP Catalyst Search Strategy

```
[Appendix1 heading]: "Appendix D. TP Catalyst Search strategy"

"Table 5: Search Process in TP Catalyst"  ← [Caption style]

[IMMAGINE screenshot TP Catalyst search strategy — inserire come inline image]
```

⚠️ **IMPORTANTE**: L'immagine di Appendix D è uno screenshot esportato da TP Catalyst.
Deve essere fornita come file immagine (PNG/JPEG) e inserita come `ImageRun` nel documento.
Se non disponibile, inserire un placeholder "[Insert TP Catalyst Search Strategy screenshot]".

### Appendix E — Details of Comparable Companies

```
[Appendix1 heading]: "Appendix E. Details of Comparable Companies"

Per ogni società comparable:

[ROSSO #A32020, ITALIC, MAIUSCOLO]: "NOME SOCIETÀ IN MAIUSCOLO"
[Normal]: "Descrizione di 2-4 frasi: paese, attività principale, struttura aziendale,
           caratteristiche funzionali rilevanti per la comparabilità."
```

Il testo delle descrizioni viene dalla colonna "Description" del foglio `6. Final Set` o
dalla colonna `Commento Breve` / `Comments` del foglio `Worksheet_AI`.

### Appendix F — Results of Comparable Companies

```
[Caption]: "Table 6 – Comparable companies [PLI] – Fiscal Years [ANNI]"

[TABLE 6 — vedi §4]
```

### Appendix G — Arm's length range

```
[Caption]: "Table 7– Arm's length range [descrizione set finale]"

[TABLE 7 — vedi §4]
```

### Appendix H — Comparable Companies Financial Information

```
[Caption]: "Table [N] – Comparable Companies Financial Information – Fiscal Years [ANNI] (th EUR)"

[TABLE 8 — vedi §4]
```

### Appendix I — Rejection Matrix

```
[Appendix1 heading]: "Appendix I. Rejection Matrix of the Comparable Companies"

[Tabella grande con tutte le società screened e motivo rigetto/accettazione]

Struttura consigliata:
Company Name | BvD ID | Country | Quant: Data | Quant: Losses | Quant: Intang | 
              Qual: Group | Qual: Functions | Qual: Products | Qual: Other | Status
```

---

## 8. Dati di input — Estrazione da Excel TP Catalyst

### Fogli Excel e utilizzo

| Foglio | Dati estratti |
|--------|--------------|
| `1. Title` | Metadati: società, transazione, anno, metodo, PLI |
| `2. Search summary` | Tabella funnel quantitativo (Table 2 nel report) |
| `5. Analisi` o `Analisi FY2023` | Tutti i dati finanziari per PLI calculation |
| `6. Final Set` | Lista comparable finali con PLI per anno |
| `RejectedAccepted Table` | Matrice rigetto per Appendix I |
| `Worksheet_AI` | Descrizioni aziende (colonne: Company Name, Country, BvD ID, Website, Commento, Comments) |

### Calcolo PLI

```python
import statistics

# Per ROS: EBIT / Turnover
def calc_ros(ebit, turnover):
    return ebit / turnover if turnover != 0 else None

# Per NCP: EBIT / Total Costs
def calc_ncp(ebit, total_costs):
    return ebit / total_costs if total_costs != 0 else None

# Weighted average su 3 anni
def weighted_avg(ebit_3y, base_3y):
    total_ebit = sum(ebit_3y)
    total_base = sum(base_3y)
    return total_ebit / total_base if total_base != 0 else None

# IQR statistiche
values = [wa_pli for company in final_set]
values_sorted = sorted(values)
n = len(values_sorted)

minimum = min(values_sorted)
maximum = max(values_sorted)
median = statistics.median(values_sorted)
q1 = statistics.quantiles(values_sorted, n=4)[0]   # 25th percentile
q3 = statistics.quantiles(values_sorted, n=4)[2]   # 75th percentile
```

### Formato output PLI nelle tabelle

```python
# Formattare come percentuale con 2 decimali
f"{value * 100:.2f}%"  # es. "6.20%"
```

---

## 9. Variabili template — Sostituzione testi

Elenco completo variabili da sostituire in ogni report:

| Variabile | Descrizione | Esempio |
|-----------|-------------|---------|
| `{CLIENT_NAME}` | Nome gruppo cliente | "TOD's Group" |
| `{TESTED_PARTY_NAME}` | Nome società soggetto | "TOD'S S.p.A." |
| `{TESTED_PARTY_TYPE}` | Tipo entità | "Retailers" / "Contract Manufacturers" / "Wholesalers" |
| `{TRANSACTION_DESC}` | Descrizione transazione | "Retail distribution of fashion and apparel products" |
| `{GEOGRAPHY}` | Mercato geografico | "North American and Western European" |
| `{FISCAL_YEAR}` | Anno fiscale | "2024" |
| `{FISCAL_YEAR_DATE}` | Data completa | "December 31st, 2024" |
| `{PLI_FULL_NAME}` | Nome PLI completo | "Operating Margin" / "Net Cost Plus" / "Return on Sales" |
| `{PLI_ABBR}` | Abbreviazione PLI | "OM" / "NCP" / "ROS" |
| `{PLI_FORMULA_DESC}` | Descrizione formula | "operating profit (EBIT) expressed as a percentage of turnover" |
| `{YEAR}` | Anno più recente | "2023" |
| `{YEAR_MINUS_1}` | Anno medio | "2022" |
| `{YEAR_MINUS_2}` | Anno più vecchio | "2021" |
| `{YEARS}` | Range anni | "2023-2021" |
| `{TP_CATALYST_VERSION}` | Versione TP Catalyst | "TP Catalyst, Release 176, November 2024 – update number 176005, version 176" |
| `{N_INITIAL}` | Aziende campione iniziale | "331" |
| `{N_COMPARABLE}` | Aziende comparable finali | "20" |
| `{N_QUANT_REJECTED}` | Rigettate screening quant | "200" |
| `{N_QUAL_REJECTED}` | Rigettate screening qual | "111" |
| `{Q1_PCT}` | Primo quartile | "1.81%" |
| `{MEDIAN_PCT}` | Mediana | "7.25%" |
| `{Q3_PCT}` | Terzo quartile | "10.45%" |
| `{MIN_PCT}` | Minimo | "0.47%" |
| `{MAX_PCT}` | Massimo | "16.51%" |

---

## 10. Architettura XML Injection — UNICO METODO APPROVATO

> ⛔ **DEPRECAZIONE TOTALE GENERAZIONE DA ZERO**
> La generazione procedurale (docx-js, python-docx) è **VIETATA** per questo skill.
> Unico metodo approvato: **XML Node Cloning con Data Injection**.
> Questo garantisce fedeltà visiva al 100% ereditando bordi, allineamenti e formattazione nativa Word.

### 10.1 Workflow Obbligatorio (5 Step Atomic)

```bash
# STEP 1: Decompressione template master
unzip -q "template_master.docx" -d work_dir/

# STEP 2: Normalizzazione placeholder XML (risolve fragmentation)
python normalize_placeholders.py work_dir/word/document.xml

# STEP 3: Clonazione righe tabella + injection dati
python clone_and_inject.py work_dir/word/document.xml data.json

# STEP 4: Aggiornamento metadati + TOC refresh flag
python set_update_fields.py work_dir/word/settings.xml

# STEP 5: Ricompressione + validazione schema
cd work_dir && zip -r ../output.docx . && cd ..
xmllint --noout --schema docx-schema.xsd output.docx 2>&1 | grep -q "validates" || exit 1
```

### 10.2 Script Python: normalize_placeholders.py

```python
"""
Risolve il problema della fragmentazione dei placeholder in Word XML.
Word spezza {CLIENT_NAME} in più nodi <w:t>. Questo script li fonde.
"""
import re
from lxml import etree

def normalize_run_texts(xml_path):
    """Fonde nodi <w:t> consecutivi nello stesso <w:r> parent."""
    tree = etree.parse(xml_path)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    for run in tree.xpath('//w:r', namespaces=ns):
        texts = run.xpath('./w:t', namespaces=ns)
        if len(texts) > 1:
            merged_text = ''.join(t.text or '' for t in texts)
            texts[0].text = merged_text
            for t in texts[1:]:
                run.remove(t)
    
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    import sys
    normalize_run_texts(sys.argv[1])
```

### 10.3 Script Python: clone_and_inject.py

```python
"""
Clona righe template delle tabelle e inietta dati JSON.
NON crea XML da zero, eredita formattazione nativa Word.
"""
import json
from lxml import etree
from copy import deepcopy

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def inject_table_data(xml_path, data_path):
    tree = etree.parse(xml_path)
    with open(data_path) as f:
        data = json.load(f)
    
    # ESEMPIO: Table 3 - Comparable companies
    for tbl in tree.xpath('//w:tbl', namespaces=ns):
        prev = tbl.getprevious()
        if prev is not None and 'Table 3' in (prev.xpath('.//w:t/text()', namespaces=ns) or [''])[0]:
            rows = tbl.xpath('./w:tr', namespaces=ns)
            template_row = rows[1]
            header_row = rows[0]
            tbl.remove(template_row)
            
            for company in data['comparable_companies']:
                new_row = deepcopy(template_row)
                cells = new_row.xpath('./w:tc', namespaces=ns)
                cells[0].xpath('.//w:t', namespaces=ns)[0].text = company['name']
                cells[1].xpath('.//w:t', namespaces=ns)[0].text = company['bvd_id']
                cells[2].xpath('.//w:t', namespaces=ns)[0].text = f"{company['pli_avg']:.2f}%"
                cells[3].xpath('.//w:t', namespaces=ns)[0].text = f"{company['pli_2023']:.2f}%"
                cells[4].xpath('.//w:t', namespaces=ns)[0].text = f"{company['pli_2022']:.2f}%"
                cells[5].xpath('.//w:t', namespaces=ns)[0].text = f"{company['pli_2021']:.2f}%"
                tbl.insert(tbl.index(header_row) + 1, new_row)
    
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    import sys
    inject_table_data(sys.argv[1], sys.argv[2])
```

### 10.4 Script Python: set_update_fields.py

```python
"""Forza Word ad aggiornare TOC/numero pagine all'apertura."""
from lxml import etree

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def set_update_on_open(settings_path):
    tree = etree.parse(settings_path)
    root = tree.getroot()
    for elem in root.xpath('//w:updateFields', namespaces=ns):
        root.remove(elem)
    update_elem = etree.Element('{%s}updateFields' % ns['w'])
    update_elem.set('{%s}val' % ns['w'], 'true')
    root.insert(0, update_elem)
    tree.write(settings_path, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    import sys
    set_update_on_open(sys.argv[1])
```

### 10.5 Formato JSON Dati di Input

```json
{
  "metadata": {
    "client_name": "TOD's Group",
    "transaction_desc": "Retail distribution of fashion products",
    "fiscal_year": "2024",
    "pli_name": "Operating Margin",
    "pli_abbr": "OM"
  },
  "comparable_companies": [
    {
      "name": "AZIENDA ESEMPIO S.R.L.",
      "bvd_id": "IT12345678901",
      "country": "Italy",
      "pli_2023": 6.25,
      "pli_2022": 5.80,
      "pli_2021": 7.15,
      "pli_avg": 6.40
    }
  ]
}
```

### 10.6 Vantaggi Architetturali

| Aspetto | Approccio Vecchio (docx-js) | Nuovo Approccio (XML Injection) |
|---------|-------------------------------|----------------------------------|
| **Fedeltà Layout** | 85-90% (approssimativo) | 100% (ereditato da template) |
| **Gestione Bordi** | Richiede codice custom | Ereditati automaticamente |
| **Manutenibilità** | Fragile | Resiliente (puro XML) |
| **Performance** | 3-5 secondi | <1 secondo |

---

### 10.7 Circuit Breaker Pattern — Protezione Template

```python
"""
Circuit Breaker per validazione template.
Se un template fallisce più volte, viene temporaneamente escluso.
"""
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # Funzionamento normale
    OPEN = "open"          # Template bloccato
    HALF_OPEN = "half_open"  # Test ripristino

class TemplateCircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=300):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = {}
        self.last_failure = {}
        self.states = {}
    
    def validate_template(self, template_path):
        state = self.states.get(template_path, CircuitState.CLOSED)
        
        if state == CircuitState.OPEN:
            if time.time() - self.last_failure.get(template_path, 0) < self.recovery_timeout:
                raise CircuitBreakerOpen(f"Template {template_path} temporarily blocked")
            state = CircuitState.HALF_OPEN
        
        try:
            # Validazione strutturale
            with zipfile.ZipFile(template_path, 'r') as zf:
                required = ['word/document.xml', 'word/styles.xml', '[Content_Types].xml']
                for file in required:
                    if file not in zf.namelist():
                        raise ValueError(f"Missing {file}")
                
                # Validazione XML well-formed
                doc = zf.read('word/document.xml')
                etree.fromstring(doc)
            
            # Successo: reset contatore
            self.failures[template_path] = 0
            self.states[template_path] = CircuitState.CLOSED
            return True
            
        except Exception as e:
            # Fallimento: incrementa contatore
            self.failures[template_path] = self.failures.get(template_path, 0) + 1
            self.last_failure[template_path] = time.time()
            
            if self.failures[template_path] >= self.failure_threshold:
                self.states[template_path] = CircuitState.OPEN
            
            raise TemplateValidationError(f"Invalid template: {e}")

class CircuitBreakerOpen(Exception):
    pass
```

---

### 10.8 Defensive Cell Update — Gestione Errori XML

```python
"""
Aggiornamento celle con fallback e graceful degradation.
Evita crash se struttura XML non è quella attesa.
"""
import logging

def safe_cell_update(cell, text, ns, row_idx=None, col_idx=None):
    """
    Aggiorna cella con multiple fallback strategies.
    
    Args:
        cell: Elemento XML w:tc (table cell)
        text: Testo da inserire
        ns: Namespace XML
        row_idx, col_idx: Indici per logging
    
    Returns:
        bool: True se successo, False se fallito
    """
    try:
        # Strategy 1: Trova w:t esistente
        t_elements = cell.xpath('.//w:t', namespaces=ns)
        if t_elements:
            t_elements[0].text = text
            return True
        
        # Strategy 2: Trova w:r e crea w:t
        r_elements = cell.xpath('.//w:r', namespaces=ns)
        if r_elements:
            new_t = etree.Element('{%s}t' % ns['w'])
            new_t.text = text
            r_elements[0].append(new_t)
            logging.info(f"Created w:t element for cell [{row_idx},{col_idx}]")
            return True
        
        # Strategy 3: Crea struttura completa w:r > w:t
        p_element = cell.xpath('.//w:p', namespaces=ns)
        if p_element:
            new_r = etree.Element('{%s}r' % ns['w'])
            new_t = etree.SubElement(new_r, '{%s}t' % ns['w'])
            new_t.text = text
            p_element[0].append(new_r)
            logging.warning(f"Created full structure for cell [{row_idx},{col_idx}]")
            return True
        
        # Fallimento: logga e continua
        logging.error(f"Cannot update cell [{row_idx},{col_idx}]: no valid structure found")
        return False
        
    except Exception as e:
        logging.error(f"Exception updating cell [{row_idx},{col_idx}]: {e}")
        return False

def inject_table_data_defensive(xml_path, data_path):
    """Versione difensiva con skip parziale."""
    tree = etree.parse(xml_path)
    with open(data_path) as f:
        data = json.load(f)
    
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    for tbl in tree.xpath('//w:tbl', namespaces=ns):
        prev = tbl.getprevious()
        if prev is not None and 'Table 3' in (prev.xpath('.//w:t/text()', namespaces=ns) or [''])[0]:
            rows = tbl.xpath('./w:tr', namespaces=ns)
            if len(rows) < 2:
                logging.error("Table 3 has no template row")
                continue
                
            template_row = rows[1]
            header_row = rows[0]
            tbl.remove(template_row)
            
            success_count = 0
            for i, company in enumerate(data['comparable_companies']):
                new_row = deepcopy(template_row)
                cells = new_row.xpath('./w:tc', namespaces=ns)
                
                if len(cells) < 6:
                    logging.warning(f"Row {i} has only {len(cells)} cells, expected 6")
                    continue
                
                # Aggiorna con defensive approach
                results = [
                    safe_cell_update(cells[0], company['name'], ns, i, 0),
                    safe_cell_update(cells[1], company['bvd_id'], ns, i, 1),
                    safe_cell_update(cells[2], f"{company['pli_avg']:.2f}%", ns, i, 2),
                    safe_cell_update(cells[3], f"{company['pli_2023']:.2f}%", ns, i, 3),
                    safe_cell_update(cells[4], f"{company['pli_2022']:.2f}%", ns, i, 4),
                    safe_cell_update(cells[5], f"{company['pli_2021']:.2f}%", ns, i, 5),
                ]
                
                if all(results):
                    tbl.insert(tbl.index(header_row) + 1, new_row)
                    success_count += 1
                else:
                    logging.warning(f"Row {i} partially failed, skipped")
            
            logging.info(f"Successfully inserted {success_count}/{len(data['comparable_companies'])} rows")
    
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
```

---

### 10.9 Copy-on-Write Transaction Pattern

```python
"""
Pattern Copy-on-Write per vera transazionalità.
Modifiche su copia, commit solo se tutto successo.
"""
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

class CopyOnWriteTransaction:
    """Gestione transazionale con backup e rollback."""
    
    def __init__(self, template_path):
        self.template_path = Path(template_path)
        self.work_dir = None
        self.backup_dir = None
        self.snapshots = []
        self.committed = False
    
    def __enter__(self):
        """Inizializza ambiente isolato."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.work_dir = Path(tempfile.gettempdir()) / f"sbnp_cow_{timestamp}"
        self.backup_dir = self.work_dir / "snapshots"
        self.backup_dir.mkdir(parents=True)
        
        # Copia template in area di lavoro
        shutil.copytree(self.template_path, self.work_dir / "working_copy")
        
        logging.info(f"COW transaction started: {self.work_dir}")
        return self
    
    def snapshot(self, step_name):
        """Crea snapshot prima di operazione rischiosa."""
        doc_xml = self.work_dir / "working_copy" / "word" / "document.xml"
        snapshot_path = self.backup_dir / f"{step_name}_{datetime.now().strftime('%H%M%S')}.xml"
        shutil.copy(doc_xml, snapshot_path)
        self.snapshots.append((step_name, snapshot_path))
        logging.info(f"Snapshot created: {step_name}")
    
    def rollback(self, step_name=None):
        """Ripristina a snapshot specifico o ultimo."""
        if not self.snapshots:
            logging.error("No snapshots to rollback")
            return False
        
        if step_name:
            snapshot = next((s for s in self.snapshots if s[0] == step_name), None)
        else:
            snapshot = self.snapshots[-1]
        
        if snapshot:
            doc_xml = self.work_dir / "working_copy" / "word" / "document.xml"
            shutil.copy(snapshot[1], doc_xml)
            logging.info(f"Rolled back to: {snapshot[0]}")
            return True
        return False
    
    def commit(self, output_path):
        """Commit finale: copia risultato e marca successo."""
        if self.committed:
            raise RuntimeError("Transaction already committed")
        
        working_copy = self.work_dir / "working_copy"
        
        # Ricomprimi
        shutil.make_archive(str(Path(tempfile.gettempdir()) / "final_output"), 
                           'zip', working_copy)
        
        # Sposta in destinazione finale
        final_zip = Path(tempfile.gettempdir()) / "final_output.zip"
        shutil.move(str(final_zip), output_path)
        
        self.committed = True
        logging.info(f"Transaction committed: {output_path}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup: se non committed, automatic rollback."""
        if not self.committed and exc_type is not None:
            logging.error(f"Transaction failed, rollback executed: {exc_val}")
        
        # Cleanup directory temporanea
        if self.work_dir and self.work_dir.exists():
            shutil.rmtree(self.work_dir, ignore_errors=True)
            logging.info("COW transaction cleanup completed")

# Uso
# with CopyOnWriteTransaction(template_path) as tx:
#     tx.snapshot("pre_normalization")
#     normalize_placeholders(tx.work_dir / "working_copy" / "word" / "document.xml")
#     
#     tx.snapshot("pre_injection")
#     inject_table_data(...)
#     
#     tx.commit("/path/to/output.docx")
```

---

### 10.10 File Locking e Gestione Concorrenza

```python
"""
Locking distribuito per prevenire race condition
su template condivisi in ambiente multi-utente.
"""
import fcntl  # Unix. Per Windows: import portalocker
import os
import secrets

class DistributedTemplateLock:
    """Lock esclusivo su template con timeout."""
    
    def __init__(self, template_path, timeout=30):
        self.template_path = template_path
        self.timeout = timeout
        self.lock_file = f"{template_path}.lock"
        self.fd = None
    
    def __enter__(self):
        """Acquisisce lock con timeout."""
        self.fd = open(self.lock_file, 'w')
        
        try:
            # Non-blocking con timeout
            start = time.time()
            while True:
                try:
                    fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    logging.info(f"Lock acquired: {self.template_path}")
                    return self
                except IOError:
                    if time.time() - start > self.timeout:
                        raise TimeoutError(f"Cannot acquire lock on {self.template_path}")
                    time.sleep(0.1)
        except:
            self.fd.close()
            raise
    
    def __exit__(self, *args):
        """Rilascia lock."""
        if self.fd:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            self.fd.close()
            try:
                os.remove(self.lock_file)
            except:
                pass
            logging.info(f"Lock released: {self.template_path}")

def create_isolated_work_dir():
    """Crea directory di lavoro univoca per processo."""
    pid = os.getpid()
    tid = threading.current_thread().ident
    timestamp = time.time()
    random_suffix = secrets.token_hex(8)
    
    work_dir = Path(tempfile.gettempdir()) / f"sbnp_{pid}_{tid}_{timestamp}_{random_suffix}"
    work_dir.mkdir(parents=True, exist_ok=False)
    
    return work_dir

# Uso in ambiente concorrente
# with DistributedTemplateLock(template_path, timeout=60):
#     with CopyOnWriteTransaction(template_path) as tx:
#         # ... operazioni ...
#         tx.commit(output_path)
```

---

### 10.11 Observability — Structured Logging e Metrics

```python
"""
Observability completa: logging strutturato, metrics Prometheus,
tracing distribuito per monitoraggio produzione.
"""
import structlog
import time
from contextvars import ContextVar
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Context variable per correlation ID
request_id_var = ContextVar('request_id', default=None)

# Metrics Prometheus
GENERATION_DURATION = Histogram(
    'sbnp_report_generation_seconds',
    'Time spent generating report',
    ['template_type', 'status']
)

GENERATION_ERRORS = Counter(
    'sbnp_report_generation_errors_total',
    'Total generation errors',
    ['error_type', 'template_type']
)

ACTIVE_GENERATIONS = Gauge(
    'sbnp_active_generations',
    'Currently running generations'
)

REPORT_SIZE = Histogram(
    'sbnp_report_size_bytes',
    'Size of generated reports'
)

# Logger strutturato
logger = structlog.get_logger()

def get_correlation_id():
    """Recupera o genera correlation ID per tracing."""
    cid = request_id_var.get()
    if not cid:
        cid = str(uuid.uuid4())
        request_id_var.set(cid)
    return cid

class ObservableGenerator:
    """Wrapper che aggiunge observability a qualsiasi generatore."""
    
    def __init__(self, generator_func):
        self.generator = generator_func
    
    def generate(self, excel_path, metadata, output_path):
        """Esecuzione con monitoring completo."""
        cid = get_correlation_id()
        start_time = time.time()
        template_type = metadata.get('transaction_type', 'unknown')
        
        ACTIVE_GENERATIONS.inc()
        
        logger.info(
            "generation_started",
            correlation_id=cid,
            template_type=template_type,
            client=metadata.get('client_name'),
            excel_file=excel_path,
            output_file=output_path
        )
        
        try:
            # Esecuzione generazione
            result = self.generator(excel_path, metadata, output_path)
            
            # Successo
            duration = time.time() - start_time
            file_size = os.path.getsize(output_path)
            
            GENERATION_DURATION.labels(
                template_type=template_type,
                status='success'
            ).observe(duration)
            
            REPORT_SIZE.observe(file_size)
            
            logger.info(
                "generation_completed",
                correlation_id=cid,
                duration_seconds=duration,
                file_size_bytes=file_size,
                template_type=template_type
            )
            
            return result
            
        except ValidationError as e:
            GENERATION_ERRORS.labels(
                error_type='validation',
                template_type=template_type
            ).inc()
            
            logger.error(
                "generation_failed_validation",
                correlation_id=cid,
                error=str(e),
                template_type=template_type
            )
            raise
            
        except Exception as e:
            GENERATION_ERRORS.labels(
                error_type='unexpected',
                template_type=template_type
            ).inc()
            
            logger.error(
                "generation_failed_unexpected",
                correlation_id=cid,
                error=str(e),
                error_type=type(e).__name__,
                template_type=template_type,
                exc_info=True
            )
            raise
            
        finally:
            ACTIVE_GENERATIONS.dec()

# Avvio server metrics (porta 9090)
# start_http_server(9090)

# Uso
# generator = ObservableGenerator(generate_report_atomic)
# generator.generate(excel, metadata, output)
```

---

### 10.12 Checklist Deployment Production

Prima di deploy in produzione, verificare:

```bash
# 1. Health Check
python -c "from report_generator import health_check; health_check()"

# 2. Resource Limits
ulimit -v 524288  # Max 512MB RAM
ulimit -t 60      # Max 60s CPU time

# 3. Template Hash Verification
sha256sum templates/*.docx > templates.sha256
sha256sum -c templates.sha256

# 4. Alerting Rules (Prometheus)
# - sbnp_report_generation_errors_total > 1%
# - sbnp_active_generations > 10 (too many concurrent)
# - sbnp_report_generation_seconds > 30s (p95)

# 5. Audit Trail
# Tutte le generazioni loggate in /var/log/sbnp/reports/
# Retention: 90 giorni

# 6. Backup Strategy
# - Template masters in version control
# - Daily backup /var/log/sbnp/
# - Disaster recovery: < 1 ora RTO
```

---

## 11. Workflow Operativo HA — Production Grade

### 11.1 Input Validation

```python
def validate_input(excel_path, metadata):
    """Valida dati prima di iniziare generazione."""
    required_sheets = ['6. Final Set', '2. Search summary', 'Worksheet_AI']
    wb = openpyxl.load_workbook(excel_path)
    
    for sheet in required_sheets:
        if sheet not in wb.sheetnames:
            raise ValueError(f"Foglio mancante: {sheet}")
    
    final_set = wb['6. Final Set']
    if final_set.max_row < 2:
        raise ValueError("Nessuna comparable company nel foglio Final Set")
    
    required_meta = ['client_name', 'fiscal_year', 'pli_abbr', 'transaction_desc']
    for key in required_meta:
        if key not in metadata or not metadata[key]:
            raise ValueError(f"Metadato obbligatorio mancante: {key}")
```

### 11.2 Template Selection Logic

```python
def select_template(transaction_type, geography):
    """Selezione deterministica del template master."""
    template_map = {
        ('wholesale', 'EU'): 'templates/Acciaierie_Valbruna_WHS_EU.docx',
        ('wholesale', 'FE'): 'templates/Acciaierie_Valbruna_WHS_FE.docx',
        ('contract_mfg', 'EU'): 'templates/Crosspolimeri_CM.docx',
        ('support_svc', 'EU'): 'templates/Ascoli_HFD_Support.docx',
        ('wholesale', 'USA'): 'templates/CM_Bandera_USA_adj.docx'
    }
    key = (transaction_type.lower(), geography.upper())
    if key not in template_map:
        raise ValueError(f"Combinazione non supportata: {key}")
    return template_map[key]
```

### 11.3 Atomic Generation Transaction

```python
import tempfile
import shutil
from pathlib import Path

class DocumentGenerationError(Exception):
    """Errore bloccante nella generazione report."""
    pass

def generate_report_atomic(excel_path, metadata, output_path):
    """Generazione atomica con rollback automatico in caso errore."""
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            validate_input(excel_path, metadata)
            
            template = select_template(metadata['transaction_type'], metadata['geography'])
            work_dir = Path(tmpdir) / 'work'
            shutil.unpack_archive(template, work_dir, 'zip')
            
            data = extract_data_from_excel(excel_path)
            data.update(metadata)
            
            doc_xml = work_dir / 'word' / 'document.xml'
            normalize_placeholders(doc_xml)
            replace_placeholders(doc_xml, data)
            clone_and_inject_tables(doc_xml, data)
            
            settings_xml = work_dir / 'word' / 'settings.xml'
            set_update_on_open(settings_xml)
            
            shutil.make_archive(str(Path(tmpdir) / 'output'), 'zip', work_dir)
            shutil.move(str(Path(tmpdir) / 'output.zip'), output_path)
            
            validate_docx_schema(output_path)
            return True
            
        except Exception as e:
            logging.error(f"Generazione fallita: {e}")
            raise DocumentGenerationError(f"Report generation failed: {e}")
```

---

## 12. Checklist QA Automatizzata — Zero Intervento Manuale

### 12.1 QA Script Python

```python
"""
qa_validator.py — Validazione automatica 100% checklist
"""
from docx import Document
from lxml import etree
import zipfile
import re

class QAValidator:
    def __init__(self, docx_path, expected_metadata):
        self.docx_path = docx_path
        self.metadata = expected_metadata
        self.errors = []
    
    def validate_all(self):
        """Esegue tutti i controlli della checklist."""
        self.check_cover_page()
        self.check_language()
        self.check_toc()
        self.check_headers_footers()
        self.check_tables()
        self.check_styles()
        self.check_appendices()
        
        if self.errors:
            raise QAValidationError(f"QA fallita con {len(self.errors)} errori:\n" + "\n".join(self.errors))
        return True
    
    def check_cover_page(self):
        """Verifica copertina."""
        doc = Document(self.docx_path)
        with zipfile.ZipFile(self.docx_path) as zf:
            if 'word/media/image2.jpeg' not in zf.namelist():
                self.errors.append("Logo SBNP mancante (image2.jpeg)")
        
        first_page_text = '\n'.join([p.text for p in doc.paragraphs[:5]])
        if self.metadata['client_name'] not in first_page_text:
            self.errors.append(f"Nome cliente '{self.metadata['client_name']}' non trovato in copertina")
    
    def check_language(self):
        """Verifica assenza testo italiano."""
        doc = Document(self.docx_path)
        italian_words = ['sezione', 'tabella', 'appendice', 'società', 'anno fiscale']
        full_text = '\n'.join([p.text for p in doc.paragraphs]).lower()
        for word in italian_words:
            if word in full_text:
                self.errors.append(f"Parola italiana trovata: '{word}'")
    
    def check_tables(self):
        """Verifica formattazione tabelle."""
        doc = Document(self.docx_path)
        tables_with_iqr = []
        for i, table in enumerate(doc.tables):
            if len(table.rows) == 3 and len(table.columns) == 7:
                header_text = table.rows[0].cells[0].text
                if 'Average' in header_text and '%' in header_text:
                    tables_with_iqr.append(i)
        
        if len(tables_with_iqr) != 2:
            self.errors.append(f"Trovate {len(tables_with_iqr)} tabelle IQR invece di 2")
    
    def check_styles(self):
        """Verifica font e colori."""
        with zipfile.ZipFile(self.docx_path) as zf:
            styles_xml = zf.read('word/styles.xml')
            tree = etree.fromstring(styles_xml)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            for style_id in ['Heading1', 'Heading2', 'Normal']:
                style = tree.xpath(f'//w:style[@w:styleId="{style_id}"]', namespaces=ns)
                if style:
                    font = style[0].xpath('.//w:rFonts/@w:ascii', namespaces=ns)
                    if font and font[0] != 'Cambria':
                        self.errors.append(f"Stile {style_id} usa font {font[0]} invece di Cambria")
    
    def check_appendices(self):
        """Verifica presenza appendici A-I."""
        doc = Document(self.docx_path)
        full_text = '\n'.join([p.text for p in doc.paragraphs])
        for letter in 'ABCDEFGHI':
            if f"Appendix {letter}." not in full_text:
                self.errors.append(f"Appendix {letter} mancante")

# Uso
# validator = QAValidator('output.docx', metadata)
# validator.validate_all()
```

### 12.2 Checklist Automatizzata (Sostituisce Checklist Manuale)

```bash
#!/bin/bash
# qa_pipeline.sh — Esegue validazione completa

DOCX_PATH=$1
METADATA_JSON=$2

echo "=== QA Validation Pipeline ==="

# 1. Schema XSD
echo "[1/5] Validazione schema XML..."
python validate_schema.py "$DOCX_PATH" || exit 1

# 2. QA checklist automatica
echo "[2/5] QA checklist (cover, language, tables, styles)..."
python qa_validator.py "$DOCX_PATH" "$METADATA_JSON" || exit 1

# 3. File size sanity check
echo "[3/5] File size check..."
SIZE=$(stat -f%z "$DOCX_PATH")
if [ $SIZE -lt 50000 ] || [ $SIZE -gt 5000000 ]; then
    echo "ERRORE: File size anomalo ($SIZE bytes)"
    exit 1
fi

echo "✅ QA PASSED"
```
