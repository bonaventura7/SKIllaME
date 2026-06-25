---
name: sbnp-masterfile-template-factory
description: >-
  Genera, sanitizza, analizza e valida template Masterfile Transfer Pricing in
  stile SBNP, preservando il design system del file Word sorgente, la struttura
  normativa standardizzata, i quality gate redazionali e la Style Cognition
  Layer per capire i documenti a livello di struttura, sintassi, ritmo,
  lessico, formule ricorrenti e architettura argomentativa. Usa questa skill
  quando l'utente vuole: creare un nuovo template Masterfile da un gold source
  .docx, clonare il design di un Masterfile SBNP esistente, ripulire un file
  Word da residui di clienti precedenti, costruire un builder kit (template +
  playbook + checklist + QA gate), oppure capire e replicare lo stile di uno o
  più documenti senza copiarli meccanicamente. Trigger forti: "template
  masterfile", "copia design", "stile SBNP", "ripulisci docx", "builder kit
  SBNP", "template TP", "gold source masterfile", "sanitizza template",
  "capire stile documento", "analizza sintassi e struttura", "replica tono".
language: it
version: "3.1.0-final"
source: internal
risk: safe
compatibility:
  tools: [python, fetch_file]
  outputs: [docx, md, json, xlsx, txt]
---

# SBNP Masterfile Template Factory 3.1 Final

## 0) Scopo

Questa skill crea o sanitizza un **template Masterfile Transfer Pricing** in stile SBNP,
oppure genera un **builder kit** completo composto da template Word, playbook redazionale,
checklist dati cliente e QA gate.

In più, questa versione finale aggiunge una **Style Cognition Layer**: non si limita a copiare il design,
ma capisce lo stile dei documenti a livello di:
- struttura del documento;
- architettura dei paragrafi;
- sintassi prevalente;
- ritmo frasale;
- lessico specialistico;
- formule ricorrenti;
- modo di esporre fatti, metodo, evidenze e conclusioni.

L'obiettivo non è scrivere il Masterfile cliente-specifico, ma preparare un **artefatto
riutilizzabile, pulito, coerente, stilisticamente allineato e difendibile** che preservi:
- struttura normativa standard del Masterfile;
- stile editoriale SBNP;
- design system del documento Word sorgente;
- qualità sintattico-argomentativa dei documenti campione;
- quality gate finali per intercettare refusi, residui cliente, placeholder incoerenti, toni sbagliati e fragilità tecniche del `.docx`.

## 1) Regola madre: prima mente locale, poi esecuzione

Prima di qualsiasi intervento:
1. **Mente locale** — ricostruisci obiettivo, contesto, input, rischi, workaround.
2. **Brainstorming** — valuta 2-3 approcci possibili e scegli il più robusto.
3. **Scelta architetturale** — preferisci la soluzione meno fragile e più reversibile.
4. **Esecuzione** — applica modifiche minime e controllate.
5. **Quality gate** — verifica stile, struttura, contenuto, apribilità del file e residui.

Non saltare direttamente al codice o a sostituzioni brute-force.

## 2) Principio architetturale

### Soluzione ideale
Generare un template perfetto da zero usando librerie ad alto livello, asset redazionali controllati
e una mappa di stile estratta dai documenti sorgente.

### Soluzione pragmatica raccomandata
Quando esiste un Masterfile SBNP approvato o di buona qualità, **clonare un gold source e sanitizzarlo**
è preferibile a generare da zero.

**Perché funziona:**
- evita drift di stile;
- preserva `styles.xml`, `theme1.xml`, numbering, margini, header/footer e dettagli invisibili ma critici;
- riduce il rischio di produrre un `.docx` corrotto;
- massimizza la fedeltà al design system SBNP;
- consente di combinare **design preservation** e **style cognition**.

### Cosa evitare
- ricreare da zero un `.docx` complesso senza necessità;
- sostituire testo cliente-specifico con regex cieche su XML interi;
- modificare asset di stile senza motivo;
- confondere **copia del testo** con **estrazione del pattern di stile**;
- mescolare transcript, log o brainstorming grezzo dentro template o `SKILL.md`.

## 3) Tipi di task supportati

Classifica il task in una di queste categorie:
- **A1 — Template da gold source**: duplica un `.docx` approvato e trasformalo in template pulito.
- **A2 — Sanitize template esistente**: ripulisci residui cliente e placeholder non coerenti.
- **A3 — Builder kit completo**: genera template + playbook + checklist + QA gate.
- **A4 — QA finale**: esegui controllo pass/fail su template già prodotto.
- **A5 — Design extraction**: estrai e stabilizza il design system da uno o più Masterfile SBNP.
- **A6 — Style cognition**: analizza uno o più documenti per capire stile, struttura e sintassi depositabile.
- **A7 — Hybrid mode**: unisci design extraction + style cognition + sanitize template.

## 4) Input minimi richiesti

### 4.1 Input bloccanti
Per procedere servono almeno:
- un **gold source** Word (`.docx`) oppure un template di base già approvato;
- il **nome del Gruppo target**;
- la **ragione sociale corretta della Capogruppo**;
- il **FY / data di chiusura del periodo d'imposta**;
- la scelta del deliverable: solo `.docx`, builder kit, style report o combinazione dei tre.

### 4.2 Input arricchenti
Se disponibili, migliorano il risultato:
- elenco dei clienti precedenti da ripulire (es. Damiani, Bandera, DB);
- frontespizio desiderato;
- indice definitivo del Masterfile;
- glossario SBNP già validato;
- organigramma, tabelle standard, placeholder da lasciare;
- standard SBNP interno aggiornato (playbook, checklist, QA gate);
- documenti campione da usare come **stile** e documenti campione da usare come **contenuto**.

Se mancano dati bloccanti, fermati e chiedi **solo ciò che sblocca il lavoro**.

## 5) Standard SBNP da rispettare

Quando il playbook interno è disponibile, **prevale sempre** su qualunque inferenza stilistica.

### 5.1 Stile editoriale
- **Corpo testo**: Times New Roman 12 pt;
- **Titolo 2 / Titolo 3**: Bordeaux Scuro `#A32020`, grassetto e corsivo;
- tono: professionale, formale, impersonale, orientato al diritto tributario internazionale.

### 5.2 Tag interni ammessi in drafting
Usa solo questi tag quando l'informazione non è stabilizzata:
- `[DATO MANCANTE: ...]`
- `[INCERTO: ...]`
- `[DISCREPANZA: ...]`

Non trasformare un dato incerto in un contenuto “definitivo”.

## 6) Style Cognition Layer — obbligatoria quando l'utente chiede di «capire lo stile»

Questa fase prende ispirazione da un approccio di document architecture difensiva:
non copiare meccanicamente il testo sorgente; estrai invece pattern, struttura,
ritmo, logica argomentativa e lessico utile, poi ricostruisci un testo o un template
originale, pulito e professionalmente depositabile.

### 6.1 Document Intake Router
Classifica ogni file caricato in una o più categorie:
- **Documento sorgente di stile**
- **Documento sorgente di contenuto**
- **Documento sorgente di prova**
- **Commenti interni da convertire**
- **Materiale da non copiare ma solo sintetizzare**
- **Materiale tecnico/numerico da verificare**

### 6.2 Diagnosi iniziale obbligatoria
Dopo la lettura dei documenti, produci sempre una mini-diagnosi:
- **Dominio prevalente**: es. transfer pricing / contenzioso / audit / compliance
- **Modalità scelta**: DEEP / REVIEW / BUILD / STYLE-EXTRACTION
- **Documenti usati come stile**
- **Documenti usati come contenuto**
- **Rischio principale**
- **Tesi/voce centrale provvisoria**

### 6.3 Cosa analizzare nei documenti di stile
Analizza almeno questi livelli:

#### A. Voce
- formale / impersonale / istituzionale;
- assertiva o prudente;
- tecnica o narrativa;
- analitica o sintetica.

#### B. Struttura
- apertura del paragrafo;
- premessa;
- sviluppo;
- chiusura;
- modo di introdurre tabelle, figure e allegati.

#### C. Sintassi
- lunghezza media frasi;
- frequenza di subordinate;
- uso di incisi;
- densità nominale;
- prevalenza di costruzioni passive o attive.

#### D. Ritmo argomentativo
- frasi brevi o medio-lunghe;
- alternanza tra affermazione, spiegazione e caveat;
- frequenza di formule come “in particolare”, “in via preliminare”, “come si evince”.

#### E. Lessico e formule ricorrenti
Estrai termini e formule ricorrenti senza copiarli meccanicamente.
Esempi utili in contesto professionale:
- “come si evince dalla tabella sopra esposta”
- “si rimanda all’Allegato 1”
- “il Gruppo opera”
- “nel periodo d’imposta in esame”
- “in particolare”
- “si segnala che”

#### F. Architettura probatoria
Capisci come il documento:
- introduce un fatto;
- richiama un dato;
- ancora il testo a tabelle/allegati;
- gestisce incertezze;
- evita toni colloquiali o interni.

### 6.4 Output della Style Cognition
Quando richiesto, restituisci un **Style Report** con:
1. **Voce prevalente**
2. **Struttura dei paragrafi**
3. **Pattern sintattici**
4. **Formule ricorrenti utili**
5. **Elementi da NON replicare** (commenti, refusi, placeholder, errori)
6. **Mappa di stile applicabile al nuovo template**

## 7) Output ammessi

Questa skill può produrre uno o più dei seguenti output:
1. **Template Word Masterfile** pulito e riutilizzabile;
2. **Playbook redazionale** in Markdown o Word;
3. **Checklist dati cliente** in Markdown, Word o Excel-ready;
4. **Report di estrazione design system**;
5. **Style Report** su struttura/sintassi/lessico/ritmo;
6. **Registro QA finale** pass/fail;
7. **Report JSON di sanitizzazione** con warning, sostituzioni e residui;
8. **Versione TXT ultra-pulita** della skill o del playbook.

## 8) Workflow operativo standard

### Fase A — Intake e classificazione
- leggi gli input disponibili;
- classifica il task (A1/A2/A3/A4/A5/A6/A7);
- individua rischi, fragilità e vincoli di file;
- separa documenti di stile da documenti di contenuto.

### Fase B — Mente locale e brainstorming
Per ogni task esplicita internamente:
- obiettivo preciso;
- stato dell'arte;
- rischio nascosto;
- workaround migliore;
- criterio di successo.

#### Approcci da comparare
**Approccio 1 — Generazione da zero**
- utile solo se non esiste alcun gold source;
- rischio alto di drift di stile.

**Approccio 2 — Clone & Sanitize**
- approccio raccomandato in ambiente SBNP;
- preserva stili, design e compatibilità Word.

**Approccio 3 — Gold source + skeleton injection**
- ottimo quando vuoi mantenere frontespizio, indice e heading già pronti.

**Approccio 4 — Style cognition + clone**
- ideale quando vuoi preservare il design e capire anche come i documenti “parlano”.

### Fase C — Esecuzione tecnica

#### Modalità raccomandata: Clone & Sanitize
1. Duplica il gold source.
2. Apri il `.docx` come archivio ZIP.
3. Preserva intatti:
   - `word/styles.xml`
   - `word/theme/theme1.xml`
   - numbering, rels, settings, font table, header/footer
4. Agisci solo sui file XML testuali rilevanti, tipicamente:
   - `word/document.xml`
   - `word/header*.xml`
   - `word/footer*.xml`
   - `word/footnotes.xml`
   - `word/endnotes.xml`
   - `word/comments.xml`
   - `docProps/core.xml`
   - `docProps/custom.xml`
5. Modifica solo i **text nodes**, non l'XML intero a stringa libera.
6. Rimuovi o sostituisci:
   - nomi cliente precedente;
   - sedi, date, dati identificativi non riutilizzabili;
   - testi non riusabili nel template.
7. Inserisci lo skeleton target.
8. Richiudi il `.docx`.
9. Esegui residual scan e report finale.

#### Skeleton minimo del Masterfile
Il template deve almeno contenere:
- Copertina
- Indice
- Glossario
- Introduzione
- Presupposto del principio di libera concorrenza o “arm's length principle”
- Ambito e utilizzo del presente report
- Struttura del presente documento
- 1 Struttura organizzativa
- 2 Attività svolte
  - 2.1 Principali fattori di generazione dei profitti del gruppo
  - 2.2 Flussi delle operazioni
  - 2.3 Accordi per la prestazione di servizi infragruppo
  - 2.4 Principali mercati
  - 2.5 Struttura operativa e catena del valore
  - 2.6 Operazioni di riorganizzazione aziendale
- 3 Beni immateriali del gruppo multinazionale
- 4 Attività finanziarie infragruppo
- 5 Rapporti finanziari del gruppo multinazionale
- Allegato 1 Bilancio consolidato del Gruppo
- Appendice (se prevista)

### Fase D — Design system extraction
Se il task richiede di copiare il design di documenti esistenti:
- estrai `styles.xml` e `theme1.xml` dal `.docx`;
- identifica font corpo, headings, size e colori chiave;
- confronta più documenti SBNP;
- stabilizza uno **standard interno**.

### Fase E — Builder kit
Quando l'utente chiede un kit completo, genera:
- `SBNP_Masterfile_Template_vX.docx`
- `SBNP-Playbook.md`
- `SBNP-Checklist.md`
- `SBNP-QA-Gate.md`
- opzionale: `SBNP-Style-Report.md`
- opzionale: `SBNP-SKILL.txt`

### Fase F — Report tecnico di sanitizzazione
Genera, ove possibile, un report JSON con:
- file modificati;
- numero di sostituzioni per pattern;
- warning;
- residui trovati dopo la sanitizzazione;
- esito finale (`success`, `message`).

## 9) Companion implementation consigliata

Se l'utente chiede anche il motore tecnico, preferisci una companion implementation Python con queste caratteristiche:
- `tempfile.TemporaryDirectory()` invece di temp dir fissa;
- `Path` da `pathlib`;
- `xml.etree.ElementTree` per modificare **solo** i nodi di testo;
- residual scan finale su XML rilevanti;
- verifica integrità ZIP (`testzip()`);
- backup opzionale;
- `dry_run=True/False`.

### Caratteristiche minime della companion implementation
- **Mai** usare solo `word/document.xml` come unico target.
- **Mai** sostituire anni o numeri genericamente senza contesto, a meno di modalità esplicita `template_mode`.
- **Sempre** produrre un report tecnico se il task è di sanitizzazione automatica.
- **Sempre** verificare che il `.docx` risultante sia apribile.

## 10) Quality gate finale — obbligatorio

Prima di consegnare qualsiasi output, esegui sempre questo controllo.

### 10.1 Controlli editoriali
- il corpo è nello stile previsto;
- i titoli critici seguono il colore corretto;
- non ci sono commenti o revisioni residue;
- non ci sono blocchi markdown o transcript finiti nel documento finale;
- il tono resta depositabile e professionale.

### 10.2 Controlli di pulizia
- nessun residuo Damiani / Bandera / DB / altri clienti precedenti;
- nessun placeholder dimenticato non marcato;
- nessun campo con dati palesemente non riferiti al cliente target.

### 10.3 Controlli strutturali
- indice coerente;
- sezione 2.6 corretta: `Operazioni di riorganizzazione aziendale`;
- numerazione tabelle e figure continua;
- Allegato 1 presente.

### 10.4 Controlli stilistici avanzati
- ritmo frasale coerente con i campioni;
- formule ricorrenti usate con moderazione e coerenza;
- nessuna imitazione meccanica di un documento terzo;
- differenza chiara tra **stile replicato** e **testo copiato**.

### 10.5 Controlli tecnici sul file
- il `.docx` si apre correttamente;
- Word non segnala corruzione;
- PDF esportabile;
- tabelle e heading non risultano rotti o vuoti in modo incoerente.

## 11) Stop conditions

Interrompi o segnala chiaramente quando:
- il gold source non è disponibile;
- il `.docx` risultante non passa il controllo di apribilità;
- i riferimenti cliente precedente non sono stati completamente rimossi;
- il documento è stato alterato in modo tale da perdere il design system;
- i dati richiesti per personalizzare il template mancano e l'utente vuole un documento “finale” anziché un template.

## 12) Workaround smart policy

### Workaround pragmatico
- **Cosa facciamo ora:** usiamo un gold source SBNP e lo sanitizziamo, poi estraiamo una mappa di stile dai documenti campione.
- **Perché funziona:** preserva il design e consente di capire meglio tono, struttura e sintassi.
- **Limite:** se il gold source è sporco o Word ha spezzato il testo su più run, alcuni residui possono sfuggire.
- **Rischio residuo:** residui nascosti in XML secondari o stringhe spezzate su più `w:t`.
- **Evoluzione verso soluzione definitiva:** template ufficiale SBNP pulito, versionato, validato e una v2 paragraph-aware del motore Python.

## 13) Output format raccomandato

Quando completi il lavoro, restituisci sempre una consegna strutturata con:

### Sintesi
- cosa è stato generato;
- da quale gold source;
- livello di pulizia raggiunto.

### Mente locale
- scelta architetturale fatta;
- rischio maggiore evitato;
- workaround applicato.

### Piano operativo
- passaggi eseguiti;
- stile estratto;
- eventuali input ancora necessari.

### Soluzione
- nome dei file generati;
- contenuto essenziale;
- mappa di stile;
- eventuali placeholder lasciati.

### Workaround / fallback
- limiti attuali;
- come evolvere.

### Rischi e mitigazioni
- residui cliente;
- apribilità del file;
- coerenza del design;
- rischio di copia meccanica dello stile.

### Validazione
- check pass/fail;
- qualità finale.

### Prossimi passi
- personalizzazione per cliente 4;
- QA partner review;
- builder kit finale.

## 14) Cosa NON deve fare questa skill

Questa skill **non** deve:
- scrivere il Masterfile completo cliente-specifico se l'utente chiede solo il template;
- inventare dati o testi fiscali definitivi non supportati;
- copiare meccanicamente il testo sorgente invece di estrarre pattern di stile;
- mescolare transcript, log operativi, brainstorming grezzo o appunti di sessione dentro `SKILL.md` o dentro il template finale;
- sovrapporsi a una skill di QA puro o di drafting completo, se quelle esistono già come skill distinte.

## 15) Esempi di trigger validi

### Esempio 1
**Input utente:**
> Ho tre masterfile SBNP già belli. Fammi un template Word pulito con lo stesso stile.

### Esempio 2
**Input utente:**
> Copiami il design del Damiani e rendilo un template generico per il prossimo cliente.

### Esempio 3
**Input utente:**
> Voglio il kit completo: template, playbook e checklist cliente.

### Esempio 4
**Input utente:**
> Ho già uno script Python che sanitizza il .docx. Miglioralo in modo che sia più robusto e generi un report.

### Esempio 5
**Input utente:**
> Usa questi documenti per capire struttura, sintassi, formule ricorrenti e tono: poi dammi un template che "parli" come loro senza copiarli.

## 16) Criterio di eccellenza

La skill è riuscita se il risultato finale:
- sembra prodotto dallo Studio SBNP e non da un generatore generico;
- è riutilizzabile per più clienti;
- è tecnicamente apribile e stabile in Word;
- non contiene residui del cliente precedente;
- capisce e replica **il modo di costruire il discorso**, non solo il layout;
- riduce drasticamente il lavoro manuale del draft successivo.
