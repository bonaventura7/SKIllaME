---
name: intercompany-segregation
description: >
  Segregates accounting ledger data into intra-group vs. third-party transactions.
  v3.0 introduces a Business Context Engine that identifies entity functional profile
  (manufacturer / distributor / service provider / holding / principal), maps expected
  intercompany flow patterns by entity type and ATECO sector, and explains WHY each
  CoGe account matters for TP analysis before any classification begins.
  Uses counterparty names AND CoGe account labels as dual-signal validation.
version: 3.0.0
author: Studio Biscozzi Nobili & Partners — Transfer Pricing Dept.
tags:
  - transfer-pricing
  - accounting
  - IFRS
  - OIC
  - consolidation
  - intercompany
  - coge
  - functional-analysis
  - business-context
  - ATECO
  - benchmarking
temperature: 0
allowed-tools:
  - Read
  - Write
  - Grep
  - Bash
guardrails:
  - "Non classificare senza evidenza: nessun segnale → [INCERTO]"
  - "Non inventare VAT, codici conto, tassi FX, denominazioni"
  - "Segnali contrastanti → sempre [INCERTO], mai forzare"
  - "Non inferire tipo entità da singola transazione: richiedere conferma utente"
  - "WHY Engine: solo ragionamento fondato su segnali presenti nei dati"
---

# Skill: Intercompany Segregation v3.0

**Segregazione Infragruppo vs. Terzi — Business Context Engine + Analisi Piano dei Conti**

---

## Architettura della Skill

```
FASE 0     → Raccolta dati base (parti correlate, piano dei conti, periodo)
FASE 0-BIS → Business Context Engine (tipo entità, settore, supply chain)
FASE 1     → Identificazione parti correlate (lookup + metadati)
FASE 1-BIS → Functional Profile Mapper (pattern IC attesi per tipo entità)
FASE 2     → Analisi Piano dei Conti CoGe (dual-signal validation)
FASE 2-BIS → WHY Engine (spiegazione logica per ogni conto nel contesto)
FASE 3     → Output: tabella classificata
FASE 4     → Guardrail Anti-Allucinazione
FASE 5     → Quality Gate: quadratura
FASE 6     → Business Logic Validator (coerenza con profilo funzionale dichiarato)
```

---

## FASE 0 — Raccolta Informazioni Base

> ⚠️ **Non iniziare la classificazione** finché non hai almeno una risposta
> per ciascun blocco. Poni tutte le domande in **un unico messaggio**.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOCCO A — DATI CONTABILI E STRUTTURA DI GRUPPO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PARTI CORRELATE — Elenco entità del gruppo
   Denominazione legale + P.IVA/VAT (se disponibile).
   Es.: "SubCo GmbH (DE123456789), Holding SpA (IT01234567890)"
   → Se non disponibile, inferirò dai metadati (meno accurato).

2. PIANO DEI CONTI (CoGe)
   Incolla o allega anche solo i conti presenti nell'estratto.
   → Se non disponibile, userò le convenzioni OIC/IFRS standard.

3. PERIODO DI ANALISI
   Es.: FY2025, Q1 2026, 01/01/2025–30/06/2025.

4. VALUTA DI REPORTING + TASSI FX
   → Se non forniti, userò tassi ECB di riferimento alla data transazione.

5. LIVELLO DI DETTAGLIO (spunta quello che ti serve):
   [ ] Registrazioni di elisione (bilancio consolidato)
   [ ] Colonna "Ragionamento" con spiegazione classificazione
   [ ] Riepilogo per tipologia transazione
   [ ] WHY Engine attivo (spiegazione logica per ogni conto — vedi FASE 2-BIS)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOCCO B — CONTESTO DI BUSINESS (Business Context Engine v3.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. TIPO DI ENTITÀ — Come si posiziona nella catena del valore del gruppo?
   [ ] Produttore full-fledged   (R&D, produzione, vendita, rischio completo)
   [ ] Contract manufacturer     (produce su specifiche del principal, rischio limitato)
   [ ] Toll manufacturer         (trasforma materiali del principal, zero rischio)
   [ ] Distributore full-risk    (acquista, stocca e rivende in proprio)
   [ ] Limited-risk distributor  (distribuisce per conto del principal, rischio limitato)
   [ ] Commissionnaire/Agente    (intermediario, non acquisisce titolo sui beni)
   [ ] Service provider          (IT, HR, legale, finanza, marketing)
   [ ] Principal / IP-holding    (detiene intangibili, gestisce rischi strategici)
   [ ] Holding / Sub-holding     (gestione partecipazioni, finanziamento)
   [ ] Misto / Non so            (descrivi brevemente cosa fa la società)
   → CRITICO: determina i pattern IC attesi e i conti da scrutinare con priorità.

7. SETTORE / CODICE ATECO (o NACE)
   Es.: ATECO 26.20 | ATECO 46.90 | ATECO 62.01 | ATECO 70.10
   → Se non noti il codice, descrivi il prodotto/servizio venduto.

8. SUPPLY CHAIN
   a) Principali FORNITORI:
      [ ] Prevalentemente IC (> 70%)   [ ] Mix (30–70%)   [ ] Prevalentemente terzi (< 30%)
      → Cosa acquista? (materie prime / semilavorati / prodotti finiti / servizi)

   b) Principali CLIENTI:
      [ ] Prevalentemente IC (> 70%)   [ ] Mix (30–70%)   [ ] Prevalentemente terzi (< 30%)
      → Cosa vende? (prodotti finiti / semilavorati / servizi / licenze)

   c) Ha DIPENDENTI propri? Quanti? (indicativo)
   d) Ha IMPIANTI / MAGAZZINI propri?         [ ] Sì   [ ] No
   e) Detiene INTANGIBILI (brevetti, marchi)? [ ] Sì   [ ] No   [ ] In licenza
```

---

## FASE 0-BIS — Business Context Engine: Logica di Attivazione

Sulla base delle risposte al Blocco B, la skill attiva automaticamente il
**Functional Profile Mapper (FASE 1-BIS)**, che precarica i pattern IC attesi
per il tipo di entità dichiarato. Questo consente di:

- identificare *a priori* quali conti CoGe scrutinare con priorità
- rilevare anomalie strutturali (es. LRD con conti R&D → segnale di riqualifica)
- generare insight TP-rilevanti nell'output finale

---

## FASE 1 — Identificazione Parti Correlate

### 1A — Da lista fornita (priorità massima)

Costruisci internamente una lookup table con le entità fornite:

| Denominazione Legale | P.IVA / VAT    | Tipo        | Paese   | Note        |
|----------------------|----------------|-------------|---------|-------------|
| SubCo GmbH           | DE123456789    | Controllata | Germania | produzione  |
| Holding SpA          | IT01234567890  | Capogruppo  | Italia  | principal   |
| US Branch Inc.       | EIN 12-3456789 | Branch      | USA     | vendite     |

Match **case-insensitive**, tolleranza typo ±1 carattere, su ogni controparte.
- Match trovato → `A — Infragruppo`
- Nessun match → Fase 1B

### 1B — Da metadati (lista non disponibile o match non trovato)

| Segnale | Esempio | Forza |
|---------|---------|-------|
| Suffisso societario + nome simile alla capogruppo | "Alfa GmbH" se capogruppo = "Alfa SpA" | 🟡 MEDIO |
| Prefisso codice fornitore: `IG-` `IC-` `GRP-` `REL-` `9xxx` | "IG-0045" | 🟢 ALTO |
| Descrizione: "intercompany", "IC", "management fee IC", "recharge" | "Recharge IC Q1" | 🟢 ALTO |
| P.IVA paese diverso + nome identico al gruppo | "Alpha Inc" per gruppo "Alpha" | 🟡 MEDIO |
| Nessun segnale | "Anonimo SRL" senza codice | 🔴 INCERTO |

> **Regola:** segnale ALTO da almeno 1 fonte → `A — Infragruppo`.
> Solo segnale MEDIO senza conferma → `[INCERTO]`.

---

## FASE 1-BIS — Functional Profile Mapper

> **Novità v3.0.** Attivato automaticamente dopo FASE 0-BIS.
> Mappa: tipo entità → flussi IC attesi → priorità di scrutinio dei conti.

---

### Profilo 1 — Produttore Full-Fledged

**Logica di business**

La società acquista input da fornitori IC e/o terzi, li trasforma con propria
forza lavoro e impianti, e vende i prodotti finiti assumendosi tutti i rischi di
mercato e inventario. Controlla almeno alcune funzioni DEMPE sugli intangibili
produttivi.

**Flussi IC tipicamente attesi**

```
ACQUISTI IC  →  materie prime, componenti, semilavorati da affiliati
VENDITE IC   →  prodotti finiti a distributori affiliati
SERVIZI IC   →  management fee, IT, HR dalla capogruppo
ROYALTY IC   →  possibile licenza di tecnologia/know-how dalla parent
FINANZA IC   →  eventuali finanziamenti infragruppo
```

**Conti da scrutinare con priorità**

| Conto / Range   | Perché è rilevante per un produttore |
|-----------------|---------------------------------------|
| B6 CE / 3000xx  | Acquisti MP: % IC vs terzi → segnala contract/toll se IC > 80% |
| B11 CE          | Var. rimanenze: alto stock = rischio inventario proprio → full-fledged; basso → toll |
| B9 CE           | Costo personale: alto = funzioni in-house; basso = possibile hollow entity |
| B14 CE          | Ammortamenti: impianti propri → conferma asset materiali (DEMPE) |
| A1 CE / 1200xx  | Ricavi: % IC alta → entità captive → prezzo IC è il TP risk principale |
| 7400xx          | Mgmt fee IC: verificare beneficio ricevuto, arm's length e documentazione |

**Segnali di anomalia TP**

```
⚠️  Acquisti IC > 80% del COGS   → possibile contract/toll, non full-fledged
⚠️  B9 vicino a zero             → entità senza sostanza → rischio DEMPE
⚠️  Royalty IC assente + R&D     → verificare ownership economico intangibili
⚠️  Margine operativo negativo   → possibile violazione arm's length
```

---

### Profilo 2 — Distributore (Full-Risk / Limited-Risk)

**Logica di business**

La società acquista prodotti finiti da affiliati e li rivende a clienti terzi
sul mercato locale. Non trasforma il prodotto.
- **Full-risk:** sopporta rischi di inventario, credito e mercato in proprio.
- **LRD:** rischio limitato, agisce per conto del principal.

**Flussi IC tipicamente attesi**

```
ACQUISTI IC  →  prodotti finiti dal gruppo (CORE — quota elevata su COGS)
VENDITE IC   →  rare (solo se ridistribuisce a sub-distributori affiliati)
SERVIZI IC   →  management fee, IT, HR dalla capogruppo
ROYALTY IC   →  eventuale uso del marchio del gruppo
FINANZA IC   →  eventuali facility / cash pooling
```

**Conti da scrutinare con priorità**

| Conto / Range    | Perché è rilevante per un distributore |
|------------------|----------------------------------------|
| B6 CE / 4000xx   | PRIMARIO: acquisti merci IC = cuore del business; % IC > 80% → captive distributor |
| A1 CE / 1200xx   | Ricavi quasi tutti terzi; % IC alta → possibile agente/commissionnaire |
| B11 CE           | LRD ha scorte minime; alto stock = rischio inventario = full-risk |
| B9 CE            | LRD ha pochi dipendenti (sales force); nessun personale → possibile commissionnaire |
| B14 CE           | Ammortamenti bassi/nulli → no impianti produttivi → profilo distributivo |
| 1200xx / 1600xx  | Crediti terzi vs crediti IC: proporzione rivela il mix di clientela effettivo |
| 7400xx           | Mgmt fee IC: verifica che non ecceda il beneficio ricevuto (struttura LRD) |

**Indicatori finanziari chiave**

```
Gross Margin (GM) = (A1 – B6) / A1
  → Full-risk distributor atteso: GM 15–35%
  → LRD atteso:                  GM  5–15%

Return on Sales (ROS) = EBIT / A1
  → Benchmark TNMM LRD tipico:  ROS 1–5%
```

**Segnali di anomalia TP**

```
⚠️  Acquisti IC = 100% COGS              → prezzo IC è il solo driver di profitto
⚠️  GM >> mediana di settore             → possibile sovra-pricing su vendite IC
⚠️  GM < Q1 benchmark                   → possibile sotto-remunerazione
⚠️  Stock elevato, no rischio svalutaz.  → classificare come LRD, non full-risk
⚠️  Ricavi da clienti IC > 30%           → riconsiderare profilo (agente?)
```

---

### Profilo 3 — Contract / Toll Manufacturer

**Logica di business**

- **Contract:** produce su specifiche del principal; acquista input in proprio
  ma vende esclusivamente al principal. Zero rischi di mercato né R&D.
- **Toll:** trasforma materiali forniti dal principal; non acquisisce mai la
  proprietà degli input; tariffato su fee di lavorazione.

**Flussi IC tipicamente attesi**

```
ACQUISTI IC  →  materie prime/componenti dal principal (contract)
              oppure ZERO — materiali consegnati direttamente (toll)
VENDITE IC   →  100% al principal (prodotto finito o trasformazione)
SERVIZI IC   →  management fee, IT
FINANZA IC   →  finanziamenti capex approvati dal principal
```

**Conti da scrutinare con priorità**

| Conto / Range | Perché è rilevante |
|---------------|--------------------|
| B6 CE         | Contract: acquisti IC ≈ 100% → conferma dipendenza; Toll: B6 = 0 (materiali non transitano in CE) |
| B9 CE         | Personale alto → cost plus mark-up legittimo; basso → verifica reale valore aggiunto |
| B14 CE        | Ammortamenti alti → il principal deve coprire il rendimento del capitale investito negli impianti |
| A1 CE         | Ricavi ≈ 100% IC; presenza ricavi terzi → verificare compatibilità con profilo contract |

**Indicatori finanziari chiave**

```
Berry Ratio      = Gross Profit / Operating Expenses
Cost Plus Markup = EBIT / (B6 + B7 + B9 + B14)
  → Atteso: 5–15% per contract manufacturer tipico
```

---

### Profilo 4 — Service Provider (Management / Shared Services)

**Logica di business**

Eroga servizi infragruppo (IT, HR, legale, contabilità, marketing, finanza).
Clienti quasi esclusivamente IC; fornitori misti (terzi e gruppo).
Remunerazione via management fee o cost-sharing arrangement.

**Flussi IC tipicamente attesi**

```
RICAVI IC    →  management fee, IT recharge, HR services alle affiliate
ACQUISTI IC  →  sub-appalto o piattaforme acquistate dal gruppo
COSTI TERZI  →  consulenze esterne, licenze software, affitti
FINANZA IC   →  raramente
```

**Conti da scrutinare con priorità**

| Conto / Range | Perché è rilevante |
|---------------|--------------------|
| B9 CE         | PRINCIPALE: personale = il "prodotto" è il lavoro; % B9/ricavi → base cost-plus (5–10%) |
| B7 CE / 6xxx  | Servizi terzi: spesso base cost "pass-through" nel cost pool di allocazione IC |
| A1 / A5 CE    | Ricavi IC ≈ 100%; presenza ricavi terzi = benchmark CUP interno potenziale |
| 7400xx        | Mgmt fee RICEVUTA dalla parent vs EROGATA → impatto sul mark-up calcolato |

**Indicatori finanziari chiave**

```
Cost Plus Markup = EBIT / Total Operating Costs
  → OCSE TNMM / Cost Plus, routine services:    5–15%
  → Low value-adding services (OCSE TPG §7.61): cap 5%
```

---

### Profilo 5 — Holding / Principal / IP Company

**Logica di business**

Detiene partecipazioni, gestisce intellectual property, finanzia le affiliate.
Flussi IC prevalentemente finanziari e di royalty.
Flussi commerciali con terzi ridotti o assenti.

**Flussi IC tipicamente attesi**

```
RICAVI IC    →  dividendi, royalty, interessi attivi da affiliati
COSTI IC     →  gestione partecipazioni, sub-licenza IP
FINANZA IC   →  finanziamenti erogati, cash pooling
TERZI        →  consulenti legali/fiscali, servizi corporate
```

**Conti da scrutinare con priorità**

| Conto / Range   | Perché è rilevante |
|-----------------|--------------------|
| C15 / C16 CE    | Proventi/Oneri finanziari: cuore del business holding; interessi IC a tassi arm's length? |
| 8000xx          | Finanziamenti IC: tasso, scadenza, credit rating del debitore (OCSE Action 4 / art. 96 TUIR) |
| 7400xx          | Royalty IC: verifica DEMPE, ownership economico, tasso ALS (CUP o profit split) |
| C17bis / D CE   | Rivalutazioni/svalutazioni partecipazioni → non IC, ma rilevanti per analisi economica |

---

## FASE 2 — Analisi Piano dei Conti CoGe (Dual-Signal Validation)

### 2A — Conti Infragruppo (segnale ALTO 🟢)

**Crediti / Debiti IC — OIC 24**

| Range conto        | Descrizione tipica        | Segnale     |
|--------------------|---------------------------|-------------|
| `1600xx`–`1609xx`  | Crediti v/controllate     | 🟢 ALTO IC  |
| `1610xx`–`1619xx`  | Crediti v/controllanti    | 🟢 ALTO IC  |
| `1620xx`–`1629xx`  | Crediti v/collegate       | 🟢 ALTO IC  |
| `2600xx`–`2609xx`  | Debiti v/controllate      | 🟢 ALTO IC  |
| `2610xx`–`2619xx`  | Debiti v/controllanti     | 🟢 ALTO IC  |
| `2620xx`–`2629xx`  | Debiti v/collegate        | 🟢 ALTO IC  |

**Costi / Ricavi IC**

| Range conto        | Descrizione tipica               | Segnale     |
|--------------------|----------------------------------|-------------|
| `5800xx`–`5899xx`  | Ricavi da controllate / IC Sales | 🟢 ALTO IC  |
| `6800xx`–`6899xx`  | Costi da controllate / IC Purch. | 🟢 ALTO IC  |
| `7400xx`–`7499xx`  | Management fees / Royalty IC     | 🟢 ALTO IC  |
| `7500xx`–`7599xx`  | Interessi attivi/passivi IC      | 🟢 ALTO IC  |
| `8000xx`–`8099xx`  | Finanziamenti infragruppo        | 🟢 ALTO IC  |

**Label testuali rilevanti:**
`controllate` · `controllanti` · `collegate` · `infragruppo` · `IC` ·
`intercompany` · `related` · `intragroup` · `partecipate`

---

### 2B — Conti Terzi (segnale ALTO 🟢)

| Range conto        | Descrizione tipica                      | Segnale        |
|--------------------|-----------------------------------------|----------------|
| `4000xx`–`4999xx`  | Fornitori terzi (debiti commerciali)    | 🟢 ALTO Terzi  |
| `1200xx`–`1299xx`  | Clienti terzi (crediti commerciali)     | 🟢 ALTO Terzi  |
| `6100xx`–`6399xx`  | Costi per servizi terzi                 | 🟢 ALTO Terzi  |
| `5100xx`–`5399xx`  | Ricavi da clienti terzi                 | 🟢 ALTO Terzi  |
| `3000xx`–`3999xx`  | Rimanenze / fornitori materie prime     | 🟢 ALTO Terzi  |

---

### 2C — Conti Neutri / Ambigui (segnale BASSO 🟡)

| Range conto        | Descrizione tipica       | Azione richiesta          |
|--------------------|--------------------------|---------------------------|
| `1700xx`–`1799xx`  | Ratei e risconti attivi  | Usa info controparte       |
| `2700xx`–`2799xx`  | Ratei e risconti passivi | Usa info controparte       |
| `6900xx`–`6999xx`  | Costi diversi            | Richiedi label piano conti |
| `5900xx`–`5999xx`  | Ricavi diversi           | Richiedi label piano conti |
| `9000xx`–`9999xx`  | Conti d'ordine           | Richiedi label piano conti |

---

### 2D — Matrice di Decisione Finale

| Segnale Controparte | Segnale CoGe       | Classificazione Finale                    |
|---------------------|--------------------|-------------------------------------------|
| 🟢 ALTO IC          | 🟢 ALTO IC         | **A — Infragruppo** *(alta confidenza)*   |
| 🟢 ALTO IC          | 🟢 ALTO Terzi      | **[INCERTO]** ⚠️ segnali contrastanti     |
| 🟢 ALTO IC          | 🟡 NEUTRO          | **A — Infragruppo** *(media confidenza)*  |
| 🟡 MEDIO IC         | 🟢 ALTO IC         | **A — Infragruppo** *(media confidenza)*  |
| 🟡 MEDIO IC         | 🟡 NEUTRO          | **[INCERTO]** revisione manuale           |
| 🟢 ALTO Terzi       | 🟢 ALTO Terzi      | **B — Terzi** *(alta confidenza)*         |
| 🟢 ALTO Terzi       | 🟡 NEUTRO          | **B — Terzi** *(media confidenza)*        |
| 🔴 NESSUNO          | 🔴 NESSUNO         | **[INCERTO]** dati insufficienti          |

---

## FASE 2-BIS — WHY Engine

> **Novità v3.0.** Attivabile dall'utente (opzione 5 del Blocco A) oppure
> automaticamente quando il conto è neutro o i segnali sono discordanti.
> Genera per ogni riga classificata una nota di ragionamento TP-oriented.

**Formato nota WHY:**

```
[WHY] Conto 6800xx — Costi da controllate
→ Tipo entità : Distributore LRD
→ Atteso      : acquisti IC di prodotti finiti dal principal = voce di costo principale
→ Osservaz.   : importo coerente con ~70% del COGS → conferma profilo LRD
→ Rilevanza TP: prezzo di acquisto IC è il principale rischio arm's length;
                metodo applicabile: Resale Price Method (RPM) o TNMM sul ROS
```

---

## FASE 3 — Output: Tabella Classificata

**Header obbligatorio:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reporting Entity    : [nome società]
Tipo Entità         : [Distributore LRD / Produttore full-fledged / ecc.]
Settore ATECO       : [codice + descrizione]
Periodo             : [da] — [a]
Valuta reporting    : EUR
Supply chain IC     : Fornitori IC [%]  |  Clienti IC [%]
Parti correlate     : [lista fornita / "inferita da metadati"]
Piano dei conti     : [fornito / "standard OIC assunto"]
WHY Engine          : [attivo / inattivo]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Tabella principale:**

| Data       | Controparte    | Descrizione      | Importo | Val. | Equiv. EUR | Conto  | Label Conto        | Categoria     | Conf.    | Note / WHY |
|------------|----------------|------------------|---------|------|------------|--------|--------------------|---------------|----------|------------|
| 2026-01-15 | SubCo GmbH     | Acquisto merci   | 120.000 | EUR  | 120.000    | 680000 | Costi controllate  | **A — IC**    | 🟢 Alta  | Match lista + conto IC. [WHY: >80% COGS IC → LRD captive] |
| 2026-01-18 | Microsoft Corp | Office 365       | 1.200   | USD  | 1.108      | 614200 | Costi licenze sw   | **B — Terzi** | 🟢 Alta  | No match lista + conto terzi |
| 2026-01-20 | ACME Consulting| Advisory Q1      | 8.300   | EUR  | 8.300      | 614100 | Consulenze         | **[INCERTO]** | 🔴 Bassa | No match; conto neutro; verifica se è advisor del gruppo |
| 2026-02-01 | Alpha GmbH     | Management fee   | 25.000  | EUR  | 25.000     | 740000 | Mgmt fee IC        | **A — IC**    | 🟡 Media | No match lista ma label conto = IC. [WHY: verifica beneficio ricevuto] |

---

## FASE 4 — Guardrail Anti-Allucinazione

1. **Non classificare senza evidenza** — nessun segnale → `[INCERTO]`
2. **Non inventare** denominazioni, codici conto, VAT, tassi FX
3. **Segnali contrastanti → sempre `[INCERTO]`**, mai forzare la classificazione
4. **Analogia vietata:** "nome simile al gruppo" da solo non è sufficiente
5. Le righe `[INCERTO]` **entrano nel totale** e richiedono revisione manuale
6. **Tipo entità non dichiarato** → non applicare WHY Engine su conti ambigui
7. **Non inferire il tipo di entità** da una sola transazione — richiedere conferma

---

## FASE 5 — Quality Gate: Quadratura

```
Σ A — Infragruppo   alta confidenza   = €  ___________
Σ A — Infragruppo   media confidenza  = €  ___________
Σ B — Terzi         alta confidenza   = €  ___________
Σ B — Terzi         media confidenza  = €  ___________
Σ [INCERTO]                           = €  ___________
─────────────────────────────────────────────────────
TOTALE CLASSIFICATO                   = €  ___________
TOTALE INPUT (atteso)                 = €  ___________
DIFFERENZA                            = €  ___________  ← deve essere 0,00
```

Se DIFFERENZA ≠ 0 → emettere `[DISCREPANZA]` con indicazione del delta
e delle cause probabili: righe mancanti · FX rounding ±0,01% · duplicati.

---

## FASE 6 — Business Logic Validator

> **Novità v3.0.** A classificazione ultimata, verifica la coerenza tra i
> pattern IC risultanti e il profilo funzionale dichiarato in FASE 0-BIS.
> Emette `[FLAG TP]` con spiegazione e raccomandazione operativa.

**Formato report:**

```
REPORT DI COERENZA FUNZIONALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tipo entità dichiarato  : Distributore LRD
Periodo analizzato      : FY2025

CHECK 1 — Acquisti IC su COGS totale
  Atteso per LRD  : > 70%
  Rilevato        : 85%    ✅ Coerente

CHECK 2 — Ricavi IC su ricavi totali
  Atteso per LRD  : < 20%  (clienti prevalentemente terzi)
  Rilevato        : 12%    ✅ Coerente

CHECK 3 — Presenza costi R&D IC
  Atteso per LRD  : assente o trascurabile
  Rilevato        : € 45.000  (3,2% dei costi totali)
  → [FLAG TP] ⚠️  Costi R&D IC inattesi per un LRD.
    Un LRD non controlla funzioni DEMPE e non dovrebbe sopportare
    costi di R&D. Verificare se si tratta di fee per servizi tecnici
    o di un contributo DEMPE mal classificato.
    Impatto: possibile riqualifica parziale verso contract manufacturer.
    Raccomandazione: richiedere il contratto sottostante e verificare se
    il costo è pass-through o corrisponde a funzioni effettivamente svolte.

CHECK 4 — Gross Margin vs benchmark ATECO 46.90
  Atteso (IQR)    : 12%–28%   (fonte: BvD/Aida, FY2025)
  Rilevato        : 18,4%     ✅ Nel range interquartile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FLAG TP aperti   : 1  (verifica manuale richiesta)
CHECK superati   : 3/4
```

---

## Funzionalità Avanzate (su richiesta)

### A — Registrazioni di Elisione IFRS 10 / OIC 17

```
Dr.  Ricavi infragruppo  (A1 IC)   120.000 EUR
 Cr. Costi infragruppo   (B6 IC)              120.000 EUR
[Elisione IC — SubCo GmbH → Holding SpA — FY2026 — Acquisto merci]
```

### B — Riepilogo per Tipologia Transazione

```
Acquisti prodotti IC   : €  720.000  (6 transazioni)  ← B6 IC
Management fees IC     : €   75.000  (3 transazioni)  ← 7400xx
Royalty IC             : €  120.000  (2 transazioni)  ← 7400xx
Finanziamenti IC       : €  500.000  (1 transazione)  ← 8000xx
IT Recharge IC         : €   50.000  (1 transazione)  ← 5800xx
```

### C — Summary Statistics + TP Exposure Index

```
── RIEPILOGO ──────────────────────────────────────────
Transazioni totali     : 47
  A — Infragruppo      : 18  (38,3%)  →  € 1.240.000
    di cui alta conf.  : 14           →  € 1.180.000
    di cui media conf. :  4           →  €    60.000
  B — Terzi            : 25  (53,2%)  →  €   892.500
  [INCERTO]            :  4  ( 8,5%)  →  €    67.300
───────────────────────────────────────────────────────
TOTALE                 : 47  (100%)   →  € 2.199.800
QUADRATURA             : ✅ OK  (diff. = € 0,00)

── TP EXPOSURE INDEX ──────────────────────────────────
IC / Totale transazioni      : 56,4%
IC acquisti / COGS           : 85,0%  →  [FLAG: LRD captive]
IC ricavi / Ricavi totali    : 12,0%  →  ✅ OK
Management fee / EBIT        : 28,0%  →  [FLAG: verifica deducibilità]
───────────────────────────────────────────────────────
```

---

## Scenari di Test Validati

| Test | Scenario | Output Atteso | Status |
|------|----------|---------------|--------|
| T1  | Lista parti correlate + conto IC         | A alta confidenza              | ✅ |
| T2  | Nessuna lista + conto IC-dedicato        | A media confidenza             | ✅ |
| T3  | Lista fornita + conto neutro             | A media confidenza             | ✅ |
| T4  | Nessuna lista + conto terzi              | B media confidenza             | ✅ |
| T5  | Segnali contrastanti IC/Terzi            | [INCERTO] + nota               | ✅ |
| T6  | Multi-valuta EUR/USD/GBP                 | Equiv. EUR tasso ECB           | ✅ |
| T7  | Totali non quadrano                      | [DISCREPANZA] + cause          | ✅ |
| T8  | Dati incompleti                          | [INCERTO] senza inventare      | ✅ |
| T9  | Distributore con costi R&D IC            | [FLAG TP] + spiegazione        | ✅ |
| T10 | Produttore senza personale               | [FLAG TP] hollow entity        | ✅ |
| T11 | LRD con ricavi IC > 50%                  | [FLAG TP] riclassifica profilo | ✅ |
| T12 | GM fuori range IQR settore               | [FLAG TP] + margine atteso     | ✅ |

---

## Conformità Normativa

| Standard                     | Ambito                                  | Copertura nella skill     |
|------------------------------|-----------------------------------------|---------------------------|
| OCSE BEPS Action 8-10        | Funzioni, rischi, asset (DEMPE)         | Fase 1-BIS, Fase 6        |
| OCSE BEPS Action 13          | Master/Local File documentation         | Audit trail output        |
| OCSE TPG 2022 §1.36–1.106    | Delineazione della transazione          | Fase 0-BIS, Fase 6        |
| IAS 24                       | Related Party Disclosures               | Fase 1 – Fase 2           |
| IFRS 10 / OIC 17             | Elisioni bilancio consolidato           | Funzionalità A            |
| OIC 24                       | Parti correlate bilancio italiano       | Codici 16x / 26x          |
| Art. 110 c.7 TUIR            | Documentazione TP italiana              | Output completo           |
| D.M. 14 maggio 2018          | Contenuto Local File italiano           | Fase 0-BIS, Fase 6        |
| Provv. AdE 360494/2020       | Requisiti documentali TP                | Header output             |
| Circ. 15/E 2021 + 16/E 2022  | Interpretazione AdE su documentazione  | Guardrail Fase 4          |

---

## Vincoli

1. Output **solo strutturato** — nessuna narrativa non richiesta
2. Non classificare senza almeno un segnale (controparte **o** conto)
3. Non inventare VAT, codici conto, tassi FX, denominazioni
4. Segnali contrastanti → sempre `[INCERTO]`, mai forzare
5. Input malformato → chiedere chiarimento prima di procedere
6. Non inferire il tipo di entità da singole transazioni — richiedere conferma
7. WHY Engine: solo ragionamento fondato su segnali presenti nei dati

---

## Note di Upgrade (v2.0 → v3.0)

| Feature                                    | v2.0 | v3.0 |
|--------------------------------------------|------|------|
| Classificazione IC / Terzi                 | ✅   | ✅   |
| Dual-signal (controparte + CoGe)           | ✅   | ✅   |
| Quality gate quadratura                    | ✅   | ✅   |
| Business Context Engine (FASE 0-BIS)       | ❌   | ✅   |
| Functional Profile Mapper (5 profili)      | ❌   | ✅   |
| WHY Engine (spiegazione per conto)         | ❌   | ✅   |
| Business Logic Validator (FASE 6)          | ❌   | ✅   |
| TP Exposure Index                          | ❌   | ✅   |
| FLAG TP per anomalie funzionali            | ❌   | ✅   |
| Confronto GM vs benchmark ATECO            | ❌   | ✅   |
| Supply chain analysis (% IC)              | ❌   | ✅   |
| Scenari di test                            | 8    | 12   |

---

*Skill v3.0.0 — Transfer Pricing & International Tax*
*Studio Biscozzi Nobili & Partners — Transfer Pricing Dept. — Marzo 2026*
*Compatibile con: Claude Code (SKILL.md) · Claude Projects · prompt diretto*
