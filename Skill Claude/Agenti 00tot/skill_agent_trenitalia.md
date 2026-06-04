# 🚆 SKILL AGENT v5.1.1 — Rimborso Trenitalia (OTP + GDPR + Regional Attachment + lefrecce.it PDF Recovery + CAPTCHA Confirmation)
## Architecture: HA + Evaluator-Optimizer + Cross-Validation + MFA Resilience + Human-in-the-Loop CAPTCHA
**Owner:** Luca Consalter | **Tessera:** `036647537` | **Email:** `luca.consalter@gmail.com`  
**Version:** 5.1.1 | **Validated:** 2026-04-25 | **Patch:** lefrecce.it PDF Source, CAPTCHA pagina 6/6 confirmed  
**SoT (Source of Truth):** trenitalia.com + viaggiatreno.it + trainstats.altervista.org + lefrecce.it

---

## 🎯 PHILOSOPHY (Principi Architetturali)
1. **Ground Truth First:** Nessuna richiesta senza verifica incrociata da ≥2 fonti indipendenti.
2. **Fail Forward:** Ogni errore attiva un fallback predefinito, mai uno stop.
3. **Evaluator-Optimizer:** Dopo ogni azione, un loop di validazione decide se procedere, retry o escalate.
4. **Transparency by Design:** Ogni decisione è loggata, tracciabile, reversibile.
5. **Human-in-the-Loop:** Checkpoint prima di azioni irreversibili (submit, email, ART, **CAPTCHA**).
6. **Pre-Flight Verification:** Ogni gate bloccante (OTP, allegato, consenso, CAPTCHA) viene pre-verificato prima di investire tempo nella compilazione.

---

## 🌐 GROUND TRUTH SOURCES (Fonti Verificate)

| Source | URL | Type | Reliability | Use Case |
|--------|-----|------|-------------|----------|
| **Trenitalia Official** | trenitalia.com/it/informazioni/ritardi | Primary | ★★★★★ | Ritardo ufficiale per PNR/numero treno |
| **ViaggiaTreno** | viaggiatreno.it | Primary | ★★★★★ | Stato reale treno, binario, ritardo in tempo reale e storico |
| **Smart Caring** | trenitalia.com/it/informazioni/smart-caring.html | Primary | ★★★★★ | Notifica push/email ufficiale Trenitalia (prova legale) |
| **TrainStats** | trainstats.altervista.org | Secondary | ★★★★☆ | Storico ritardi medi, classifiche regolarità, grafici |
| **Zugfinder** | zugfinder.net/it/start | Secondary | ★★★★☆ | Statistiche puntualità AV, posizione treni, ritardi passati |
| **App Trenitalia** | iOS/Android | Primary | ★★★★★ | "I miei viaggi" + ritardo registrato + check-in BDR |
| **lefrecce.it Purchases** | lefrecce.it/Channels.Website.WEB/#/user-area/purchases | Primary | ★★★★★ | **PDF biglietto recovery per allegato obbligatorio** |

**Cross-Validation Rule:** Per ritardi contestati o dubbi, l'agente DEVE verificare su **almeno 2 fonti** prima di procedere.

---

## 🧮 DECISION MATRIX v5.1.1 (Cross-Validated)

### Input Variables
```python
train_type = {"FRECCIA", "IC", "ICN", "REGIONALE"}
ticket_type = {"BDR", "BER", "TICKETLESS", "CARTACEO", "CARNET"}
delay_minutes = int >= 0
price_euro = float
payment_method = {"CARTA", "PAYPAL", "SATISPAY", "APPLE_PAY", "GOOGLE_PAY", "CONTANTI"}
is_checkin = bool
has_smart_caring = bool  # Notifica push/email Trenitalia
date_travel = date
source_verified = {"TRENITALIA", "VIAGGIATRENO", "SMART_CARING", "TRAINSTATS", "ZUGFINDER"}
```

### Algorithm
```python
def calculate_channel_and_percent():
    # GATE 0: Termine prescritto
    if today > date_travel + 365 days:
        return {"status": "EXPIRED", "action": "STOP"}

    # GATE 1: Soglia minima
    threshold = 4.0
    if price_euro < threshold:
        return {"status": "BELOW_THRESHOLD", "action": "STOP"}

    # GATE 2: Cross-validation ritardo
    if len(source_verified) < 1:
        return {"status": "NO_GROUND_TRUTH", "action": "VERIFY_FIRST"}

    # BDR AUTOMATIC DETECTION
    if ticket_type == "BDR" and is_checkin and payment_method != "CONTANTI":
        if delay_minutes > 60:
            return {
                "channel": "BDR_AUTO",
                "percent": 25 if delay_minutes < 120 else 50,
                "min_amount": 16 if delay_minutes < 120 else 8,
                "action": "MONITOR",
                "sla_days": 30
            }

    # FRECCIE / IC / ICN
    if train_type in {"FRECCIA", "IC", "ICN"}:
        if delay_minutes >= 30 and delay_minutes < 60:
            return {"channel": "APP_LEFRECCE", "percent": 25, "action": "SUBMIT"}
        elif delay_minutes >= 60 and delay_minutes < 120:
            return {"channel": "APP_LEFRECCE", "percent": 25, "action": "SUBMIT"}
        elif delay_minutes >= 120:
            return {"channel": "APP_LEFRECCE", "percent": 50, "action": "SUBMIT"}

    # REGIONALE MANUALE
    if train_type == "REGIONALE":
        if delay_minutes >= 60 and delay_minutes < 120:
            return {"channel": "APP_WEBFORM", "percent": 25, "action": "SUBMIT"}
        elif delay_minutes >= 120:
            return {"channel": "APP_WEBFORM", "percent": 50, "action": "SUBMIT"}

    # RINUNCIA / CANCELLAZIONE
    if motivation in {"CANCELLAZIONE", "RINUNCIA"}:
        return {"channel": "WEBFORM", "percent": 100, "action": "SUBMIT", "note": "Possibile trattenuta 20%"}

    return {"status": "NOT_ELIGIBLE", "action": "STOP"}
```

---

## 🛠️ TOOL DEFINITIONS (Agent-Computer Interface)

### Tool 1: `verify_delay_multi_source`
```yaml
description: "Verifica ritardo su multiple fonti per cross-validation"
parameters:
  train_number: string (es. "7636")
  date_travel: "DD/MM/YYYY"
  station_from: string
  station_to: string
sources:
  - name: "trenitalia_ritardi"
    url: "https://www.trenitalia.com/it/informazioni/ritardi"
    method: "INPUT train_number + date → EXTRACT delay_minutes"
  - name: "viaggiatreno"
    url: "http://www.viaggiatreno.it"
    method: "SEARCH train_number → EXTRACT stato, ritardo, binario"
  - name: "trainstats"
    url: "https://trainstats.altervista.org"
    method: "SEARCH train_number + date → EXTRACT storico ritardo medio"
  - name: "smart_caring_inbox"
    method: "SCAN gmail luca.consalter@gmail.com for 'Trenitalia' + 'ritardo' + train_number"
returns:
  delay_official: integer
  delay_confirmed_by: list[string]
  screenshot_paths: list[string]
  confidence: enum["HIGH" (2+ sources match), "MEDIUM" (1 source), "LOW" (0 sources)]
rules:
  - "Se confidence == LOW → STOP e richiedi verifica manuale"
  - "Se confidence == MEDIUM → procedi ma annota riserva"
  - "Se confidence == HIGH → procedi con massima priorità"
```

### Tool 2: `extract_ticket_data`
```yaml
description: "Estrae dati biglietto da Area Riservata Trenitalia"
parameters:
  login_method: "CartaFRECCIA"
  card_number: "036647537"
  password: "[VAULT]"
navigation:
  1: "https://www.trenitalia.com/it.html"
  2: "CLICK Area Riservata"
  3: "INPUT CartaFRECCIA: 036647537"
  4: "INPUT Password: [VAULT]"
  5: "CLICK I MIEI VIAGGI"
  6: "FILTER date_travel OR scroll last 12 months"
  7: "EXTRACT: pnr, train_number, station_from, station_to, time_scheduled, price, ticket_type"
returns:
  ticket_record: yaml structure (vedi Data Model)
  screenshot_path: string
validation:
  - "pnr MUST be 10-13 digits"
  - "price MUST be > 0"
  - "train_number MUST be numeric"
```

### Tool 2b: `download_ticket_pdf` (Nuovo v5.1.1)
```yaml
description: "Scarica PDF biglietto da Area Riservata lefrecce.it per allegato obbligatorio"
url: "https://www.lefrecce.it/Channels.Website.WEB/#/user-area/purchases"
parameters:
  login_method: "CartaFRECCIA"
  card_number: "036647537"
  password: "[VAULT]"
navigation:
  1: "https://www.lefrecce.it"
  2: "CLICK Area Riservata"
  3: "INPUT CartaFRECCIA: 036647537"
  4: "INPUT Password: [VAULT]"
  5: "NAVIGATE → user-area/purchases"
  6: "FILTER date_travel (DD/MM/YYYY) OR scroll"
  7: "LOCATE ticket by PNR/train_number"
  8: "CLICK 'Scarica PDF' / download icon"
returns:
  pdf_path: "string (local path, es. /artifacts/{pnr}_ticket_lefrecce_{timestamp}.pdf)"
  file_size_bytes: int
  status: enum["SUCCESS", "NOT_FOUND", "LOGIN_FAILED"]
validation:
  - "file_size_bytes MUST be > 10000"
  - "file MUST contain 'Trenitalia' OR 'CartaFRECCIA' in header (PDF text extract)"
rules:
  - "IF status == NOT_FOUND → FALLBACK to App Trenitalia (source_priority #1)"
  - "IF status == LOGIN_FAILED → TRIGGER KIR-005"
```

### Tool 3: `compile_webform_reclami`
```yaml
description: "Compila webform Trenitalia con validazione campi v5.1.1"
url: "https://reclami-e-suggerimenti.trenitalia.com/rimborsi/anagrafica.aspx"
parameters:
  anagrafica:
    nome: "Luca"
    cognome: "Consalter"
    data_nascita: "07/02/1987"
    luogo_nascita: "Torino"
    indirizzo: "Via Cola di Rienzo 8"
    cap: "20143"
    citta: "Milano"
    provincia: "MI"
    telefono: "[VAULT]"
    email: "luca.consalter@gmail.com"
    tessera: "036647537"
  viaggio:
    titolo_viaggio: "string (PNR/codice 10-13 cifre)"
    data_emissione: "DD/MM/YYYY"
    origine: "STAZIONE (DD/MM/YYYY HH:MM)"
    destinazione: "STAZIONE (DD/MM/YYYY HH:MM)"
    numero_treno: "string"
    data_viaggio: "DD/MM/YYYY"
  richiesta:
    canale_acquisto: enum["Sito Web", "App", "Biglietteria", "EMV", "Agenzia", "Altro"]
    motivazione: enum["Ritardo", "Cancellazione", "Rinuncia", "Soppressione"]
    metodo_pagamento_valido: bool
  consenso_gdpr:
    type: bool
    default: true
    description: "Spunta obbligatoria 'Do il consenso' per condivisione dati con terzi"
    rule: "MUST be true per procedere. Se il form presenta unchecked → CLICK e verifica."
  otp_handler:
    type: object
    properties:
      email_cartafreccia: "luca.consalter@gmail.com"
      otp_timeout_seconds: 120
      max_retry: 3
      spam_check: true
      fallback_access_area_riservata: "https://www.trenitalia.com/it.html"
  regional_attachment_gate:
    type: object
    condition: "train_type == 'REGIONALE'"
    properties:
      required: true
      accepted_formats: ["PDF", "JPG", "PNG"]
      max_size_mb: 3.5
      source_priority:
        - "PDF da lefrecce.it → user-area/purchases (FILTER by date) [v5.1.1]"
        - "PDF da App Trenitalia (I miei viaggi)"
        - "Screenshot biglietto digitale dall'app"
        - "Foto biglietto cartaceo (se applicabile)"
  captcha_handler:
    type: object
    description: "Gestione CAPTCHA pagina 6/6 INVIO RICHIESTA"
    properties:
      trigger_page: "6/6 INVIO RICHIESTA"
      type: "image + audio"
      human_required: true
      audio_bypass: "CLICK 'Ascolta codice di sicurezza' → human transcribes"
      refresh: "CLICK 'Aggiorna codice di sicurezza'"
  note: "string (max 1000 chars, MUST contain 'Reg. UE 2021/782')"
  allegati: "list[file] (PDF <3.5MB preferred)"
field_validation:
  - "Origine/Destinazione FORMAT: 'STAZIONE (GG/MM/AAAA HH:MM)' — es. 'TORINO PORTA SUSA (02/02/2026 18:05)'"
  - "Note MUST include: Reg. UE 2021/782, nome, tessera, email"
  - "Consent: checkbox 'Do il consenso' MUST be checked before submit"
  - "IF train_type == REGIONALE → allegato MUST be present (PDF/JPG/PNG <3.5MB)"
  - "IF allegati upload FAILS OR missing for REGIONALE → complete WITHOUT attachments, SAVE protocol, TRIGGER CH-5 Email fallback with attachment"
  - "CAPTCHA: IF pagina 6/6 presenta 'Codice di Sicurezza' → human-in-the-loop attivato"
returns:
  protocollo: "string (es. RIF. 2026/XXXXX)"
  status: enum["SUCCESS", "PARTIAL", "FAILED"]
  allegati_fallback: bool
  otp_status: enum["VERIFIED", "FAILED", "BYPASSED"]
  captcha_status: enum["SOLVED", "HUMAN_REQUIRED", "BYPASSED"]
```

### Tool 4: `send_email_escalation`
```yaml
description: "Invia email a Customer Care con allegati e riferimento protocollo"
to: "customer.service.regionale@trenitalia.it"
subject: "Re: Richiesta indennizzo rimborso - Treno {numero} del {data} - Tessera 036647537"
body_template: "TPL-2 (Email Completa) dalla Templates Library"
attachments:
  - "screenshot_ticket"
  - "screenshot_delay"
  - "original_notification_email (if exists)"
conditional:
  - "IF protocollo exists → CITE in first paragraph"
  - "IF allegati_fallback == TRUE → explain in email: 'Completato webform senza allegati per errore tecnico noto (KIR-001). Allego ora documentazione.'"
  - "IF otp_failed == TRUE → explain in email: 'Verifica OTP non ricevuta dopo 3 tentativi (KIR-011). Richiedo gestione manuale.'"
  - "IF captcha_blocked == TRUE → explain in email: 'Webform bloccato a pagina 6/6 per CAPTCHA non risolvibile (KIR-006). Richiedo gestione manuale via email.'"
returns:
  sent: bool
  timestamp: ISO8601
  confirmation_screenshot: string
```

### Tool 5: `generate_report`
```yaml
description: "Genera report finale markdown con tutti i ticket processati"
output_file: "rimborsi_luca_{data}.md"
content:
  - summary: "N treni, M eleggibili, P protocolli"
  - ticket_table: "| PNR | Treno | Data | Ritardo | % | Canale | Protocollo | Status |"
  - ground_truth_log: "| Fonte | Ritardo | Screenshot |"
  - known_issues: "| KIR-ID | Descrizione | Risoluzione |"
  - next_actions: "| Data | Azione | Canale |"
```

---

## 🔄 EVALUATOR-OPTIMIZER LOOP (Self-Consistency)

Dopo OGNI step critico, l'agente esegue questo loop:

```
STEP N → ACTION → EVALUATE → DECISION
                    │
                    ├─ PASS → Proceed to STEP N+1
                    │
                    ├─ FAIL_RETRY → Adjust params → Retry STEP N (max 3)
                    │
                    └─ FAIL_ESCALATE → Switch to fallback channel
```

### Evaluator Checks

#### EV-1: Post-Data Collection
```
□ PNR length 10-13 chars?
□ Price > €4?
□ Delay ≥ threshold (60min Regionale/IC, 30min Frecce)?
□ Date within 1 year?
□ Cross-validation confidence ≥ MEDIUM?
```
**Fail Retry:** Re-extract from Area Riservata.  
**Fail Escalate:** Ask user for manual input.

#### EV-2: Pre-Submit (v5.1.1)
```
□ All required fields populated?
□ Date format DD/MM/YYYY HH:MM correct?
□ Note contains "Reg. UE 2021/782"?
□ Erogazione = ACCREDITO CARTA (not bonus)?
□ Allegati size < 3.5MB (if present)?
□ CONSENT: "Do il consenso" is checked?
□ REGIONAL GATE: IF train_type==REGIONALE → allegato present OR fallback email ready?
□ OTP-READY: Email CartaFRECCIA accessible and spam folder checked?
□ CAPTCHA: IF pagina 6/6 presenta "Codice di Sicurezza" → human-in-the-loop attivato?
```
**Fail Retry:** Fix formatting, attach file, check consent, resend OTP.  
**Fail Escalate:** Skip to CH-5 Email with explanation + full attachments.

#### EV-3: Post-Submit
```
□ Protocol number visible on confirmation page?
□ Confirmation email received (check inbox)?
□ Screenshot saved with correct naming?
```
**Fail Retry:** Check email inbox for protocol.  
**Fail Escalate:** Contact call center 199892021.

#### EV-4: Post-Email
```
□ Email sent confirmation (screenshot)?
□ No bounce-back within 1 hour?
□ Allegati attached correctly?
```
**Fail Retry:** Resend email.  
**Fail Escalate:** ART after 30 days silence.

#### EV-OTP: OTP Verification Gate
```
□ OTP email arrived within 120s?
□ OTP code valid and not expired?
□ Submit confirmed after OTP?
```
**Fail Retry (max 3):** "INVIA NUOVO OTP"  
**Fail Escalate:** CH-5 Email fallback (bypass OTP)  
**Fail Escalate (email wrong):** STOP → Area Riservata → update email → restart CH-4

#### EV-CAPTCHA: CAPTCHA Gate (Nuovo v5.1.1)
```
□ CAPTCHA image loaded and readable?
□ Human input received within 60s?
□ Submit confirmed after CAPTCHA?
```
**Fail Retry:** "Aggiorna codice di sicurezza"  
**Fail Escalate (human unavailable):** STOP webform, TRIGGER CH-5 Email (bypass CAPTCHA)  
**Fail Escalate (audio available):** "Ascolta codice di sicurezza" → human transcribes

---

## 🐛 KNOWN ISSUES REGISTRY v5.1.1 (KIR)

| ID | Issue | Trigger | Impact | Workaround | Probability | Detection |
|----|-------|---------|--------|------------|-------------|-----------|
| KIR-001 | Upload allegati fallisce | Webform Step 4.8 | Alto | Completa senza allegati → CH-5 Email | 40% | EV-2 |
| KIR-002 | "Viaggio non trovato" | Area Riservata | Medio | Attendi 48h; cerca "I MIEI ACQUISTI" | 15% | EV-1 |
| KIR-003 | Ritardo 0 min su trenitalia.com | trenitalia.com/ritardi | Medio | Cross-check ViaggiaTreno + TrainStats | 10% | EV-1 |
| KIR-004 | No button Indennizzo | App/Sito | Medio | Webform diretto (CH-4) | 20% | EV-2 |
| KIR-005 | Login fallito | Credenziali | Alto | Recupero password via SMS/email | 5% | EV-0 |
| **KIR-006** | **CAPTCHA pagina 6/6** | **INVIO RICHIESTA** | **Alto** | **HUMAN-IN-THE-LOOP: input manuale caratteri. AUDIO: 'Ascolta codice'. Se human unavailable → CH-5 Email** | **100%** | **EV-CAPTCHA** |
| KIR-007 | BDR non automatico | Check-in mancato | Medio | Webform manuale + spiegazione | 10% | EV-1 |
| KIR-008 | Obliterazione mancante | Cartaceo | Alto | Nota in webform + foto se possibile | 15% | EV-1 |
| KIR-009 | Smart Caring non ricevuto | Notifica mancata | Basso | Verifica spam + usa ViaggiaTreno come prova | 8% | EV-1 |
| KIR-010 | TrainStats non trova treno | Treno non tracciato | Basso | Usa solo Trenitalia + ViaggiaTreno | 5% | EV-1 |
| KIR-011 | OTP non ricevuto / scaduto | Pagina verifica OTP | Alto | 1) Controlla spam 2) INVIA NUOVO OTP (max 3x) 3) Se fallisce → CH-5 Email fallback | 15% | EV-OTP |
| **KIR-012** | **Allegato obbligatorio Regionale mancante** | **Step 4.8** | **Alto** | **1) lefrecce.it → purchases → filtra per data → scarica PDF [v5.1.1] 2) App Trenitalia 3) Screenshot 4) CH-5 Email** | **25%** | **EV-2** |
| KIR-013 | Email CartaFRECCIA errata / inaccessibile | OTP page | Alto | STOP flusso. Accedi Area Riservata → aggiorna email → riavvia CH-4. Non bypassabile. | 5% | EV-OTP |

---

## 🛤️ CHANNEL PROCEDURES v5.1.1

### CH-0: GROUND TRUTH VERIFICATION (Pre-step obbligatorio)
**Prima di qualsiasi azione, verifica il ritardo su ≥1 fonte.**

```
1. SOURCE A (Primaria): trenitalia.com/it/informazioni/ritardi
   → INPUT: train_number + date_travel
   → OUTPUT: delay_minutes_A, screenshot_A

2. SOURCE B (Primaria): viaggiatreno.it
   → INPUT: train_number OR station_from + station_to + time
   → OUTPUT: delay_minutes_B, stato_treno_B, screenshot_B

3. SOURCE C (Secondaria, opzionale): trainstats.altervista.org
   → INPUT: train_number + date_travel
   → OUTPUT: delay_storico_C, grafico_C, screenshot_C

4. SOURCE D (Smart Caring): Scan inbox luca.consalter@gmail.com
   → SEARCH: "Trenitalia" + "ritardo" + train_number + date_travel
   → OUTPUT: notification_email_D, screenshot_D

5. CROSS-VALIDATION:
   IF delay_minutes_A == delay_minutes_B (±5 min):
      → confidence = HIGH
   ELSE IF only one source available:
      → confidence = MEDIUM
   ELSE:
      → confidence = LOW → STOP, richiedi verifica manuale

6. SAVE: artifacts/{pnr}_groundtruth_{timestamp}.png (collage screenshot)
```

### CH-1: BDR AUTOMATICO
**Pre-conditions:** `ticket_type == BDR AND is_checkin == TRUE AND payment != CONTANTI`  
**SLA:** 30 gg  
**Action:** Nessuna. Solo monitoraggio.

### CH-2: APP / AREA RISERVATA
**Pre-conditions:** `confidence >= MEDIUM AND ticket_type in {TICKETLESS, BDR_NON_AUTO}`  
**Procedure:** Come v5.0, con EV-2 pre-submit e EV-3 post-submit.

### CH-3: LeFrecce.it
**Pre-conditions:** `train_type in {FRECCIA, IC, ICN}`  
**Procedure:** Come v5.0.

### CH-4: WEBFORM RECLAMI (Aggiornato v5.1.1)
**Pre-conditions:** `CH-2/3 falliti OR ticket_type in {CARTACEO, BER, TICKETLESS_REGIONALE}`  
**URL:** `https://reclami-e-suggerimenti.trenitalia.com/rimborsi/anagrafica.aspx`

#### Step-by-Step

**Step 4.1–4.6** *(Anagrafica, Viaggio, Richiesta, Note)* → *Invariati*

**Step 4.7 — GDPR CONSENT GATE**
```
LOCATE: checkbox "Do il consenso" (Par. III Finalità del trattamento)
ACTION: CLICK checkbox
VERIFY: checkbox state == checked
IF unchecked AND disabled → LOG "Consent gate blocked" → TRIGGER KIR-012
```

**Step 4.8 — REGIONAL ATTACHMENT GATE (v5.1.1)**
```
IF train_type == "REGIONALE":

  ATTEMPT 1: lefrecce.it PDF Recovery [Nuovo v5.1.1]
    → OPEN lefrecce.it in new tab
    → LOGIN with CartaFRECCIA 036647537 + [VAULT]
    → NAVIGATE user-area/purchases
    → FILTER date_travel = DD/MM/YYYY
    → LOCATE PNR / Train number
    → CLICK download PDF
    → VERIFY file_size > 10KB
    → IF SUCCESS → UPLOAD to webform via "SFOGLIA" → "AGGIUNGI FILE"

  ATTEMPT 2: App Trenitalia (Fallback)
    → OPEN App Trenitalia → "I miei viaggi"
    → LOCATE ticket by date
    → SHARE/EXPORT as PDF
    → UPLOAD to webform

  ATTEMPT 3: Screenshot (Last resort)
    → Screenshot biglietto digitale
    → SAVE as JPG/PNG <3.5MB
    → UPLOAD to webform

  IF ALL ATTEMPTS FAIL:
    → TRIGGER KIR-012
    → LOG "Attachment recovery failed after 3 sources"
    → PROCEED to submit WITHOUT attachment (if button allows)
    → IF button blocked → STOP webform, TRIGGER CH-5 Email with manual attachment
```

**Step 4.9 — PRE-SUBMIT OTP READINESS**
```
ACTION: BEFORE clicking "Prosegui con la Richiesta":
  1. OPEN gmail/luca.consalter@gmail.com in secondary tab
  2. VERIFY inbox accessible and not full
  3. CHECK spam folder pre-emptively (clear if needed)
  4. NOTE: OTP will be sent to CartaFRECCIA-associated email
```

**Step 4.10 — SUBMIT & OTP LOOP**
```
ACTION: CLICK "Prosegui con la Richiesta"
EXPECTED: Redirect to OTP verification page ("Inserisci codice OTP")

OTP LOOP (Evaluator EV-OTP):
  WAIT: max 60s for email arrival
  IF email received:
    → EXTRACT OTP (6 digits typically)
    → INPUT OTP in form
    → CLICK "Conferma"
  ELSE IF no email AND retry_count < 3:
    → CLICK "INVIA NUOVO OTP"
    → WAIT 60s
    → retry_count++
    → LOOP
  ELSE IF no email after 3 retries:
    → TRIGGER KIR-011
    → CHECK spam folder again
    → IF email_cartafreccia incorrect → STOP, redirect to Area Riservata to update email
    → ELSE → TRIGGER CH-5 Email fallback (bypass OTP entirely)
```

**Step 4.11 — CAPTCHA GATE (Nuovo v5.1.1)**
```
EXPECTED: Pagina 6/6 INVIO RICHIESTA con campo "Codice di Sicurezza"
LOCATE: image CAPTCHA + "Aggiorna codice di sicurezza" + "Ascolta codice di sicurezza"

ACTION:
  1. SCREENSHOT captcha image → save as {pnr}_captcha_{timestamp}.png
  2. PRESENT to human operator: "Inserisci i caratteri del CAPTCHA"
  3. IF human responds within 60s:
       → INPUT characters in field
       → CLICK "Invia"
  4. ELSE IF human unavailable AND audio available:
       → CLICK "Ascolta codice di sicurezza"
       → HUMAN transcribes audio
       → INPUT characters
  5. ELSE:
       → TRIGGER KIR-006
       → STOP webform
       → TRIGGER CH-5 Email fallback (bypass CAPTCHA)

EVALUATOR EV-CAPTCHA:
  IF submit accepted → PASS
  IF "Codice errato" → CLICK "Aggiorna codice di sicurezza" → retry (max 3)
  IF still failing → TRIGGER CH-5 Email
```

**Step 4.12 — POST-SUBMIT CONFIRMATION**
```
CHECK: Protocol number visible?
CHECK: Confirmation email received?
SAVE: screenshot as {PNR}_webform_prot_{timestamp}.png
```

### CH-5: EMAIL CUSTOMER CARE
**To:** `customer.service.regionale@trenitalia.it`  
**Subject:** `Re: Richiesta indennizzo - Treno {numero} del {data} - Tessera 036647537`  
**Template:** TPL-2 (vedi sotto).

### CH-6: CALL CENTER
**Number:** `199892021`  
**Script:** TPL-3 (vedi sotto).

### CH-7: POSTA / MODULO EUROPEO
**Address:** `Trenitalia S.p.A, Ufficio Reclami e Rimborsi, Piazza della Croce Rossa 1, 00161 Roma`

### CH-8: ART ESCALATION
**URL:** `https://www.autorita-trasporti.it`

---

## 📚 TEMPLATES LIBRARY v5.1.1

### TPL-1: Webform Note (1000 chars, ottimizzato per parsing automatico)
```
[CONTESTO] Spett.le Customer Care Regionale Trenitalia, presento formale
richiesta indennizzo ex Reg. UE 2021/782 per disservizio in data [DATA].
[DATI] Treno [TIPO] [NUMERO] tratta [DA]-[A]. Ritardo confermato: [XX] min
(fonti: Trenitalia + ViaggiaTreno). PNR: [XXXXX]. Importo: EUR[XX,XX].
[NORMATIVA] Ai sensi art. 17 Reg. UE 2021/782 e CGT, richiedo indennita
[25%/50%/100%].
[ANAGRAFICA] Luca Consalter, Tessera 036647537, luca.consalter@gmail.com,
Via Cola di Rienzo 8, 20143 Milano.
[ALLEGATI] Biglietto + screenshot ritardo + notifica Smart Caring (se disp).
[EROGAZIONE] Accredito carta. Grazie.
```

### TPL-2: Email Completa (Cross-Reference Ground Truth + v5.1.1 Fallback)
```
Spett.le Customer Care Regionale Trenitalia,

con la presente desidero presentare formale reclamo per il disservizio subito
in data [DATA], relativo alla [cancellazione/ritardo] del treno [TIPO] [NUMERO]
sulla tratta [PARTENZA] - [ARRIVO].

VERIFICA RITARDO (Ground Truth):
- Fonte primaria Trenitalia: ritardo confermato [XX] min
- Fonte secondaria ViaggiaTreno: ritardo confermato [XX] min
- [Eventuale: Smart Caring notification ricevuta alle ore HH:MM]

DATI VIAGGIO:
- Numero treno: [TIPO] [NUMERO]
- Data e ora prevista: [DATA], ore [HH:MM]
- Tratta: [PARTENZA] - [ARRIVO]
- Ritardo effettivo all'arrivo: [XX] minuti
- PNR / Codice biglietto: [XXXXX]
- Importo: EUR [XX,XX]

Ai sensi del Regolamento UE 2021/782 e CGT Trenitalia, richiedo
l'indennita del [25%/50%/100%].

DATI ANAGRAFICI:
- Nome: Luca Consalter
- Tessera CartaFRECCIA: 036647537
- Nato: Torino, 07/02/1987
- Residenza: Via Cola di Rienzo 8, 20143 Milano
- Email: luca.consalter@gmail.com
- Telefono: [INSERIRE]

{IF protocollo}
RIFERIMENTO: Ho completato il webform (Protocollo: [RIF. 2026/XXXXX])
ma ho riscontrato errore tecnico sull'upload allegati (KIR-001 noto).
Allego ora la documentazione completa.
{ENDIF}

{IF otp_failed OR attachment_gate_blocked OR captcha_blocked}
NOTA TECNICA: Ho tentato la compilazione del webform reclami ma il sistema
ha richiesto verifica OTP non ricevuta (KIR-011), allegato obbligatorio per
treno regionale non caricabile (KIR-012), e/o CAPTCHA a pagina 6/6 non
risolvibile in automazione (KIR-006). Allego pertanto tutta la documentazione
a questa email per completamento manuale della pratica.
{ENDIF}

ALLEGATI:
- Copia biglietto (PDF)
- Screenshot ritardo ufficiale (Trenitalia + ViaggiaTreno)
- [Eventuale: email Smart Caring]

Cordiali saluti,
Luca Consalter
luca.consalter@gmail.com
```

### TPL-3: Call Center Script
```
Buongiorno, sono Luca Consalter, tessera CartaFRECCIA 036647537.
Chiedo assistenza per indennizzo [ritardo/cancellazione] treno [NUMERO]
del [DATA], tratta [PARTENZA]-[ARRIVO].
Ritardo verificato su Trenitalia e ViaggiaTreno: [XX] minuti.
{IF webform_failed} Ho tentato il webform ma ho riscontrato errore tecnico
sull'upload allegati, verifica OTP o CAPTCHA. {ENDIF}
Dati biglietto: PNR [XXXXX], importo EUR [XX,XX].
Potete registrare la pratica o indicarmi lo stato?
```

### TPL-4: ART Escalation
```
Oggetto: Segnalazione mancato rimborso — Tessera 036647537

Spett.le ART,

il sottoscritto Luca Consalter (Tessera CartaFRECCIA 036647537) segnala
mancato rimborso/indennizzo da parte di Trenitalia S.p.A.

Dati pratica:
- Treno: [NUMERO] del [DATA]
- Ritardo: [XX] min (verificato su fonti ufficiali)
- Richiesta inoltrata via: [canale] in data [DATA_RICHIESTA]
- Protocollo: [RIF. 2026/XXXXX]
- Termine: [DATA] (entro 1 anno)

Trenitalia non ha risposto entro 30 giorni / ha rifiutato ingiustamente.
Ai sensi Reg. UE 2021/782, richiedo intervento dell'Autorita.

Allego: protocolli, screenshot, email.

Luca Consalter
luca.consalter@gmail.com
```

---

## 📁 ARTIFACT NAMING CONVENTION v5.1.1

```
{PNR}_{TYPE}_{SOURCE}_{TIMESTAMP}.{ext}

TYPE:
  ticket        -> biglietto originale
  delay_tren    -> screenshot ritardo da trenitalia.com
  delay_viag    -> screenshot ritardo da viaggiatreno.it
  delay_stats   -> screenshot ritardo da trainstats.altervista.org
  smart_caring  -> screenshot notifica push/email
  groundtruth   -> collage multi-source
  app_confirm   -> conferma app/Area Riservata
  webform_data  -> dati webform compilati
  webform_prot  -> pagina protocollo
  email_sent    -> conferma invio email
  raccomandata  -> ricevuta postale
  report        -> report finale
  otp_page      -> screenshot pagina verifica OTP
  consent       -> screenshot checkbox GDPR consent
  captcha       -> screenshot CAPTCHA pagina 6/6 [v5.1.1]
  lefrecce_pdf  -> PDF biglietto scaricato da lefrecce.it [v5.1.1]

Esempi:
  2740877613_delay_tren_20260424_1630.png
  2740877613_groundtruth_20260424_1645.png
  2740877613_smart_caring_20260424_1650.png
  2740877613_otp_page_20260424_1655.png
  2740877613_captcha_20260424_1700.png
  2740877613_lefrecce_pdf_20260424_1705.pdf
  BATCH_report_20260424_1710.md
```

---

## ⏱️ SLA & TIMELINE v5.1.1

| Canale | Tempo Agent | Risposta Trenitalia | Next Check | Escalation Trigger |
|--------|-------------|---------------------|------------|-------------------|
| CH-0 Ground Truth | 5 min | — | — | Confidence LOW |
| CH-1 BDR Auto | 2 min | 30 gg | D+30 | Accredito mancante |
| CH-2 App/Sito | 5 min | 24h | D+7 | No conferma |
| CH-3 LeFrecce | 5 min | 24h | D+7 | No conferma |
| CH-4 Webform | **18 min** | 10-30 gg | D+15 | No risposta |
| CH-5 Email | 5 min | 5-10 gg | D+10 | No risposta |
| CH-6 Call Center | N/A | Immediato | D+1 | — |
| CH-7 Posta | 15 min | 30-60 gg | D+45 | No risposta |
| CH-8 ART | 30 min | 60-90 gg | D+90 | — |

**Nota v5.1.1:** Il tempo agent per CH-4 è aumentato da 15 a 18 min per accomodare recovery PDF da lefrecce.it e human-in-the-loop CAPTCHA.

---

## 🤖 AGENT PROMPT v5.1.1

```
================================================================================
MISSION: RimborsoTrenitalia_v5.1.1_MultiSource_OTP_Captcha_Resilience
CLASSIFICATION: Internal Use — PII Handling Required
ARCHITECTURE: HA + Evaluator-Optimizer + Cross-Validation + MFA Resilience + Human-in-the-Loop
================================================================================

ROLE:
Sei un agente browser enterprise specializzato in rimborsi Trenitalia.
Operi con ground truth verification, evaluator loop, e full traceability.
Mai azione senza prova. Mai stop senza fallback.

OWNER DATA (Immutable — Read Only):
- NAME: Luca Consalter
- BIRTH: Torino, 07/02/1987
- ADDRESS: Via Cola di Rienzo 8, 20143 Milano
- CF_CARD: 036647537
- EMAIL: luca.consalter@gmail.com
- PHONE: [ASK AT RUNTIME — VAULT]
- CARD_LAST4: [ASK AT RUNTIME — VAULT]
- PASSWORD: [ASK AT RUNTIME — VAULT]

SECURITY DIRECTIVES:
1. NEVER log passwords or full card numbers.
2. NEVER save credentials to local files.
3. PII inseribile SOLO in form HTTPS ufficiali Trenitalia.
4. All screenshots → /artifacts/ with naming convention.
5. OTP codes MUST be extracted from email in real-time, NEVER cached.
6. CAPTCHA images MUST be presented to human operator, NEVER solved by AI.

GROUND TRUTH SOURCES (Verifica ritardo su ALMENO 1 fonte prima di agire):
- PRIMARY: trenitalia.com/it/informazioni/ritardi
- PRIMARY: viaggiatreno.it
- SECONDARY: trainstats.altervista.org
- SECONDARY: zugfinder.net/it/start
- PRIMARY: Smart Caring inbox (luca.consalter@gmail.com)

MISSION MODES:
[A] SINGLE-TRENO: Utente fornisce treno specifico.
[B] BATCH-SCAN: Scansiona "I MIEI VIAGGI" ultimi 12 mesi, processa tutti eleggibili.

PHASE 0 — HEALTH CHECK (Quality Gate QG-1)
1. ASK: "Modalita [A] Single o [B] Batch?"
2. ASK: Password, Telefono, Ultime 4 cifre carta.
3. VERIFY login su trenitalia.com con CF_CARD + PASSWORD.
4. VERIFY login su lefrecce.it con CF_CARD + PASSWORD (per PDF recovery).
5. IF FAIL → STOP. Suggerisci recupero password.
6. IF OK → PROCEED.

PHASE 1 — DATA COLLECTION (Quality Gate QG-2)
IF MODE [A]:
  1. ASK: Numero treno, Data, Tratta, Ritardo, Tipo biglietto, Canale acquisto, Importo.
  2. IF dati mancanti → AUTO-RECOVER da Area Riservata.
  3. POPULATE ticket_record.

IF MODE [B]:
  1. NAVIGATE trenitalia.com → "I MIEI VIAGGI".
  2. SCROLL ultimi 12 mesi.
  3. FOR EACH ticket: EXTRACT pnr, treno, data, tratta, importo → batch_manifest.csv
  4. FOR EACH: CHECK ritardo su trenitalia.com/ritardi + viaggiatreno.it
  5. IF eleggibile → ADD to eligible_list.
  6. ASK: "Processo tutti gli M treni? [Y/N]"

PHASE 2 — GROUND TRUTH VERIFICATION (Evaluator EV-1)
FOR EACH ticket:
  1. SOURCE A: trenitalia.com/ritardi → delay_A, screenshot_A
  2. SOURCE B: viaggiatreno.it → delay_B, screenshot_B
  3. SOURCE C (opt): trainstats.altervista.org → delay_C, screenshot_C
  4. SOURCE D (opt): Scan inbox Smart Caring → notification_D
  5. CROSS-VALIDATE:
     IF delay_A == delay_B (±5 min) → confidence = HIGH
     ELIF 1 source → confidence = MEDIUM
     ELSE → confidence = LOW → STOP, richiedi manuale
  6. SAVE: artifacts/{pnr}_groundtruth_{timestamp}.png
  7. SET ticket_record.confidence = [HIGH|MEDIUM|LOW]

PHASE 3 — DECISION MATRIX
RUN Decision Matrix Algorithm (vedi sezione Decision Matrix).
DETERMINE: channel, percent, action.
POPULATE ticket_record.

PHASE 3.5 — OTP PRE-FLIGHT (Quality Gate QG-OTP)
  1. VERIFY: Accesso email luca.consalter@gmail.com funzionante
  2. VERIFY: Email associata a CartaFRECCIA 036647537 è corretta e accessibile
  3. ACTION: Apri inbox e spam folder in tab secondaria
  4. IF email non accessibile → STOP. Correggi prima in Area Riservata.
  5. IF train_type == REGIONALE → VERIFY lefrecce.it purchases accessibile per PDF
  6. IF OK → PROCEED to Phase 4.

PHASE 4 — CHANNEL EXECUTION (Evaluator EV-2 pre-submit, EV-3 post-submit)
FOR EACH ticket (ordine: data piu recente prima):

  IF channel == BDR_AUTO:
    LOG "Auto. Monitor D+30."
    SET status = MONITORING
    CONTINUE

  IF channel == APP/SITO:
    EXECUTE CH-2 Procedure
    EV-2 CHECK (Pre-Submit): tutti campi OK? Erogazione = carta? Note contiene Reg. UE?
    IF EV-2 FAIL → FIX e riprova (max 3)
    SUBMIT
    EV-3 CHECK (Post-Submit): protocollo visibile? screenshot salvato?
    IF SUCCESS → SET status = SUBMITTED, SAVE protocol
    ELSE → TRIGGER CH-4

  IF channel == WEBFORM:
    EXECUTE CH-4 Procedure (Steps 4.1–4.12)
    EV-2 CHECK (incl. Consent + Regional Attachment + OTP-readiness + CAPTCHA-ready)
    IF KIR-012 triggered → attempt attachment recovery (lefrecce.it PDF → App → Screenshot)
    IF KIR-001 triggered → complete senza allegati, SAVE protocol, TRIGGER CH-5
    SUBMIT → OTP LOOP (EV-OTP)
    IF KIR-011 triggered → retry OTP max 3, poi TRIGGER CH-5
    CAPTCHA GATE (EV-CAPTCHA) → HUMAN-IN-THE-LOOP
    IF KIR-006 triggered → STOP webform, TRIGGER CH-5
    POST-SUBMIT → EV-3

  IF channel == EMAIL:
    EXECUTE CH-5 Procedure
    EV-4 CHECK: email sent? allegati OK?
    SET status = SUBMITTED

PHASE 5 — REPORT GENERATION
GENERATE: artifacts/BATCH_report_{timestamp}.md
CONTENT:
- Summary: N treni, M eleggibili, P protocolli
- Table: PNR | Treno | Data | Ritardo | Fonti | Confidence | % | Canale | Protocollo | Status
- Ground Truth Log: per ogni treno, quali fonti usate e risultati
- Known Issues: KIR triggered e risoluzioni
- Next Actions: D+7, D+15, D+30, D+90

PHASE 6 — CLEANUP
- CLEAR clipboard.
- CLOSE all tabs.
- LOGOUT Area Riservata.
- LOGOUT lefrecce.it.
- ARCHIVE artifacts.
- DISPLAY summary to user.

================================================================================
END OF PROMPT
================================================================================
```

---

## ✅ CHECKLIST PRE-LANCIO v5.1.1

```
[ ] Password Area Riservata Trenitalia testata
[ ] Password lefrecce.it testata (stessa CF, può essere diversa)
[ ] ⭐ ACCESSO lefrecce.it → user-area/purchases VERIFICATO
[ ] Telefono cellulare noto
[ ] Ultime 4 cifre carta per verifica accredito
[ ] Accesso email luca.consalter@gmail.com verificato
[ ] Email CartaFRECCIA associata corretta
[ ] INBOX pronta: spam controllata
[ ] ALLEGATO REGIONALE: lefrecce.it purchases testato per data viaggio
[ ] Screenshot abilitati nel browser agent
[ ] Cartella ~/artifacts/ pronta
[ ] Connessione internet stabile
[ ] HUMAN-ON-CALL per CAPTCHA pagina 6/6 (se automazione pura)
[ ] Timer: 25 min max per single
```

---

## 📎 APPENDIX — URL Reference v5.1.1

| Service | URL | Purpose |
|---------|-----|---------|
| Trenitalia Home | https://www.trenitalia.com/it.html | Entry point |
| Area Riservata | https://www.trenitalia.com/it.html | Login CF Card |
| Info Ritardi | https://www.trenitalia.com/it/informazioni/ritardi | Ground Truth A |
| Smart Caring | https://www.trenitalia.com/it/informazioni/smart-caring.html | Notifications |
| BDR Auto Info | https://www.trenitalia.com/it/servizi/indennizzo-automatico-biglietto-digitale-regionale.html | Auto conditions |
| Webform Reclami | https://reclami-e-suggerimenti.trenitalia.com/rimborsi/anagrafica.aspx | Fallback |
| LeFrecce | https://www.lefrecce.it | Frecce/IC |
| **lefrecce.it Purchases** | **https://www.lefrecce.it/Channels.Website.WEB/#/user-area/purchases** | **PDF Biglietto Recovery** |
| ViaggiaTreno | http://www.viaggiatreno.it | Ground Truth B (real-time) |
| TrainStats | https://trainstats.altervista.org | Ground Truth C (storico) |
| Zugfinder | https://www.zugfinder.net/it/start | Ground Truth D (stats AV) |
| ART | https://www.autorita-trasporti.it | Escalation |

---

## 💡 PRO TIP DA ARCHITECT v5.1.1

> *"Il webform Trenitalia ha 4 gate, non 3: Dati → Consenso → Allegato → CAPTCHA. Il CAPTCHA a pagina 6/6 è il gate finale che nessun agente può bypassare senza human-in-the-loop. La strategia HA è: prepara tutto prima (dati, allegato da lefrecce.it, consenso spuntato), poi invoca l'umano solo per i 4 caratteri del CAPTCHA. Se l'umano non c'è, il fallback CH-5 Email è il tuo disaster recovery."*

> *"lefrecce.it/user-area/purchases è la fonte nascosta più potente: stesso backend Trenitalia, interfaccia diversa, spesso il PDF è disponibile qui quando l'App Trenitalia fa storie. Usala come primo tentativo, non come fallback."*

Questa skill è progettata per:
- **Zero richieste illegittime:** Ground truth su ≥1 fonte prima di ogni submit
- **Zero perdite dati:** Evaluator loop su ogni step critico
- **Zero blocchi irrecuperabili:** OTP, allegato, consenso e CAPTCHA hanno tutti fallback documentati
- **Scalabilità orizzontale:** Stesso prompt per 1 o 100 treni
- **Audit completo:** Artifact naming + report markdown per ogni missione
- **Human override:** Checkpoint espliciti prima di azioni irreversibili

**Prossimo step consigliato:**  
Prima di rieseguire CH-4, eseguire **Phase 3.5 (OTP Pre-Flight)** in modalità *read-only*: verifica accesso lefrecce.it purchases, email CF, e allegato PDF per la data specifica. Se tutto passa, procedi con il webform; se fallisce, correggi prima di sprecare tempo sulla compilazione.

---
*Skill v5.1.1 lefrecce.it PDF Recovery + CAPTCHA Confirmation — Enterprise HA Architecture.*
*Sources: trenitalia.com, viaggiatreno.it, trainstats.altervista.org, zugfinder.net, lefrecce.it*
