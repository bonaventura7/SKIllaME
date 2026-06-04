# Istruzioni Operative Definitive — Timesheet SBNP

## Obiettivo

Compilare il timesheet mensile SBNP partendo da:

1. email inviate in Outlook Web Mail;
2. riunioni presenti in Outlook Web Calendar;
3. Google Sheet SBNP esistente.

L’agente deve:

- usare solo browser automation per Outlook;
- non usare mai API Outlook o Microsoft Graph;
- non cercare file locali, cloud, Excel, template o allegati;
- mappare le ore ai clienti SBNP;
- applicare un cap massimo di 8 ore al giorno;
- aggiornare il Google Sheet se possibile;
- altrimenti produrre una tabella copiabile.

---

## Trigger

L’agente si attiva solo con questi comandi:

```text
timesheet [mese]
compila timesheet
```

Esempi:

```text
timesheet marzo 2026
timesheet aprile
timesheet 04/2026
compila timesheet
```

Se il mese non è specificato, chiedere solo:

```text
Per quale mese devo compilare il timesheet?
```

Non fare altre domande iniziali.

---

## Vincoli Assoluti

```text
1. Usare solo Outlook Web Mail via browser.
2. Usare solo Outlook Web Calendar via browser.
3. Non usare mai API Outlook.
4. Non usare mai Microsoft Graph.
5. Non usare export Outlook.
6. Non cercare file locali.
7. Non cercare file su OneDrive, SharePoint, Google Drive o cartelle condivise.
8. Non aprire allegati.
9. Non scaricare allegati.
10. Non gestire credenziali, password, OTP o MFA.
11. Se serve login, fermarsi e chiedere all’utente di autenticarsi manualmente.
12. Leggere solo dati necessari: data, ora, oggetto, destinatari, partecipanti, titolo evento, durata.
```

---

## Google Sheet di Destinazione

```text
https://docs.google.com/spreadsheets/d/1wboFuFVIDUH-cNQAYQ6nOXyOLgbTjiJXRkzW_1y90Us/edit?usp=sharing
```

---

## Struttura del Foglio

Il foglio usa una struttura a matrice mensile.

Colonne:

```text
Data
Ore
Tod's
Tesmec
Petrone
Ascoli
Eataly
Swiss Steel
Pettinaroli
Innovo
Valbruna
Amenduni
Damiani
Digital Bros
Inglese
RT Law
Review
Sviluppo
SMEI
Sony
Beuer
Medel
Mega
Crosspolimeri
Bandera
Rhom
```

Regole:

```text
- Ogni riga rappresenta un giorno.
- La colonna Ore contiene il totale giornaliero.
- Le colonne cliente contengono le ore imputate al cliente.
- Le celle senza ore devono restare vuote, se il foglio usa celle vuote.
- Non scrivere 0 dove il foglio normalmente lascia celle vuote.
- Non creare nuove colonne cliente.
- Non modificare la struttura del foglio se non necessario.
```

---

## Step 1 — Determinazione del Mese

Dal comando dell’utente estrarre:

```text
Mese
Anno
Data inizio
Data fine
Numero giorni del mese
```

Esempio:

```text
timesheet marzo 2026
```

Diventa:

```text
Mese: marzo
Anno: 2026
Periodo: 01/03/2026 - 31/03/2026
```

Se l’anno non è specificato, usare l’anno corrente.

---

## Step 2 — Accesso a Outlook Web Mail

Aprire:

```text
https://outlook.office.com/mail/?deeplink=mail%2F0%2F
```

Se Outlook richiede autenticazione, fermarsi e dire:

```text
Sono arrivato alla pagina di login di Outlook. Autenticati manualmente, poi dimmi quando sei pronto.
```

Dopo il login:

```text
1. Aprire Posta inviata.
2. Filtrare per il mese richiesto.
3. Se il filtro non funziona bene, ordinare per data decrescente.
4. Scorrere manualmente fino all’inizio del mese.
5. Analizzare solo le email inviate nel mese richiesto.
6. Fermarsi appena si esce dal periodo richiesto.
```

---

## Step 3 — Estrazione Email Inviate

Per ogni email inviata nel mese raccogliere:

```text
Data
Ora
Oggetto
Destinatari principali
Domini destinatari
Cliente probabile
Tipo attività
Ore stimate
Confidenza matching
Note eventuali
```

Non leggere il corpo completo dell’email salvo sia indispensabile per capire il cliente o il tipo di attività.

Non aprire allegati.

---

## Regole di Stima Ore Email

| Tipo email | Ore |
|---|---:|
| Risposta brevissima, conferma, grazie, ok | 0.25 |
| Email operativa semplice | 0.50 |
| Email articolata con analisi, parere, risposta tecnica, legale o fiscale | 1.00 |
| Coordinamento complesso con molte persone o più azioni | 1.50 |
| Thread numeroso stesso giorno, stesso cliente, stesso argomento | massimo 2.00 |

---

### Deduplicazione Email

Non contare ogni email come attività separata.

Raggruppare email con:

```text
stesso giorno
stesso cliente
stesso argomento
```

Esempio:

```text
5 email nello stesso giorno su Eataly / documentazione / revisione
```

Non diventano:

```text
5 x 0.50h = 2.50h
```

Ma diventano una riga aggregata:

```text
Eataly — scambio email e coordinamento documentazione — 1.00h / 1.50h
```

---

### Anti Doppio Conteggio Email + Riunione

Se una email è solo organizzativa rispetto a una riunione già conteggiata nello stesso giorno e stesso cliente:

```text
- non conteggiarla separatamente;
oppure
- includerla nella stessa attività della riunione;
oppure
- assegnarle massimo 0.25h.
```

Esempio:

```text
Email: "Confermo call Eataly alle 15"
Riunione calendario: "Call Eataly" 15:00-16:00
```

Risultato consigliato:

```text
Conteggiare solo la riunione da 1.00h.
```

---

## Step 4 — Accesso a Outlook Calendar

Aprire:

```text
https://outlook.office.com/calendar/view/workweek?deeplink=mail%2F0%2F
```

Procedura:

```text
1. Passare alla vista mese oppure settimana.
2. Andare al mese richiesto.
3. Scorrere tutte le settimane del mese.
4. Aprire gli eventi lavorativi rilevanti.
5. Escludere eventi personali o non lavorativi.
```

---

## Step 5 — Estrazione Riunioni

Per ogni riunione lavorativa raccogliere:

```text
Data
Titolo evento
Ora inizio
Ora fine
Durata
Partecipanti principali
Domini partecipanti
Cliente probabile
Confidenza matching
Note eventuali
```

---

## Regole Riunioni

Conteggiare:

```text
- call con cliente;
- meeting operativo;
- review documentale;
- allineamento su pratica;
- riunione interna collegata a cliente o progetto;
- avanzamento lavori;
- discussione tecnica/fiscale/legale/organizzativa.
```

Escludere:

```text
- ferie;
- malattia;
- eventi personali;
- reminder;
- focus time;
- blocchi generici;
- pausa pranzo;
- travel time non chiaramente lavorativo;
- eventi senza collegamento professionale.
```

---

## Durata Riunioni

Usare sempre la durata effettiva del calendario:

```text
Durata = ora fine - ora inizio
```

Esempi:

```text
09:00 - 10:00 = 1.00h
14:30 - 16:00 = 1.50h
10:15 - 10:45 = 0.50h
```

Se la durata non è visibile:

```text
1. Aprire il dettaglio evento.
2. Cercare ora inizio e ora fine.
3. Se ancora non visibili, non inserire ore nel foglio.
4. Segnalare nel report finale: "durata non visibile — da verificare".
```

Non inventare durate.

---

## Step 6 — Matching Cliente SBNP

### Clienti Ammessi

Usare solo queste colonne cliente/categoria:

```text
Tod's
Tesmec
Petrone
Ascoli
Eataly
Swiss Steel
Pettinaroli
Innovo
Valbruna
Amenduni
Damiani
Digital Bros
Inglese
RT Law
Review
Sviluppo
SMEI
Sony
Beuer
Medel
Mega
Crosspolimeri
Bandera
Rhom
```

Non creare nuovi clienti.

---

### Gerarchia Matching

| Livello | Regola | Confidenza |
|---|---|---|
| 1 | Dominio email chiaramente riconducibile al cliente | Alta |
| 2 | Nome cliente esplicito in oggetto email o titolo evento | Alta |
| 3 | Nome cliente nei destinatari o partecipanti | Media |
| 4 | Keyword cliente nel testo visibile o snippet | Media |
| 5 | Contesto da thread o attività dello stesso giorno | Bassa |
| 6 | Fallback Review/Sviluppo solo se coerente | Bassa |

---

### Mapping Domini / Keyword

```text
@tods / tods / tod's → Tod's
@tesmec / tesmec → Tesmec
@petrone / petrone → Petrone
@ascoli / ascoli → Ascoli
@eataly / eataly → Eataly
@swisssteel / swiss steel → Swiss Steel
@pettinaroli / pettinaroli → Pettinaroli
@innovo / innovo → Innovo
@valbruna / valbruna → Valbruna
@amenduni / amenduni → Amenduni
@damiani / damiani → Damiani
@digitalbros / digital bros → Digital Bros
@inglese / inglese → Inglese
@rtlaw / rt law → RT Law
@smei / smei → SMEI
@sony / sony → Sony
@beuer / beuer → Beuer
@medel / medel → Medel
@mega / mega → Mega
@crosspolimeri / crosspolimeri → Crosspolimeri
@bandera / bandera → Bandera
@rhom / rhom → Rhom
```

---

## Step 7 — Fallback Cliente

Usare `Review` solo per:

```text
- analisi generale;
- controllo documenti;
- verifica;
- review;
- attività interna non tecnica;
- classificazione prudente di attività lavorativa non attribuibile con certezza.
```

Usare `Sviluppo` solo per:

```text
- automazioni;
- tool;
- workflow;
- processi;
- attività tecnica;
- configurazioni;
- sviluppo operativo.
```

Se non c’è sufficiente evidenza:

```text
- non inventare cliente;
- non creare nuova colonna;
- non scrivere automaticamente ore dubbie;
- segnalare nel report finale come riga da verificare.
```

---

## Step 8 — Aggregazione Giornaliera

Per ogni giorno:

```text
Ore giorno = ore email aggregate + ore riunioni
```

Poi distribuire le ore sulle colonne cliente.

La colonna `Ore` deve essere:

```text
somma delle colonne cliente del giorno
```

Esempio:

```text
Ore = Tod's + Tesmec + Petrone + ... + Rhom
```

Regola assoluta:

```text
Ore giorno <= 8
```

---

## Step 9 — Cap Massimo 8 Ore/Giorno

Se il totale calcolato supera 8 ore:

```text
totale giorno > 8
```

Applicare riduzione in questo ordine:

```text
1. Ridurre email brevi o solo organizzative.
2. Comprimere email stimate.
3. Aggregare attività minori dello stesso cliente.
4. Ridurre attività con confidenza bassa.
5. Preservare le riunioni con durata reale.
6. Ridurre riunioni solo se inevitabile e segnalarlo chiaramente.
```

Obiettivo:

```text
Ore finali giorno <= 8
```

Nel report finale indicare:

```text
Data
Ore calcolate prima del cap
Ore finali
Riduzioni applicate
```

---

## Step 10 — Compilazione Google Sheet

Aprire:

```text
https://docs.google.com/spreadsheets/d/1wboFuFVIDUH-cNQAYQ6nOXyOLgbTjiJXRkzW_1y90Us/edit?usp=sharing
```

Procedura:

```text
1. Trovare il blocco del mese richiesto.
2. Se il blocco esiste, lavorare solo su quel mese.
3. Se il blocco non esiste, creare un nuovo blocco copiando la struttura del mese precedente.
4. Prima di scrivere, verificare se le celle Ore o Totale contengono formule.
5. Se contengono formule, non sovrascriverle.
6. Scrivere solo nelle celle cliente giornaliere.
7. Lasciare vuote le celle senza ore.
8. Aggiornare o verificare la riga TOTALE [MESE].
```

---

## Gestione Mese Non Presente nel Foglio

Se il mese richiesto non esiste:

```text
1. Copiare il blocco del mese precedente.
2. Incollarlo sotto l’ultimo blocco presente.
3. Aggiornare le date dal giorno 01 all’ultimo giorno corretto del mese.
4. Rimuovere eventuali giorni in eccesso.
5. Aggiungere eventuali giorni mancanti.
6. Rinominare la riga finale in TOTALE [MESE].
7. Cancellare i valori cliente copiati dal mese precedente.
8. Conservare formule, formattazione e struttura.
9. Verificare che la colonna Ore funzioni correttamente.
```

---

## Policy Dati Esistenti

Se nel mese sono già presenti valori:

```text
1. Leggere i valori esistenti prima di modificarli.
2. Non cancellare dati senza motivo.
3. Se una cella già valorizzata deve cambiare, farlo solo dopo aver ricalcolato l’intero giorno.
4. Non sovrascrivere formule.
5. Nel report indicare se sono state modificate celle già valorizzate.
```

---

## Gestione Excel / File / Template

### Regola Principale

L’agente non deve mai cercare file autonomamente.

Quindi sono vietati:

```text
- ricerca di file Excel locali;
- ricerca di template timesheet;
- ricerca in cartelle download;
- ricerca in OneDrive;
- ricerca in SharePoint;
- ricerca in Google Drive;
- apertura allegati email;
- download di allegati;
- uso di file storici non forniti esplicitamente.
```

---

### Se l’utente fornisce esplicitamente un file Excel

Se l’utente carica o indica esplicitamente un file Excel da usare, allora l’agente può usarlo solo se il task lo consente.

Esempio comando valido:

```text
Usa questo Excel che ti ho caricato come template timesheet.
```

In quel caso:

```text
1. Usare solo il file fornito dall’utente.
2. Non cercare altri file.
3. Non aprire allegati Outlook.
4. Non modificare formule senza necessità.
5. Non cambiare struttura, colonne o formattazione salvo richiesta.
6. Compilare solo celle coerenti con il timesheet.
7. Salvare una copia modificata, non sovrascrivere l’originale salvo autorizzazione.
8. Restituire il file aggiornato o una tabella copiabile.
```

---

### Se esistono sia Google Sheet sia Excel

Priorità consigliata:

```text
1. Google Sheet indicato nel task.
2. Excel solo se fornito esplicitamente dall’utente.
3. Output copiabile se nessuno dei due è scrivibile.
```

Non usare Excel come fonte se il task dice di usare Google Sheet.

---

### Se l’agente non può accedere al file Excel

Rispondere:

```text
Non posso cercare autonomamente file Excel o template.
Se vuoi che usi un Excel, caricalo esplicitamente o forniscimi un link accessibile.
Altrimenti preparo la tabella copiabile nel formato del Google Sheet.
```

---

## Step 11 — Verifica Aritmetica

Prima di consegnare, verificare sempre:

```text
Per ogni giorno:
Ore = somma colonne cliente
Ore <= 8
```

Per il mese:

```text
Totale Ore mese = somma colonna Ore
Totale Ore mese = somma totali clienti
```

Se i totali non coincidono:

```text
1. Non consegnare.
2. Ricontrollare righe giornaliere.
3. Ricontrollare colonne cliente.
4. Correggere l’errore.
5. Ripetere la verifica.
```

---

## Checklist Pre-Consegna

```markdown
## Checklist Pre-Consegna

### Mese e periodo
- [ ] Mese richiesto correttamente identificato
- [ ] Anno corretto
- [ ] Data inizio corretta
- [ ] Data fine corretta
- [ ] Numero giorni del mese corretto
- [ ] Weekend gestiti correttamente

### Vincoli
- [ ] Usato solo Outlook Web Mail via browser
- [ ] Usato solo Outlook Web Calendar via browser
- [ ] Nessuna API Outlook usata
- [ ] Nessun Microsoft Graph usato
- [ ] Nessun export Outlook usato
- [ ] Nessun file cercato
- [ ] Nessun allegato aperto
- [ ] Nessuna credenziale gestita

### Email
- [ ] Analizzata Posta inviata del mese
- [ ] Email duplicate aggregate
- [ ] Email brevi stimate correttamente
- [ ] Email operative stimate proporzionalmente
- [ ] Thread stesso cliente/giorno aggregati
- [ ] Evitato doppio conteggio email/riunione

### Calendario
- [ ] Analizzate tutte le settimane del mese
- [ ] Riunioni lavorative incluse
- [ ] Eventi personali esclusi
- [ ] Ferie/malattia/reminder esclusi
- [ ] Durate lette dal calendario
- [ ] Eventi senza durata segnalati e non inventati

### Matching cliente
- [ ] Matching da dominio verificato
- [ ] Matching da oggetto/titolo verificato
- [ ] Matching da partecipanti verificato
- [ ] Matching debole segnalato
- [ ] Nessun cliente inventato
- [ ] Review/Sviluppo usati solo se coerenti

### Google Sheet
- [ ] Blocco mese trovato o creato correttamente
- [ ] Colonne cliente rispettate
- [ ] Nessuna nuova colonna creata
- [ ] Celle vuote lasciate vuote
- [ ] Formule non sovrascritte
- [ ] Dati esistenti non cancellati senza controllo

### Excel / file
- [ ] Nessun file cercato autonomamente
- [ ] Nessun allegato aperto
- [ ] Excel usato solo se fornito esplicitamente dall’utente
- [ ] Nessun template cercato in cartelle locali/cloud

### Controlli numerici
- [ ] Ogni giorno: Ore = somma colonne cliente
- [ ] Nessun giorno supera 8h
- [ ] Riga totale mensile aggiornata o verificata
- [ ] Totale Ore mese = somma totali clienti
- [ ] Giorni con cap 8h documentati

### Report finale
- [ ] Google Sheet aggiornato sì/no indicato
- [ ] Totale ore mese indicato
- [ ] Giorni lavorati indicati
- [ ] Giorni con cap 8h indicati
- [ ] Riepilogo per cliente indicato
- [ ] Righe da verificare indicate
- [ ] Link Google Sheet incluso
```

---

## Template se Non Riesce a Scrivere sul Google Sheet

```markdown
## ⚠️ Non sono riuscito a scrivere direttamente nel Google Sheet

Ho completato l’estrazione da Outlook Web Mail e Outlook Web Calendar, ma non sono riuscito ad aggiornare direttamente il Google Sheet.

Possibili cause:
- permessi di modifica non disponibili;
- Google Sheet aperto in sola lettura;
- sessione Google non autenticata;
- errore temporaneo del browser;
- celle protette;
- formule non modificabili;
- problema di caricamento del foglio.

Ho quindi preparato qui sotto la tabella nello stesso formato del foglio, pronta da copiare e incollare.

## Tabella da copiare nel Google Sheet

Data	Ore	Tod's	Tesmec	Petrone	Ascoli	Eataly	Swiss Steel	Pettinaroli	Innovo	Valbruna	Amenduni	Damiani	Digital Bros	Inglese	RT Law	Review	Sviluppo	SMEI	Sony	Beuer	Medel	Mega	Crosspolimeri	Bandera	Rhom
[righe del mese...]
TOTALE [MESE]	[totale]	[totali clienti...]

## Riepilogo

- Mese: [mese anno]
- Totale ore: [X]
- Giorni lavorati: [Y]
- Giorni con cap 8h applicato: [Z]
- Righe da verificare: [N]

## Azione richiesta

Puoi copiare la tabella sopra e incollarla nel blocco del mese corrispondente nel Google Sheet:

https://docs.google.com/spreadsheets/d/1wboFuFVIDUH-cNQAYQ6nOXyOLgbTjiJXRkzW_1y90Us/edit?usp=sharing
```

---

## Template se Non Può Usare Excel o File

```markdown
## ⚠️ File Excel non disponibile

Non posso cercare autonomamente file Excel, template, allegati o documenti in cartelle locali/cloud.

Per procedere hai due opzioni:

1. mi fornisci esplicitamente il file Excel da usare;
2. continuo con il Google Sheet indicato;
3. preparo una tabella copiabile nello stesso formato del timesheet.

In assenza di un file fornito esplicitamente, userò il Google Sheet o produrrò l’output copiabile.
```

---

## Template Report Finale Standard

```markdown
## ✅ Timesheet Compilato — [Mese] [Anno]

**Google Sheet aggiornato:** Sì / No  
**Link:** https://docs.google.com/spreadsheets/d/1wboFuFVIDUH-cNQAYQ6nOXyOLgbTjiJXRkzW_1y90Us/edit?usp=sharing  
**Totale ore mese:** [X]  
**Giorni lavorati:** [Y]  
**Giorni con cap 8h applicato:** [Z]  
**Righe da verificare:** [N]  

---

## 📊 Riepilogo per Cliente

| Cliente | Ore |
|---|---:|
| Tod's | [x] |
| Tesmec | [x] |
| Petrone | [x] |
| Ascoli | [x] |
| Eataly | [x] |
| Swiss Steel | [x] |
| Pettinaroli | [x] |
| Innovo | [x] |
| Valbruna | [x] |
| Amenduni | [x] |
| Damiani | [x] |
| Digital Bros | [x] |
| Inglese | [x] |
| RT Law | [x] |
| Review | [x] |
| Sviluppo | [x] |
| SMEI | [x] |
| Sony | [x] |
| Beuer | [x] |
| Medel | [x] |
| Mega | [x] |
| Crosspolimeri | [x] |
| Bandera | [x] |
| Rhom | [x] |
| **TOTALE** | **[X]** |

---

## 📋 Controllo Cap 8h Giornaliero

| Data | Ore calcolate | Ore finali | Azione |
|---|---:|---:|---|
| [gg/mm/yyyy] | [x] | [x] | [nessuna / riduzione applicata] |

---

## ⚠️ Righe da Verificare

| Data | Cliente assegnato | Motivo | Azione suggerita |
|---|---|---|---|
| [gg/mm/yyyy] | Review | Cliente non chiaramente identificabile | Verificare oggetto/destinatari |
```

---

## Prompt Finale da Incollare nel Browser Agentico

```markdown
Agisci come browser agentico. Task: compila timesheet SBNP.

Trigger:
- timesheet [mese]
- compila timesheet

Se il mese non è specificato, chiedi solo:
"Per quale mese devo compilare il timesheet?"

Mese da compilare: [INSERISCI MESE]

Vincoli assoluti:
- Usa solo Outlook Web Mail e Outlook Web Calendar via browser automation.
- Non usare mai API Outlook, Microsoft Graph o export Outlook.
- Non cercare mai file locali, OneDrive, SharePoint, Google Drive, Excel, template o allegati.
- Non aprire allegati.
- Non scaricare allegati.
- Non gestire credenziali, password, OTP o MFA.
- Se serve login, chiedi all’utente di autenticarsi manualmente.
- Leggi solo dati necessari: data, ora, oggetto, destinatari, partecipanti, titolo evento, durata.

Google Sheet:
https://docs.google.com/spreadsheets/d/1wboFuFVIDUH-cNQAYQ6nOXyOLgbTjiJXRkzW_1y90Us/edit?usp=sharing

Colonne foglio:
Data, Ore, Tod's, Tesmec, Petrone, Ascoli, Eataly, Swiss Steel, Pettinaroli, Innovo, Valbruna, Amenduni, Damiani, Digital Bros, Inglese, RT Law, Review, Sviluppo, SMEI, Sony, Beuer, Medel, Mega, Crosspolimeri, Bandera, Rhom.

Procedura:
1. Determina mese, anno, data inizio, data fine e numero giorni.
2. Apri Outlook Web Mail:
   https://outlook.office.com/mail/?deeplink=mail%2F0%2F
3. Se appare login, fermati e chiedi all’utente di autenticarsi manualmente.
4. Vai in Posta inviata.
5. Analizza solo le email inviate nel mese richiesto.
6. Per ogni email raccogli:
   data, ora, oggetto, destinatari, domini, cliente probabile, ore stimate, confidenza.
7. Stima ore email così:
   - risposta breve: 0.25h
   - email operativa semplice: 0.50h
   - email articolata: 1.00h
   - coordinamento complesso: 1.50h
   - thread stesso giorno/cliente/argomento: aggrega, max 2.00h
8. Raggruppa email simili per stesso giorno, cliente e argomento.
9. Evita doppio conteggio: se un’email è solo organizzativa rispetto a una riunione già conteggiata, includila nella riunione o assegnale massimo 0.25h.
10. Apri Outlook Web Calendar:
    https://outlook.office.com/calendar/view/workweek?deeplink=mail%2F0%2F
11. Analizza tutte le riunioni del mese, settimana per settimana se necessario.
12. Per ogni riunione raccogli:
    data, titolo, ora inizio, ora fine, durata, partecipanti, domini, cliente probabile, confidenza.
13. Usa la durata effettiva della riunione.
14. Se la durata non è visibile, apri il dettaglio evento; se ancora non visibile, non inserire ore e segnala "durata non visibile — da verificare".
15. Escludi ferie, malattia, eventi personali, reminder, focus time, blocchi generici e travel time non chiaramente lavorativo.
16. Mappa ogni attività a una delle colonne cliente usando dominio email, nome cliente in oggetto/titolo, destinatari, partecipanti e contesto.
17. Mapping clienti:
    @tods / tods / tod's → Tod's
    @tesmec / tesmec → Tesmec
    @petrone / petrone → Petrone
    @ascoli / ascoli → Ascoli
    @eataly / eataly → Eataly
    @swisssteel / swiss steel → Swiss Steel
    @pettinaroli / pettinaroli → Pettinaroli
    @innovo / innovo → Innovo
    @valbruna / valbruna → Valbruna
    @amenduni / amenduni → Amenduni
    @damiani / damiani → Damiani
    @digitalbros / digital bros → Digital Bros
    @inglese / inglese → Inglese
    @rtlaw / rt law → RT Law
    @smei / smei → SMEI
    @sony / sony → Sony
    @beuer / beuer → Beuer
    @medel / medel → Medel
    @mega / mega → Mega
    @crosspolimeri / crosspolimeri → Crosspolimeri
    @bandera / bandera → Bandera
    @rhom / rhom → Rhom
18. Se cliente non identificabile:
    - usa Review solo per analisi, controllo, verifica o attività interna generale;
    - usa Sviluppo solo per automazioni, tool, workflow o attività tecnica;
    - se non c’è evidenza sufficiente, non scrivere ore e segnala da verificare.
19. Per ogni giorno calcola:
    Ore giorno = somma ore email aggregate + somma durata riunioni.
20. Applica cap massimo 8h/giorno.
21. Se un giorno supera 8h:
    - riduci prima email brevi;
    - poi email stimate;
    - poi attività con confidenza bassa;
    - preserva le riunioni reali;
    - documenta la riduzione nel report.
22. Apri il Google Sheet.
23. Trova il blocco del mese richiesto.
24. Se il mese non esiste:
    - copia il blocco del mese precedente;
    - aggiorna date;
    - cancella valori cliente copiati;
    - conserva formule;
    - rinomina TOTALE [MESE].
25. Prima di scrivere verifica se celle Ore o Totale contengono formule.
26. Se ci sono formule, non sovrascriverle.
27. Scrivi solo nelle celle cliente giornaliere.
28. Lascia vuote le celle senza ore.
29. La colonna Ore deve essere la somma delle colonne cliente del giorno.
30. Nessun giorno deve superare 8h.
31. Aggiorna o verifica la riga TOTALE [MESE].
32. Verifica:
    - ogni giorno: Ore = somma colonne cliente;
    - nessun giorno > 8h;
    - totale mese = somma colonna Ore;
    - totale mese = somma totali clienti.
33. Se non riesci a scrivere nel Google Sheet, restituisci una tabella copiabile nello stesso formato del foglio.
34. Non cercare file Excel o template. Usa Excel solo se fornito esplicitamente dall’utente.
35. Restituisci sempre report finale con:
    - Google Sheet aggiornato sì/no;
    - totale ore mese;
    - giorni lavorati;
    - giorni con cap 8h;
    - riepilogo per cliente;
    - righe da verificare;
    - controllo cap giornaliero.

Regole finali:
- Non inventare clienti.
- Non inventare durate.
- Non contare due volte la stessa attività.
- Non superare 8h/giorno.
- Non sovrascrivere formule.
- Non cancellare dati esistenti senza controllo.
- Non cercare file.
- Non aprire allegati.
```

---

## Versione Ultra-Compatta per Uso Rapido

```markdown
Compila timesheet SBNP per [MESE].

Usa solo Outlook Web Mail e Outlook Web Calendar via browser.
Non usare API Outlook, Graph, export, file, allegati, Excel o template.
Se serve login, chiedi login manuale.

Fonti:
- Posta inviata Outlook del mese
- Calendario Outlook del mese

Google Sheet:
https://docs.google.com/spreadsheets/d/1wboFuFVIDUH-cNQAYQ6nOXyOLgbTjiJXRkzW_1y90Us/edit?usp=sharing

Colonne:
Data, Ore, Tod's, Tesmec, Petrone, Ascoli, Eataly, Swiss Steel, Pettinaroli, Innovo, Valbruna, Amenduni, Damiani, Digital Bros, Inglese, RT Law, Review, Sviluppo, SMEI, Sony, Beuer, Medel, Mega, Crosspolimeri, Bandera, Rhom.

Regole:
- Email brevi 0.25h
- Email operative 0.50h
- Email articolate 1.00h
- Coordinamento complesso 1.50h
- Thread stesso giorno/cliente max 2.00h
- Riunioni = durata reale da calendario
- Non inventare durate
- Non inventare clienti
- Aggrega email simili
- Evita doppio conteggio email/riunione
- Cap massimo 8h/giorno
- Celle vuote restano vuote
- Non sovrascrivere formule
- Non cancellare dati esistenti senza controllo

Matching:
dominio email, oggetto, titolo evento, partecipanti, contesto.
Se non chiaro: Review solo per analisi/verifica, Sviluppo solo per attività tecnica. Se dubbio, segnala da verificare.

Output:
aggiorna Google Sheet se possibile; altrimenti restituisci tabella copiabile.
Report finale obbligatorio:
totale ore, riepilogo clienti, giorni con cap 8h, righe da verificare, conferma Google Sheet aggiornato sì/no.
```
