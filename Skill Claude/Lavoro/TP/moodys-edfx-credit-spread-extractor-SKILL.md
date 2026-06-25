---
name: moodys-edfx-credit-spread-extractor
description: >
  Skill definitiva per estrarre credit spread da Moody's Analytics EDF-X in modo
  autenticato, verificabile, auditabile e difendibile. Usala quando l'utente
  chiede credit spread, curve/spread per rating, currency, reference curve,
  government bonds, tenori o date specifiche da EDF-X, oppure vuole trasformare
  una richiesta puntuale in un workflow scalabile con request lock, output table,
  QA ed evidence manifest. La skill NON deve inventare valori numerici: se il dato
  non è esportato o letto in modo verificabile da EDF-X, blocca con
  DATA_NOT_EXTRACTED.
version: 1.0-definitive
language: it
risk: controlled
mode: browser-agentic + export-first + QA-gated
---

# Moody's EDF-X Credit Spread Extractor

## Missione

Estrarre credit spread da **Moody's Analytics EDF-X** senza inventare valori numerici,
con workflow ripetibile, verificabile e difendibile per:

- documentazione TP
- benchmarking interno
- analisi controllate
- output tabellari auditabili

Questa skill mette **EDF-X al centro**. Non è un benchmark hub generico.

---

## Regola madre

**NON inventare mai valori numerici.**

Se il dato non è stato:
- esportato da **Moody's Analytics EDF-X**, oppure
- letto in modo verificabile dal DOM/UI della piattaforma

allora il risultato deve essere:

```text
BLOCK / DATA_NOT_EXTRACTED
```

Se una data non è lavorativa e EDF-X non restituisce un valore esatto, non sostituire
mai la data in modo implicito: serve una **business day policy** dichiarata.

---

## Quando usare questa skill

Usa questa skill quando servono credit spread EDF-X con parametri specifici come:

- rating agency
- rating / notch
- currency
- reference curve / benchmark
- instrument type
- tenor(s)
- date di osservazione
- unità di output (es. bps)

Attivala anche quando l'utente non cita esplicitamente il nome della skill ma scrive
richieste del tipo:

- "mi servono i credit spread EDF-X per rating Baa3 EUR gov bonds"
- "costruiscimi un workflow per estrarre credit spread da Moody's"
- "voglio una tabella con spread 3Y 4Y 5Y da EDF-X"
- "trasforma questa richiesta TP in una skill auditabile"

---

## Quando NON usarla

Non usare questa skill se:

- il dato richiesto non proviene da **Moody's Analytics EDF-X**
- l'utente vuole valori simulati, proxy o stime non verificabili
- non serve audit trail / difendibilità
- l'obiettivo è un confronto teorico o di mercato senza passare da EDF-X

---

## Mente locale obbligatoria prima di operare

Prima di eseguire, fai sempre una mini-fase di reasoning strutturato:

### 1. Focus
Individua il centro della richiesta:
- estrazione puntuale?
- workflow scalabile?
- template TP?
- QA / difendibilità?

### 2. Parametri critici
Identifica i campi che non possono essere sbagliati:
- rating agency
- rating
- currency
- reference instrument / curve
- tenori
- date
- unità output
- interpolation policy
- business day policy

### 3. Rischio nascosto
Verifica il rischio maggiore:
- valori inventati
- selettori UI errati
- curva/reference diversa
- date non lavorative gestite male
- export parziale

### 4. Strategia
Scegli il percorso:
1. export nativo EDF-X (preferito)
2. export tabellare UI
3. fallback DOM grid extraction
4. blocco hard se niente è verificabile

---

## Input canonico: REQUEST_LOCK

Ogni esecuzione deve partire da un payload lockato come questo:

```json
{
  "platform": "Moody's Analytics EDF-X",
  "metric": "credit_spread",
  "rating_agency": "",
  "rating": "",
  "currency": "",
  "reference_instrument": "",
  "instrument_type": "",
  "tenors_years": [],
  "dates": [],
  "output_unit": "bps",
  "interpolation_policy": "platform_default_or_reported",
  "business_day_policy": "exact_only",
  "status": "LOCKED_NOT_EXTRACTED"
}
```

### Regola
Nessuna estrazione parte senza REQUEST_LOCK.

Se il lock manca:

```text
BLOCK / PRECONDITION_FAILED
```

---

## Workflow operativo

## Step 1 — Preconditions

Verifica:
- accesso autorizzato a **Moody's Analytics EDF-X**
- sessione autenticata / SSO / MFA disponibile
- REQUEST_LOCK presente
- output path disponibile
- policy calendario definita

Se un prerequisito manca:

```text
BLOCK / PRECONDITION_FAILED
```

---

## Step 2 — Login e navigazione

1. Apri **Moody's Analytics EDF-X**
2. Accedi con la sessione utente
3. Raggiungi il modulo corretto per credit spreads / curves
4. Verifica che il modulo esposto sia coerente con la richiesta

Se il modulo non è raggiungibile:

```text
BLOCK / MODULE_NOT_REACHED
```

---

## Step 3 — Lock parametri in UI

Imposta e verifica tutti i campi critici:

- rating agency
- rating
- currency
- reference curve / benchmark
- instrument type
- tenors
- dates
- output unit

### Doppia verifica obbligatoria
Ogni parametro critico va verificato due volte:
1. prima della query
2. prima dell'export / cattura

Se un parametro differisce dal REQUEST_LOCK:

```text
BLOCK / PARAMETER_MISMATCH
```

---

## Step 4 — Estrazione

Ordine di preferenza:

### 4.1 Export ufficiale
Preferisci:
- CSV
- XLSX
- export nativo tabellare

### 4.2 Export UI
Se non esiste export file, usa export tabellare della UI se disponibile.

### 4.3 Fallback DOM
Se non esiste export, usa la lettura della grid DOM/UI con queste regole:
- esegui doppia lettura dei campi critici
- salva screenshot o hash dell'evidenza
- marca il metodo come `dom_grid_extraction`

### 4.4 Ultima ratio
Se nessun metodo è verificabile:

```text
BLOCK / DATA_NOT_EXTRACTED
```

---

## Step 5 — Normalizzazione output

Produci due forme di output:

### Wide table

```text
Date | Rating | Currency | Reference | 3Y spread bps | 4Y spread bps | 5Y spread bps | Source | Status
```

### Long table

```text
Date | Rating | Currency | Reference | TenorYears | SpreadBps | Source | ExtractionMethod | Status
```

### Regole di normalizzazione
- nessun arrotondamento non dichiarato
- preserva l'unità dell'output
- non interpolare fuori policy
- mantieni lo spelling EDF-X o normalizza dichiarando alias

---

## Step 6 — QA Extraction Gate

Esegui i controlli minimi:

- tutte le date richieste presenti
- tutti i tenori richiesti presenti
- rating coerente
- currency coerente
- reference coerente
- unità coerente
- nessun placeholder “falso numero”
- nessun duplicato inatteso
- nessun buco non dichiarato

Se una verifica fallisce:

```text
BLOCK / QA_FAILED
```

---

## Step 7 — TP Defensibility Gate

Produci e verifica le evidenze minime:

- REQUEST_LOCK
- extraction timestamp UTC
- extraction method
- platform name
- export file hash oppure DOM snapshot hash
- business day policy
- interpolation policy
- eventuali warning
- note su assenza del dato

Se l'evidenza non basta per l'uso TP:

```text
FLAG / NOT_DEFENSIBLE_FOR_TP
```

---

## Step 8 — Output finale

Genera sempre questi artefatti:

1. `Moodys_EDFX_Request_LOCK.json`
2. `Moodys_EDFX_Output_Template.csv` oppure `Moodys_EDFX_Output_Filled.csv`
3. `Moodys_EDFX_QA.json`
4. `Moodys_EDFX_Evidence_Manifest.json`

---

## Stati ammessi

Usa solo questi stati:

- `LOCKED_NOT_EXTRACTED`
- `EXTRACTED_UNVERIFIED`
- `EXTRACTED_QA_PASS`
- `EXTRACTED_QA_FAIL`
- `BLOCK_DATA_NOT_EXTRACTED`
- `BLOCK_PARAMETER_MISMATCH`
- `BLOCK_PRECONDITION_FAILED`
- `BLOCK_MODULE_NOT_REACHED`
- `FLAG_NOT_DEFENSIBLE_FOR_TP`

---

## Business day policy

Mai sostituire tacitamente una data non lavorativa.

Valori ammessi:
- `exact_only`
- `nearest_previous_business_day`
- `nearest_next_business_day`
- `platform_default_reported`

La policy usata deve comparire nell'output e nella QA.

---

## Error handling

Ogni errore deve contenere:
- `step`
- `reason_code`
- `user_action_required`
- `retry_safe`

Esempio:

```json
{
  "step": "step_4_extraction",
  "reason_code": "DATA_NOT_EXTRACTED",
  "user_action_required": "verify EDF-X module access or export availability",
  "retry_safe": true
}
```

---

## HA / Resilience

Se la skill viene operationalizzata in pipeline:

- retry su transient UI/load failure
- exponential backoff con jitter
- circuit breaker su selector drift
- parser versioning
- fallback export → DOM
- structured logging
- run_id per correlazione
- evidence retention controllata
- rollback parser/version

### Health checks suggeriti
- modulo raggiungibile
- export disponibile
- selector drift check
- output path scrivibile
- QA engine attivo

---

## Sicurezza

- non salvare credenziali in chiaro
- non loggare token/session cookie
- least privilege
- no dati sensibili nei log
- export custoditi in path autorizzato
- hash sui file di evidenza

---

## Workaround smart policy

### Workaround pragmatico
**Cosa facciamo ora:**
- costruiamo lock, template, workflow, QA ed evidence manifest
- non popoliamo valori se EDF-X non è accessibile in modo verificabile

**Perché funziona:**
- evita valori inventati
- rende il processo scalabile e replicabile
- prepara la run operativa per chi ha accesso

**Limite:**
- senza accesso autenticato EDF-X non restituisce numeri finali

**Rischio residuo:**
- errore umano nella selezione della curva o del modulo

**Evoluzione verso soluzione definitiva:**
- parser automation
- selector regression tests
- validazione end-to-end
- pipeline con monitoring e rollback

---

## Acceptance criteria

La skill è valida solo se:

1. i parametri sono lockati
2. il dato proviene davvero da EDF-X
3. l'output è tabellare e coerente
4. la QA passa
5. il bundle di evidenze è completo

Se anche uno solo di questi punti manca, la skill non deve far finta che il dato sia pronto.

---

## Output template raccomandato

### Request lock di esempio

```json
{
  "platform": "Moody's Analytics EDF-X",
  "metric": "credit_spread",
  "rating_agency": "Moody's",
  "rating": "Baa3",
  "currency": "EUR",
  "reference_instrument": "government bonds",
  "instrument_type": "corporate",
  "tenors_years": [3, 4, 5],
  "dates": [
    "2025-01-01",
    "2025-03-31",
    "2025-06-30",
    "2025-09-30",
    "2025-12-31"
  ],
  "output_unit": "bps",
  "interpolation_policy": "platform_default_or_reported",
  "business_day_policy": "exact_only",
  "status": "LOCKED_NOT_EXTRACTED"
}
```

### Output CSV di esempio

```csv
Date,Rating,Currency,Reference,3Y spread bps,4Y spread bps,5Y spread bps,Source,Status
2025-01-01,Baa3,EUR,Government bonds,DATA_REQUIRED,DATA_REQUIRED,DATA_REQUIRED,Moody's Analytics EDF-X,authenticated extraction required
2025-03-31,Baa3,EUR,Government bonds,DATA_REQUIRED,DATA_REQUIRED,DATA_REQUIRED,Moody's Analytics EDF-X,authenticated extraction required
2025-06-30,Baa3,EUR,Government bonds,DATA_REQUIRED,DATA_REQUIRED,DATA_REQUIRED,Moody's Analytics EDF-X,authenticated extraction required
2025-09-30,Baa3,EUR,Government bonds,DATA_REQUIRED,DATA_REQUIRED,DATA_REQUIRED,Moody's Analytics EDF-X,authenticated extraction required
2025-12-31,Baa3,EUR,Government bonds,DATA_REQUIRED,DATA_REQUIRED,DATA_REQUIRED,Moody's Analytics EDF-X,authenticated extraction required
```

---

## Note di design

Questa skill è scritta seguendo il principio corretto di creazione skill:
- cattura dell'intento
- parametri ed edge cases chiariti prima
- output definito
- trigger descrittivo e “pushy” quanto basta
- workflow ripetibile
- spazio per eval e miglioramenti futuri

La logica è allineata al ruolo di una skill ben costruita: capire che cosa l'utente vuole ottenere, codificare il flusso, rafforzare il trigger e mantenere il comportamento verificabile. 

---

## Regola finale

Se non hai il dato da **Moody's Analytics EDF-X**, non riempire la tabella con numeri.

Scrivi sempre:

```text
DATA_REQUIRED / AUTHENTICATED_EXTRACTION_REQUIRED
```
