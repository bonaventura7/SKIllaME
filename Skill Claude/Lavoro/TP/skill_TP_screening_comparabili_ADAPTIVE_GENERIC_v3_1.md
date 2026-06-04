---
name: tp-comparability-analysis-adaptive-generic
description: >
  Screening adattivo di comparabilità Transfer Pricing, settore-agnostico. Usa questa skill quando l'utente
  chiede analisi di comparabilità, benchmarking TP, ricerca comparabili, revisione panel, matrice di rigetto,
  selezione/scarto comparabili, analisi funzionale TP, o fornisce liste di società da classificare come
  comparabili/non comparabili. La skill non assume mai il settore a priori: costruisce un profilo target dinamico
  da tested party, anchor panel, transazione, prodotti/servizi, funzioni, asset, rischi e mercato. Produce una
  matrice one-hot con una sola causa di rigetto per società e quality gate finale.
version: 3.1
language: it
---

# Skill — TP Comparability Analysis Adaptive Generic v3.1

## 0. Principio operativo

Prima capisco **che cosa deve essere comparabile**, poi classifico le società.

Non assumo mai che il settore sia metalli, software, pharma o altro. Il settore e il profilo target si deducono da:

- tested party, se disponibile;
- anchor panel / società iniziali indicate come “buone”;
- descrizione del business;
- transazione infragruppo da testare;
- prodotti o servizi oggetto della transazione;
- funzioni, asset e rischi;
- geografia, periodo e criteri di indipendenza.

Formula guida:

```text
Profilo target = funzioni + prodotti/servizi + rischi + asset + mercato + modello di business
```

La domanda corretta è sempre:

> Questa società è simile al profilo target di questo specifico incarico TP?

---

## 1. Quando attivare la skill

Attiva questa skill quando l’utente menziona o chiede:

- analisi di comparabilità;
- transfer pricing benchmarking;
- TP benchmarking;
- ricerca comparabili;
- screening comparabili;
- selezione comparabili;
- matrice di rigetto;
- matrice di riflessione;
- scarto soggetti non comparabili;
- classificazione società comparabili/non comparabili;
- analisi funzionale nel contesto TP;
- “quali società sono simili?”;
- “quali devo scartare?”;
- “fai Excel con cause di rigetto”.

Attiva anche se l’utente fornisce semplicemente una lista di aziende/società e chiede di revisionarle ai fini TP.

---

## 2. Architettura HA della pipeline

```text
INPUT grezzo
  -> Layer 0  Intake e assunzioni
  -> Layer 1  Parsing
  -> Layer 2  Normalizzazione
  -> Layer 3  Profilazione dinamica target
  -> Layer 4  Enrichment società candidate
  -> Layer 5  Classificazione one-hot
  -> Layer 6  Human TP review / OECD logic
  -> Layer 7  Output Excel / Markdown
  -> Layer 8  Quality gate
  -> Layer 9  Iterazione controllata
```

### Layer 0 — Intake e assunzioni

Acquisire, se disponibile:

- tested party;
- anchor panel / società “buone”;
- società candidate;
- transazione TP;
- funzione target;
- prodotti/servizi;
- rischi e asset;
- geografia;
- anni fiscali;
- criterio di indipendenza;
- solo screening qualitativo oppure anche analisi economico-finanziaria.

Se dati mancanti non bloccano, procedere con assunzioni esplicite. Se bloccano, fare massimo 3 domande mirate.

### Layer 1 — Parsing

Accettare input in:

- testo libero;
- elenco puntato/numerato;
- tabella incollata da Excel/PDF;
- CSV/TSV;
- Excel;
- lista con URL;
- lista con BD number/tax number.

Estrarre per ogni società:

| Campo | Regola |
|---|---|
| Nome società | Nome legale completo, se disponibile |
| Identificativo | BD number, tax ID, VAT, company number o N/D |
| Paese | Da prefisso, contesto o N/D |
| Sito web | URL normalizzato o N/D |
| Note utente | Conservare eventuali note |

### Layer 2 — Normalizzazione

- Pulire suffissi legali: Ltd, Inc, GmbH, S.r.l., Co., Ltd., S.A. de C.V., ecc.
- Normalizzare URL: aggiungere `https://` se necessario, rimuovere trailing slash.
- Deduplicare per identificativo, nome normalizzato e sito.
- Segnalare omonimie o identità ambigue.
- Non scartare società solo perché mancano dati: usare HOLD se necessario.

### Layer 3 — Profilazione dinamica del target

Costruire un profilo sintetico:

```text
Il profilo target dei comparabili è: [tipo attività], [prodotti/servizi],
[funzioni ammesse], [funzioni escluse], [rischi/asset rilevanti], [geografia], [periodo].
```

Esempi:

- **Distribuzione metalli**: distributori/grossisti/centri servizio di acciai e metalli industriali, con magazzino e lavorazioni leggere accessorie.
- **Software reseller**: rivenditori/distributori di software di terzi, senza sviluppo IP proprietario rilevante.
- **Contract manufacturer**: produttori conto terzi a rischio limitato, senza marchi propri e senza R&D strategica.
- **Service provider amministrativo**: fornitori di servizi amministrativi/back-office, senza funzioni strategiche o IP.
- **Logistica**: operatori logistici/3PL con magazzino, trasporto e gestione ordini, senza proprietà dei beni trasportati.

### Layer 4 — Enrichment

Per ciascuna società raccogliere evidenza su:

- attività principale;
- settore;
- prodotti/servizi;
- funzioni;
- business model;
- ownership/indipendenza;
- intangibili evidenti;
- dati finanziari disponibili, se richiesti;
- fonte/evidenza sintetica.

Regole:

- preferire sito ufficiale;
- fallback su fonti affidabili;
- non inventare dati;
- in caso di dubbio usare HOLD / Identità non verificabile / Dati finanziari non disponibili;
- distinguere sempre tra “non trovato” e “non esistente”.

---

## 3. Domande minime obbligatorie

Non fare troppe domande. Usare questo blocco minimo e procedere se possibile.

1. Le società iniziali che mi hai dato sono il panel di riferimento da imitare?
2. Qual è la tested party oppure, se non c’è, qual è il business comune delle società “buone”?
3. Quale transazione o attività dobbiamo confrontare: distribuzione, produzione, servizi, licenza IP, logistica, software, altro?
4. Le società con funzioni aggiuntive devono essere escluse o possono restare con cautela?
5. Vuoi escludere automaticamente società con settore/prodotti/funzioni diversi?

Se l’utente ha già dato abbastanza informazioni, non ripetere domande: procedere con assunzioni esplicite.

---

## 4. Decision tree universale one-hot

Applicare a ogni società.

```text
Step 1 — Esiste evidenza sufficiente sulla società?
├─ No  -> Identità non verificabile / Altro
└─ Sì  -> Step 2

Step 2 — È indipendente, se l’indipendenza è richiesta?
├─ No  -> Società non indipendente
└─ Sì / non rilevante -> Step 3

Step 3 — Opera nello stesso settore del panel target?
├─ No  -> Settore non comparabile
└─ Sì  -> Step 4

Step 4 — Offre prodotti/servizi comparabili?
├─ No  -> Prodotti/servizi diversi
└─ Sì  -> Step 5

Step 5 — Svolge funzioni comparabili?
├─ No  -> Funzioni diverse
└─ Sì  -> Step 6

Step 6 — Svolge funzioni aggiuntive rilevanti?
├─ Sì  -> Funzioni ulteriori
└─ No  -> Step 7

Step 7 — Ha prodotti/servizi ulteriori distorsivi?
├─ Sì  -> Prodotti/servizi ulteriori
└─ No  -> Step 8

Step 8 — Ha intangibili rilevanti non comparabili?
├─ Sì  -> Marchi, brevetti e altri intangibili
└─ No  -> Step 9

Step 9 — Ha dati finanziari utilizzabili, se richiesti?
├─ No  -> Dati finanziari non disponibili
└─ Sì  -> Non rigettata preliminarmente
```

---

## 5. Cause di rigetto standard

Usare una sola causa per società esclusa o in HOLD.

| Causa | Quando usarla |
|---|---|
| Società non indipendente | Captive, consociata, JV controllata, gruppo non ammesso |
| Società non finalizzata al profitto | Ente pubblico non commerciale, fondazione, associazione, università, no-profit |
| Marchi, brevetti e altri intangibili | Brand/IP owner, brevetti, software/piattaforme proprietarie, R&D strategica |
| Funzioni diverse | Business model diverso: produttore vs distributore, IP owner vs service provider, retailer vs grossista |
| Funzioni ulteriori | Settore simile ma attività aggiuntive rilevanti: produzione accessoria, engineering, consulenza strategica, lavorazioni significative |
| Prodotti/servizi diversi | Categoria di beni/servizi diversa rispetto al target |
| Prodotti/servizi ulteriori | Vende anche target, ma mix più ampio e potenzialmente distorsivo |
| Settore non comparabile | Settore complessivamente diverso dal panel target |
| Dati finanziari non disponibili | Qualitativamente simile ma dati finanziari non utilizzabili, se richiesti |
| Identità non verificabile | Sito non funzionante, dominio incoerente, omonimia, identificativo non verificato |
| Altro | Solo se nessuna categoria precedente è adatta; dettaglio obbligatorio |

### Gerarchia in caso di più criticità

1. Identità non verificabile / evidenza insufficiente
2. Società non indipendente, se filtro essenziale
3. Società non finalizzata al profitto
4. Settore non comparabile
5. Prodotti/servizi diversi
6. Funzioni diverse
7. Marchi, brevetti e altri intangibili
8. Funzioni ulteriori
9. Prodotti/servizi ulteriori
10. Dati finanziari non disponibili
11. Altro

Nota: la gerarchia può essere adattata se l’utente indica che un filtro è prioritario.

---

## 6. Regola one-hot obbligatoria

Per ogni società:

- massimo una sola `X` nelle colonne di rigetto;
- se esclusa: `Causa di rigetto` = esatto nome della colonna marcata;
- se non rigettata: nessuna `X`, causa vuota, esito `Non rigettata preliminarmente`;
- se HOLD: una sola causa, preferibilmente `Identità non verificabile`, `Dati finanziari non disponibili` o `Altro`;
- se `Altro = X`, il dettaglio è obbligatorio;
- non usare più cause contemporaneamente: scegliere la causa prevalente.

---

## 7. Output Excel consigliato

Nome file:

```text
matrice_screening_TP_[settore_o_panel]_[YYYY-MM-DD].xlsx
```

### Fogli

1. **Matrice screening** — tutti i soggetti e tutte le colonne.
2. **Riepilogo cause** — pivot conteggi per causa, rigettate, non rigettate, HOLD, totale.
3. **Profilo target** — assunzioni, tested party/anchor panel, criteri, esclusioni.
4. **Societa non rigettate** — solo società preliminarmente ammesse.
5. **HOLD da verificare** — società con evidenza insufficiente.

### Colonne matrice

| # | Colonna |
|---|---|
| 1 | Nome società |
| 2 | Identificativo / BD number / tax number |
| 3 | Paese |
| 4 | Sito web |
| 5 | Descrizione attività |
| 6 | Confronto con profilo target |
| 7 | Commento esclusione |
| 8 | Causa di rigetto |
| 9 | Società non indipendente |
| 10 | Società non finalizzata al profitto |
| 11 | Marchi, brevetti e altri intangibili |
| 12 | Funzioni diverse |
| 13 | Funzioni ulteriori |
| 14 | Prodotti/servizi diversi |
| 15 | Prodotti/servizi ulteriori |
| 16 | Settore non comparabile |
| 17 | Dati finanziari non disponibili |
| 18 | Identità non verificabile |
| 19 | Altro |
| 20 | Dettaglio se Altro |
| 21 | Esito preliminare |
| 22 | Confidence level |
| 23 | Fonte/evidenza sintetica |

### Stile Excel

- Header: `#1B2A4A`, testo bianco.
- Righe alternate: bianco / `#F7F7F5`.
- Causa di rigetto valorizzata: rosso `#C0392B`.
- Esito:
  - verde per `Non rigettata preliminarmente`;
  - rosso per `Rigettata`;
  - arancio per `HOLD`.
- Freeze panes sulla matrice.
- Filtri attivi.
- Nessuna griglia visibile.

---

## 8. Quality gate finale

Prima di consegnare, validare:

| # | Controllo | Esito atteso |
|---|---|---|
| 1 | Tutti i soggetti originali sono presenti | True |
| 2 | Nessun duplicato evidente | True |
| 3 | Ogni riga ha al massimo una X | True |
| 4 | Se causa valorizzata, esiste una X corrispondente | True |
| 5 | Se nessuna X, causa di rigetto vuota | True |
| 6 | Se non rigettata, esito coerente | True |
| 7 | Se HOLD, commento e causa coerenti | True |
| 8 | Se Altro = X, dettaglio compilato | True |
| 9 | Confidence level valorizzato per tutti | True |
| 10 | Fonte/evidenza sintetica presente | True |
| 11 | Riepilogo cause somma correttamente | True |
| 12 | Profilo target esplicitato | True |

Se un controllo fallisce, correggere prima di consegnare.

---

## 9. Confidence level

| Livello | Quando usarlo |
|---|---|
| Alto | Sito ufficiale o fonte primaria chiara, informazioni coerenti, settore inequivocabile |
| Medio | Fonti parziali, settore deducibile ma non confermato al 100% |
| Basso | Sito non accessibile, fonti contrastanti, omonimia possibile, dati scarsi |

---

## 10. Workaround intelligenti

### Caso: manca tested party

- Cosa facciamo ora: usare anchor panel / società iniziali come profilo target.
- Perché funziona: il panel buono rappresenta implicitamente funzioni, prodotti e rischi desiderati.
- Limite: meno preciso di un’analisi FAR completa.
- Rischio residuo: inclusioni/esclusioni discutibili se l’anchor panel è eterogeneo.
- Evoluzione: integrare descrizione tested party e transazione.

### Caso: fonti incomplete

- Cosa facciamo ora: classificare HOLD con causa `Identità non verificabile` o `Dati finanziari non disponibili`.
- Perché funziona: evita invenzioni e preserva audit trail.
- Limite: riduce il panel finale.
- Rischio residuo: società potenzialmente comparabile esclusa temporaneamente.
- Evoluzione: richiedere documenti, bilanci, sito ufficiale o database commerciali.

### Caso: società con più criticità

- Cosa facciamo ora: applicare gerarchia e assegnare una sola causa prevalente.
- Perché funziona: matrice pulita, difendibile e auditabile.
- Limite: perde granularità secondaria.
- Rischio residuo: motivazioni accessorie non codificate.
- Evoluzione: inserire criticità secondarie nel commento, senza aggiungere X multiple.

---

## 11. Template risposta finale

```markdown
## Sintesi screening

Ho analizzato [X] società rispetto al profilo target: [profilo sintetico].

- Non rigettate preliminarmente: [N]
- Rigettate: [N]
- HOLD / da verificare: [N]

## Cause di rigetto

| Causa | Numero |
|---|---:|
| Società non indipendente | [N] |
| Società non finalizzata al profitto | [N] |
| Marchi, brevetti e altri intangibili | [N] |
| Funzioni diverse | [N] |
| Funzioni ulteriori | [N] |
| Prodotti/servizi diversi | [N] |
| Prodotti/servizi ulteriori | [N] |
| Settore non comparabile | [N] |
| Dati finanziari non disponibili | [N] |
| Identità non verificabile | [N] |
| Altro | [N] |

## Società non rigettate

| Società | ID | Motivo |
|---|---|---|
| [Nome] | [ID] | [Motivo] |

## Quality gate

- One-hot: PASS/FAIL
- Cause coerenti con X: PASS/FAIL
- HOLD motivati: PASS/FAIL
- Fonti presenti: PASS/FAIL
- Totali coerenti: PASS/FAIL

## File prodotto

Allego Excel con matrice completa, riepilogo cause, profilo target e controlli.
```

---

## 12. Regola anti-errore finale

Non classificare una società come non comparabile in assoluto.

Classificarla solo rispetto al profilo target dell’incarico:

- se il profilo target è software, una società software può essere comparabile;
- se il profilo target è chimica, una società chimica può essere comparabile;
- se il profilo target è distribuzione metalli, una società chimica normalmente non è comparabile;
- se il profilo target è produttore conto terzi, un distributore puro normalmente ha funzioni diverse.

La causa di rigetto è sempre relativa al panel target, non assoluta.
