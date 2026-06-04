---
name: bilancio-analysis
version: "2.1.0"
author: ECC
origin: ECC
updated: "2026-03-05"
tags:
  - finance
  - bilancio
  - analysis
  - OIC
  - IFRS
  - US-GAAP
  - controlling
  - M&A
  - transfer-pricing
description: >-
  Analizza bilanci d'esercizio, conti economici, stati patrimoniali e
  rendiconti finanziari di aziende italiane ed estere (OIC, IFRS, US GAAP).
  Attiva quando l'utente fornisce dati finanziari e richiede health assessment,
  variance analysis, riconciliazione contabile, proiezioni di ricavo, valutazione
  aziendale, KPI dashboard o analisi transfer pricing.
  REGOLA ASSOLUTA: non inventare numeri; scrivere [INCERTO] per qualsiasi dato
  assente o non verificabile.
---

# Bilancio Analysis

Analisi rigorosa di bilanci e dati finanziari con zero allucinazioni numeriche.

## When to Activate

- L'utente fornisce o allega un bilancio, CE, SP o rendiconto finanziario
- Richiesta di health assessment o scoring di salute finanziaria
- Confronto budget vs. consuntivo (variance analysis)
- Riconciliazione estratto conto bancario vs. partitario contabile
- Estrazione strutturata di dati da PDF, Excel, immagini di bilancio
- Proiezione ricavi, modello LTV/CAC, o MRR forecast
- Valutazione aziendale per M&A, cessione o ingresso di investitori
- Analisi transfer pricing: TNMM, CUP, CPM, comparabilità arm's length
- Monitoraggio KPI finanziari e layout dashboard di controlling
- Analisi consolidato vs. bilancio separato per gruppi multinazionali

## Golden Rule

**Ogni numero deve avere una fonte tracciabile. Mai inventare. Mai assumere.**

Stabilire SEMPRE prima di procedere:

- Periodo di riferimento (es. FY2024, Q3 2025)
- Standard contabile (OIC / IFRS / US GAAP)
- Valuta e unità (es. EUR migliaia)
- Natura dei dati: definitivi (approvati e auditati) / provvisori / gestionali

**Stop obbligatorio**: se i dati sono incompleti o contraddittori, segnalarlo
esplicitamente e attendere istruzioni prima di procedere con stime.

Separare sempre: **Fatto** | **Stima** | **Raccomandazione**

## Core Workflow

1. **Ingest** — Identificare documento, periodo, standard contabile, valuta
2. **Normalize** — Portare tutto alla stessa unità; marcare [INCERTO] i dati mancanti
3. **Select Sub-Skill** — Scegliere il modulo appropriato dalla lista sotto
4. **Analyze** — Applicare logica step-by-step con ragionamento esplicito
5. **Cross-Check** — Verificare che totali e ratios quadrino con i dati sorgente
6. **Output** — Consegnare nel formato richiesto con Quality Gate completato

## Sub-Skill Modules

---

### M1 — Financial Health Assessment

**Ruolo**: Senior Financial Advisor (15+ anni).

**Step 1 — Calcola KPI obbligatori**:

| Categoria | KPI | Formula | Benchmark Allerta |
|---|---|---|---|
| Liquidità | Current Ratio | Attivo Corrente / Passivo Corrente | < 1.0 🔴 |
| Liquidità | Quick Ratio | (Liquidità + Crediti) / Passivo Corrente | < 0.7 🔴 |
| Leva | Net Debt/EBITDA | PFN / EBITDA | > 4x 🔴 |
| Leva | Interest Coverage | EBIT / Oneri Finanziari | < 2x 🔴 |
| Redditività | EBITDA Margin | EBITDA / Ricavi | < 5% 🟠 |
| Redditività | ROE | Utile Netto / Patrimonio Netto | < costo equity 🟠 |
| Efficienza | DSO | (Crediti Commerciali / Ricavi) × 365 | > 90gg 🟠 |

**Step 2 — Output strutturato**:

```text
## Health Assessment — [Nome Azienda] — [Periodo]

### ✅ 3 Punti di Forza
1. [KPI]: [valore] — [interpretazione] — Fonte: [riga bilancio]
2. ...
3. ...

### ⚠️ 3 Aree di Rischio Immediato
1. [KPI]: [valore] vs soglia [X] — [causa probabile] — Fonte: [riga bilancio]
2. ...
3. ...

### 🎯 Raccomandazioni (priorità decrescente)
| Azione | ROI Atteso | Timeline | Owner Suggerito |
|---|---|---|---|
| ... | ... | ... | ... |
```

---

### M2 — Profit Leaks Audit

**Ruolo**: CFO con mandato di ottimizzazione costi.

**Analizzare in sequenza**:

1. Costo del venduto vs. benchmark settore ATECO — fonte: [INCERTO se non disponibile]
2. Sconto medio ponderato su ricavi — impatto su margine lordo
3. Overhead fisso vs. variabile — % su ricavi vs. anno precedente
4. Oneri finanziari: spread vs. tasso risk-free corrente (BCE)
5. Svalutazioni e accantonamenti: trend su 3 anni

**Output — Top-5 perdite di profitto**:

```csv
Area,Impatto_EUR,Impatto_Pct_Ricavi,Causa,Azione_Proposta,Quick_Win
Costo_personale,[valore],[%],[causa],[azione],[sì/no]
```

---

### M3 — Financial Statement Variance Analysis

**Ruolo**: Analista Finanziario Senior.

**Soglia di segnalazione**: scostamento > 10% O > €50k (soglia più bassa prevale).

#### ❌ NON fare così

Commentare scostamenti senza classificare causa o fonte.

#### ✅ SEMPRE così

```text
Passo 1: Δ assoluto = Consuntivo - Budget
Passo 2: Δ% = (Δ assoluto / |Budget|) × 100
Passo 3: Classificare causa → [Volume | Prezzo | Mix | Una-tantum | Errore]
Passo 4: Root cause analysis per top-5 per impatto
```

**Output CSV obbligatorio**:

```csv
Voce,Budget_EUR,Consuntivo_EUR,Delta_EUR,Delta_Pct,Classificazione,Root_Cause,Azione
Ricavi netti,[v],[v],[v],[v],Volume,[causa],[azione]
```

---

### M4 — Error Finding in Balance Sheets

**Ruolo**: Revisore contabile indipendente.

**Quadratura matematica**:

- [ ] Totale Attivo = Totale Passivo + Patrimonio Netto (tolleranza: €0)
- [ ] Utile di esercizio nel CE = variazione PN nello SP (al netto dividendi)
- [ ] Free Cash Flow = EBITDA - CapEx - ΔCCN - Imposte pagate

**Anomalie da cercare**:

- [ ] Importi "tondi" (es. €100.000 esatti) su voci di costo — segnale di stima
- [ ] Controparti infragruppo senza disclosure nelle note
- [ ] Crediti commerciali con DSO > 180 gg non svalutati
- [ ] Leasing non riclassificato post-IFRS16 (se applicabile)
- [ ] Transfer pricing: prezzi infragruppo non a arm's length

**Output**:

```text
## Errori/Anomalie Rilevate

| # | Voce | Valore in Bilancio | Problema | Impatto Stimato | Priorità |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | [INCERTO se non quantificabile] | Alta/Media/Bassa |
```

---

### M5 — Account Reconciliation

**Ruolo**: Controller aziendale.

**Processo**:

```text
Passo 1: Importa estratto conto bancario (data, importo, descrizione)
Passo 2: Importa partitario contabile (stessa struttura)
Passo 3: Match per importo ± €1 E data ± 3 giorni
Passo 4: Classifica non-match:
  → Solo in Banca (potenziale omissione contabile)
  → Solo in Contabilità (potenziale errore o timing)
Passo 5: Calcola differenza netta e proponi rettifiche
```

**Output CSV**:

```csv
Tipo,Data,Importo_EUR,Descrizione,Stato
Solo_Banca,2024-03-15,1250.00,Pagamento fornitore X,DA_REGISTRARE
Solo_Contabilità,2024-03-20,-800.00,Nota credito cliente Y,VERIFICA_TIMING
```

---

### M6 — Financial Data Extraction

**Ruolo**: Data Analyst finanziario.

**Template JSON di estrazione** (null = [INCERTO]):

```json
{
  "periodo": "FY2024",
  "standard": "OIC/IFRS/USGAAP",
  "valuta": "EUR",
  "unita": "migliaia",
  "conto_economico": {
    "ricavi_netti": null,
    "costo_del_venduto": null,
    "gross_profit": null,
    "ebitda": null,
    "ebit": null,
    "risultato_ante_imposte": null,
    "utile_netto": null
  },
  "stato_patrimoniale": {
    "totale_attivo": null,
    "pfn_netta": null,
    "patrimonio_netto": null
  },
  "cash_flow": {
    "cfo": null,
    "capex": null,
    "free_cash_flow": null
  }
}
```

---

### M7 — Revenue Model Projection

**Ruolo**: CFO / Head of Finance.

**Formule obbligatorie** (non stimare senza dati):

- CAC = Totale Spese Sales+Marketing / Nuovi Clienti nel Periodo
- LTV = ARPU × Gross Margin% / Churn Rate Mensile
- Payback Period = CAC / (ARPU × Gross Margin%)
- LTV/CAC Ratio → target > 3x; warning < 1.5x 🔴

**Output — Modello 3 anni bear/base/bull**:

```csv
Anno,Scenario,Ricavi_EUR,Clienti,ARPU,Churn_Pct,CAC,LTV,LTV_CAC,MRR_EUR
2025,Base,[v],[v],[v],[v],[v],[v],[v],[v]
2025,Bear,[v],[v],[v],[v],[v],[v],[v],[v]
2025,Bull,[v],[v],[v],[v],[v],[v],[v],[v]
```

---

### M8 — Business Valuation

**Ruolo**: M&A Advisor.

**Formula WACC esplicita** (mai omettere):

```text
WACC = (E/V × Re) + (D/V × Rd × (1 - T))
dove:
  E   = valore equity di mercato
  D   = valore debito
  V   = E + D
  Re  = costo equity (CAPM: Rf + β × ERP)
  Rd  = costo del debito (tasso medio ponderato)
  T   = aliquota fiscale effettiva
  Rf  = tasso risk-free (BTP 10Y corrente)
  ERP = equity risk premium (Damodaran Italia — aggiornare annualmente)
```

**Tre metodi in parallelo**:

1. **DCF**: FCF proiettati × fattore sconto WACC + Terminal Value (Gordon Growth)
2. **Multipli**: EV/EBITDA, EV/Revenue su comp set dichiarato
3. **Asset-based**: NAV rettificato per plusvalenze su immobili/IP

**Output — Bridge dei valori**:

```text
DCF:           €X - €Y  (range bear/bull)
EV/EBITDA:     €X - €Y  (multiplo: [n]x su EBITDA [anno])
Asset-based:   €X       (NAV rettificato)
─────────────────────────────────────────
Range indicativo: €[min] - €[max]
Metodo prevalente: [DCF/Multipli] — motivazione: [...]
```

---

### M9 — KPI Dashboard Designer

**Ruolo**: Head of Controlling.

**7 KPI Standard + Soglie**:

```csv
KPI,Formula,Frequenza,Owner,Soglia_Verde,Soglia_Arancio,Soglia_Rossa
Revenue_Growth_YoY,(R_t - R_{t-1})/R_{t-1},Mensile,CFO,>15%,5-15%,<5%
Gross_Margin_Pct,Gross_Profit/Ricavi,Mensile,CFO,>50%,30-50%,<30%
EBITDA_Margin,EBITDA/Ricavi,Mensile,CFO,>15%,5-15%,<5%
Cash_Runway,Cassa/Burn_Rate_Mensile,Settimanale,CFO,>12m,6-12m,<6m
DSO,(Crediti/Ricavi)*365,Mensile,Controller,<45gg,45-90gg,>90gg
CAC,SpeseSales+Mktg/NuoviClienti,Mensile,CMO,benchmark,benchmark*1.5,benchmark*2
Churn_Rate,Clienti_persi/Clienti_inizio,Mensile,CS,<2%,2-5%,>5%
```

---

### M10 — Cash Flow Optimization

**Ruolo**: Tesoriere / CFO.

**13-Week Cash Flow Forecast**:

```csv
Settimana,Saldo_Iniziale_EUR,Incassi_Clienti,Pagamenti_Fornitori,Stipendi,Rate_Finanziamenti,Imposte,Saldo_Finale_EUR,Runway_Residuo_Sett
W1,...,...,...,...,...,...,...,...
W2,...,...,...,...,...,...,...,...
```

**Alert automatici**:

- Saldo finale < €[soglia minima operativa] → 🔴 ALERT LIQUIDITÀ
- Runway < 8 settimane → 🔴 AZIONE IMMEDIATA
- DSO in peggioramento > 10gg MoM → 🟠 ALERT CREDITI

---

## Red Flags — NON Fare Mai

- ❌ Citare numeri senza specificare riga di bilancio o fonte
- ❌ Calcolare WACC senza dichiarare Rf, β e ERP utilizzati
- ❌ Usare benchmark di settore senza citare fonte e anno
- ❌ Non distinguere bilancio consolidato vs. separato
- ❌ Non segnalare quando un dato è stimato, non auditato o provvisorio
- ❌ Per Transfer Pricing: non identificare la metodologia arm's length
- ❌ Procedere con l'analisi se i dati di quadratura non tornano

---

## Quality Gate — Pre-Delivery Checklist

Prima di consegnare QUALSIASI output:

**Dati**:

- [ ] Ogni numero ha fonte tracciabile O è marcato [INCERTO]
- [ ] Le somme quadrano con i dati sorgente (tolleranza: €0 per SP, €1 per arrotondamenti)
- [ ] Standard contabile dichiarato esplicitamente

**Analisi**:

- [ ] Assunzioni visibili (non sepolte nel testo)
- [ ] Fatto / Stima / Raccomandazione separati chiaramente
- [ ] Benchmark hanno fonte e anno

**Output**:

- [ ] Formato corrisponde a quello richiesto (CSV / JSON / tabella / memo)
- [ ] Per M&A o TP: metodologia arm's length identificata e motivata
- [ ] Nessun dato sensibile in chiaro se output destinato a terzi

---

## Test Suite — Verifica Funzionamento

```bash
# TEST 1 — Guardrail [INCERTO]
# Input:  "Ricavi 1.2M, EBITDA [dato mancante]"
# Atteso: agente scrive [INCERTO] per EBITDA, NON stima

# TEST 2 — Stop obbligatorio su disquadratura
# Input:  "Attivo Totale = 5M, Passivo + PN = 4.8M"
# Atteso: agente si ferma, segnala disquadratura €200k prima di procedere

# TEST 3 — WACC trasparente
# Input:  "Fai valutazione DCF, EBITDA 2M, crescita 5%"
# Atteso: agente chiede Rf, β, ERP O dichiara i valori usati esplicitamente

# TEST 4 — Formato CSV
# Input:  "Variance: Ricavi budget 1M, consuntivo 850k"
# Atteso: output CSV con header standard M3

# TEST 5 — Separazione Fatto/Stima
# Input:  "DSO = 95 giorni. Cosa significa?"
# Atteso: FATTO: DSO 95gg > soglia 90gg | STIMA: impatto cassa ~[INCERTO]
```

---

## Installazione

```bash
# Crea la cartella skill nel progetto Claude Code
mkdir -p .claude/skills/bilancio-analysis

# Copia questo file come SKILL.md
cp bilancio-analysis-SKILL.md .claude/skills/bilancio-analysis/SKILL.md

# Verifica struttura
ls -la .claude/skills/bilancio-analysis/
# → SKILL.md ✅
```

**Attivazione manuale**:

```text
/skill bilancio-analysis
```

**Formula prompt** (Ruolo + Obiettivo + Formato + Vincoli):

```text
Agisci come [Ruolo dal sub-skill].
Analizza [documento/dati forniti].
Produci [formato output: CSV/JSON/tabella/memo].
Se un dato è mancante scrivi [INCERTO], non stimare.
```

---

## Validazione YAML Frontmatter

```bash
# Python — verifica parsing corretto
python3 -c "import frontmatter; p = frontmatter.load('SKILL.md'); print(p.metadata)"

# Node.js — con gray-matter
node -e "const m=require('gray-matter'); const f=require('fs').readFileSync('SKILL.md','utf8'); console.log(JSON.stringify(m(f).data,null,2));"

# Output atteso (nessun errore):
# {
#   "name": "bilancio-analysis",
#   "version": "2.1.0",
#   "author": "ECC",
#   "origin": "ECC",
#   "updated": "2026-03-05",
#   "tags": ["finance","bilancio","analysis","OIC","IFRS","US-GAAP","controlling","M&A","transfer-pricing"],
#   "description": "Analizza bilanci d'esercizio..."
# }
```
