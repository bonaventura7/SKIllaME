---
name: tp-benchmarking-report-photocopier-v3
version: 3.0-incident-learned-ha
language: it
risk: high
output: DOCX professionale in inglese + QA report + audit pack
mission: >
  Fotocopiatrice transazionale DOCX per report di benchmarking Transfer Pricing in stile SBNP.
  La skill non genera report creativi: clona template DOCX approvati, modifica XML interni,
  inietta solo dati validati, preserva layout/stili/tabelle/header/footer/appendici e blocca
  l'output se package, arithmetic, semantic, contamination, table, style e council gates non passano.
---

# TP Benchmarking Report Photocopier v3 — Incident-Learned HA

## 0. Golden Rule

**Never optimize for beauty before fidelity.**

Il report non è valido perché “sembra bello”. È valido solo se dimostra di essere un clone controllato di un template SBNP gold standard, con dati iniettati, layout ereditato e Quality Gate superato.

La skill deve agire come:

```text
CASE_LOCK → TEMPLATE_ROUTER → COPY-ON-WRITE DOCX → XML NODE CLONING → QA GATES → COUNCIL → DELIVERY/BLOCK
```

## 1. Modalità obbligatoria

### 1.1 Prima di tutto: Brainstorming Gate

Prima di modificare qualunque file:

1. esplora contesto, file allegati e modelli;
2. identifica intento e vincoli;
3. seleziona il caso d'uso;
4. crea una matrice dati bloccante;
5. propone approccio solo dopo aver validato le assunzioni.

Per report TP questa fase non deve diventare conversazione infinita: produce immediatamente `CASE_LOCK.json`.

### 1.2 Error Detective Gate

Ogni difetto è trattato come incident:

```text
Symptom:
Impact:
Evidence:
Root Cause:
Minimal Fix:
Verification:
Prevention:
```

Se un errore è CRITICAL/HIGH, non si consegna il DOCX finale. Si consegna solo QA Failure Report.

### 1.3 LLM Council Gate

Prima della consegna, la generazione deve passare il Council:

- Contrarian: cerca contaminazioni, template wrong-family, PLI misto, old years, quasi-final.
- First Principles: verifica scopo TP, PLI, benchmark, comparability logic, limitations.
- Expansionist: identifica automazioni, regression suite, audit trail, riuso.
- Outsider: verifica leggibilità e coerenza per reviewer esterno.
- Executor: verifica che il file sia consegnabile, rollbackabile, auditabile.

Se un advisor segnala CRITICAL non risolto: `BLOCK`.

## 2. CASE_LOCK.json — gate zero

Prima di aprire o modificare il DOCX finale, creare il lock del caso:

```json
{
  "client": "Quickfairs Group",
  "transaction": "Provision of event organisation services in Europe",
  "tested_party_type": "service provider",
  "geography": "Europe",
  "pli": "NCP",
  "pli_formula": "EBIT / Total Costs",
  "period": "2024-2022",
  "fiscal_year": "FY2025",
  "tp_catalyst_release": "194 - May 2026",
  "tp_catalyst_update_number": "194025",
  "tp_catalyst_version": "194",
  "initial_population": 656,
  "quantitative_rejected": 191,
  "after_quantitative": 465,
  "qualitative_rejected": 458,
  "final_sample": 7,
  "observation": 7,
  "min_pct": 0.0097,
  "q1_pct": 0.0676,
  "median_pct": 0.1694,
  "q3_pct": 0.1975,
  "max_pct": 0.3520,
  "template_mode": "clone_existing_docx",
  "appendix_profile": "FULL_A_I",
  "release_state": "WORKING_DRAFT"
}
```

### 2.1 CASE_LOCK hard rules

- Se manca un campo obbligatorio: `BLOCK`.
- Se il documento finale contraddice CASE_LOCK: `BLOCK`.
- Se il documento contiene valori old-model in blacklist: `BLOCK`.
- Se arithmetic non riconcilia: `BLOCK`.

## 3. Template Router deterministico

La combinazione `transaction_type + geography + PLI + appendix_profile` deve selezionare esattamente un template.

| Caso | PLI | Template profile | Appendici | Note |
|---|---:|---|---|---|
| marketing/support/services | NCP | SVC/MKT_SUPPORT_EU_NCP | FULL_A_I | Usare solo se attività e search narrative sono coerenti |
| event organisation services | NCP | EVENT_ORG_EU_NCP | FULL_A_I | Search NACE 8230 / conventions and trade shows |
| contract manufacturing | NCP | CM_EU_NCP | STANDARD_A_H | Non mischiare con service providers |
| wholesale distribution | ROS | WHS_EU_ROS | COMPACT_A_F | Non usare per servizi NCP |

### 3.1 Router hard fail

```text
0 template selected → BLOCK
>1 template selected → BLOCK
wrong PLI for template → BLOCK
appendix profile mismatch → BLOCK
```

## 4. Template Fingerprint

Per ogni template approvato salvare `template_fingerprint.json`:

```json
{
  "template_id": "505_marketing_support_full_ai",
  "hash": "sha256:...",
  "appendix_profile": "FULL_A_I",
  "section_sequence": [
    "Executive Summary",
    "The Search Process",
    "The TP Catalyst Search",
    "Further Selection Process",
    "Final Sample",
    "Summary of Results",
    "Limitations"
  ],
  "appendices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
  "critical_tables": {
    "table_1_iqr": "3x7 with merged title row",
    "table_2_search_process": "native search process table",
    "further_selection": "complex merged native table",
    "table_3_final_sample": "company/BvD/PLI years/average",
    "table_7_arm_length": "stat rows x years + average",
    "financial_info": "company + total costs + EBIT"
  },
  "visual_tokens": {
    "font": "Cambria",
    "caption_color": ["#800000", "#A32020"],
    "table_header_fill": ["#800000", "#6B1414", "#A32020"],
    "table_header_text": "#FFFFFF"
  }
}
```

Se output fingerprint drift > soglia: `BLOCK` o `REVIEW_CANDIDATE`, mai `FINAL`.

## 5. XML Node Cloning Workflow

### 5.1 Workflow approvato

```text
1. validate input package
2. build CASE_LOCK.json
3. select template via router
4. copy template into isolated workdir
5. unzip DOCX
6. compute template fingerprint
7. normalize split placeholders only where needed
8. replace scalar nodes
9. clone native rows/nodes for repeated tables
10. preserve w:tcPr, w:tblPr, w:gridSpan, w:vMerge, w:shd, w:borders
11. inject data
12. set updateFields on open
13. rezip DOCX
14. package validation
15. arithmetic validation
16. semantic consistency validation
17. full package contamination scan
18. visual/table fingerprint validation
19. council review
20. release state decision
```

### 5.2 Workflow vietato

- Generare da blank document.
- Ricreare manualmente tabelle complesse.
- “Pulire” una tabella nativa trasformandola in tabella semplice.
- Usare `python-docx` come editor principale per merged tables.
- Consegnare file intermedi chiamandoli “final”.
- Scansionare solo `word/document.xml`.

## 6. Regression Suite — errori Quickfairs convertiti in test

Ogni errore visto diventa test permanente.

| Test ID | Classe | Pattern da bloccare | Severity |
|---|---|---|---:|
| REG-001 | old transaction | marketing and support sales services | CRITICAL |
| REG-002 | old sample count | 31 / 43 / 41 comparable companies | CRITICAL |
| REG-003 | old search total | 1,264 / 1,255 / 577 | CRITICAL |
| REG-004 | wrong NACE narrative | Computer programming / Advertising agencies / Public relations | CRITICAL |
| REG-005 | old years | 2023-2021 / 2021-2019 / 2020-2022 | CRITICAL |
| REG-006 | wrong thresholds | min=2,000, max=100,000 when CASE_LOCK says 20,000 | CRITICAL |
| REG-007 | hidden XML residue | forbidden tokens in footnotes/endnotes/comments/headers/footers | HIGH |
| REG-008 | table simplification | native Further Selection table replaced by simple 3-column table | HIGH |
| REG-009 | merged cell drift | gridSpan/vMerge count changed unexpectedly | HIGH |
| REG-010 | premature final | release_state=FINAL without all gates PASS | CRITICAL |

## 7. Full Package Contamination Scan

La scansione deve coprire almeno:

```text
word/document.xml
word/header*.xml
word/footer*.xml
word/footnotes.xml
word/endnotes.xml
word/comments.xml
word/settings.xml
word/_rels/*.rels
customXml/*.xml, se presenti
```

### 7.1 Forbidden old values generator

Ogni progetto genera la blacklist da:

- template source client;
- template source group;
- template source transaction;
- old PLI;
- old years;
- old NACE/NAICS/SIC;
- old sample counts;
- old thresholds;
- old geography;
- old TP Catalyst release.

Per Quickfairs vanno bloccati, tra gli altri:

```text
505 Games
Digital Bros
marketing and support sales services
brand management, marketing, press office
31 comparable
43 comparable
41 comparable
1,264
1,255
577
2023-2021
2021-2019
2020-2022
EU [14]
Advertising agencies
Computer programming
Number of employees between 1 and 100
min=2,000, max=100,000
```

## 8. Semantic Consistency Gate

Il checker confronta:

```text
CASE_LOCK
vs Search table
vs Search narrative
vs Appendix D
vs Further Selection table
vs Executive Summary
vs Final Sample
vs Appendix F/G/H/I
```

Esempi di blocco:

- Tabella: NACE 8230; narrativa: advertising agencies → `BLOCK`.
- CASE_LOCK final_sample=7; corpo: 31 companies → `BLOCK`.
- CASE_LOCK PLI=NCP; Appendix C parla di ROS → `BLOCK`.
- Search total 656; Further Selection parte da 1,264 → `BLOCK`.

## 9. Arithmetic Gate

```python
def validate_case_lock(data):
    assert data["initial_population"] - data["quantitative_rejected"] == data["after_quantitative"]
    assert data["after_quantitative"] - data["qualitative_rejected"] == data["final_sample"]
    assert data["observation"] == data["final_sample"]
    assert data["min_pct"] <= data["q1_pct"] <= data["median_pct"] <= data["q3_pct"] <= data["max_pct"]
```

Per Quickfairs:

```text
656 - 191 = 465
465 - 458 = 7
observation = 7
0.97% <= 6.76% <= 16.94% <= 19.75% <= 35.20%
```

## 10. Release State Machine

```text
WORKING_DRAFT
  ↓ package + arithmetic pass
REVIEW_CANDIDATE
  ↓ contamination + semantic + table fingerprint pass
STYLE_CANDIDATE
  ↓ visual/council pass
FINAL
```

### 10.1 Hard rule

Un file può chiamarsi `FINAL` solo se:

```text
package_errors = []
arithmetic_errors = []
semantic_errors = []
contamination_found = []
table_fingerprint_errors = []
style_errors = [] or accepted waiver
council_decision != BLOCK
```

## 11. QA JSON schema

Ogni generazione produce `QA.json`:

```json
{
  "generation_id": "uuid",
  "timestamp": "iso8601",
  "template_id": "",
  "template_hash": "sha256",
  "input_hash": "sha256",
  "output_hash": "sha256",
  "release_state": "FINAL",
  "case_lock": {},
  "package_errors": [],
  "arithmetic_errors": [],
  "semantic_errors": [],
  "contamination_found": [],
  "style_warnings": [],
  "table_fingerprint_errors": [],
  "council_decision": "APPROVE_WITH_WARNINGS",
  "qa_score": 99
}
```

## 12. HA / Resilience Controls

### 12.1 Copy-on-write

- Master template read-only.
- Working copy in isolated directory.
- No overwrite of previous passing output.

### 12.2 Rollback

If any gate fails:

```text
freeze candidate
preserve logs
write QA Failure Report
do not overwrite last good FINAL
```

### 12.3 Circuit breaker

If a template fails package/fingerprint validation repeatedly:

```text
mark template unhealthy
block future use
require template repair or reviewer waiver
```

### 12.4 Observability

Log minimally but completely:

```text
correlation_id
template_id
case_lock_hash
input_hash
output_hash
qa_score
release_state
critical_errors_count
warnings_count
```

No sensitive financial data in full logs.

## 13. Smart Workaround Policy

### Missing TP Catalyst screenshot

- Cosa facciamo ora: placeholder esplicito in Appendix D.
- Perché funziona: mantiene struttura completa.
- Limite: non submission-ready.
- Rischio residuo: reviewer può richiedere evidenza visiva.
- Evoluzione: inserire screenshot e rilanciare QA.

### Template close but not exact

- Cosa facciamo ora: `BLOCK` by default.
- Perché: la skill è fotocopiatrice, non generatore creativo.
- Eccezione: waiver scritto del reviewer.
- Rischio residuo: layout/appendix mismatch.
- Evoluzione: creare gold template dedicato.

### Merged table extraction noisy

- Cosa facciamo ora: validiamo XML fingerprint, non solo testo estratto.
- Perché: la vista testuale può duplicare celle merged.
- Limite: serve review visuale in Word.
- Evoluzione: renderer/diff visuale automatizzato.

## 14. Machine Learning / Quality Learning Layer

Non usare ML per scrivere il report. Usarlo come sentinella `PASS/WARN/BLOCK`.

### 14.1 Dataset unitario

Ogni versione prodotta diventa un esempio:

```json
{
  "input_docx_hash": "",
  "output_docx_hash": "",
  "case_lock": {},
  "qa_result": {},
  "human_feedback": "",
  "root_cause_label": "template_contamination",
  "severity": "CRITICAL",
  "fix_applied": "full_package_contamination_scan",
  "final_pass": false
}
```

### 14.2 Labels

```text
template_contamination
semantic_inconsistency
table_structure_drift
arithmetic_failure
style_drift
hidden_xml_residue
wrong_template_family
premature_delivery
```

### 14.3 Features

```text
forbidden_token_count
old_client_token_count
table_signature_distance
appendix_profile_distance
pli_consistency_score
arithmetic_pass_bool
search_narrative_match_score
hidden_xml_contamination_count
style_palette_distance
docx_package_valid_bool
release_state_valid_bool
```

### 14.4 Model output

```text
PASS
WARN
BLOCK
probable_error_type
next_minimal_fix
```

## 15. Final Delivery Rule

Consegnare il DOCX solo se tutti questi sono veri:

```text
CASE_LOCK valid
Template router deterministic
DOCX package valid
XML injection completed
Arithmetic pass
Semantic consistency pass
Full package contamination scan pass
Table fingerprint pass
Appendix profile pass
Error Detective no unresolved CRITICAL/HIGH
Council does not BLOCK
QA score >= 99/100
```

Altrimenti consegnare solo:

```text
QA Failure Report
Root cause
Minimal fix
Missing inputs
Recovery steps
```

## 16. One-line operating command

```text
Think first, lock the case, clone the template, inject only verified data, scan every XML part, block on any critical drift, then deliver only with QA evidence.
```
