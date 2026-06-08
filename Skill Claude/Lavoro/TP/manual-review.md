---
name: "benchmark-tp-screening-qualitativo"
description: "Qualitative TP screening con cluster, tolleranza e matrice esclusioni. Invoca quando devi compilare il foglio Analisi di Excel e classificare società partendo dai comparabili accettati."
---

# Skill Claude: TP Benchmark — Screening Qualitativo (v3.4)

╔══════════════════════════════════════════════════════════════════╗
║  Pattern-First + CBC + Tolleranza + Coerenza + Output Excel CSV  ║
║  OCSE 2022 | D.M. 14/5/2018 | Provv. AdE 360494/2020             ║
╚══════════════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════════════
0) Regole Assolute (anti-bug)
════════════════════════════════════════════════════════════════════
R1. Non iniziare lo screening (Fase 1) senza aver completato Fase 0.  
R2. Non saltare righe: ogni società deve avere esito + descrizione.  
R3. La descrizione è obbligatoria per tutte (anche rigettate).  
R4. Ogni “X” richiede 1 frase di motivazione (in Detail/Descrizione).  
R5. Se Sito vs Orbis è incoerente → prevale il dato più sfavorevole.  
R6. Lingua straniera ≠ rigetto: usa traduzione e indizi visivi.  
R7. Se dubbio non risolvibile → esito “Borderline” (non forzare).  
R8. Valuta materialità e rettificabilità (se rettificabile → nota).  
R9. Ogni 10 righe stampa stato avanzamento con conteggi parziali.  
R10. Timestamp obbligatorio quando il sito non è raggiungibile.

════════════════════════════════════════════════════════════════════
Fase 0 — Impara dal campione finale (obbligatoria)
════════════════════════════════════════════════════════════════════
Passo 0.1 — Chiedi il campione finale  
“Dammi il campione finale già ACCETTATO (comparabili confermati). Per ciascuno:  
Nome; Paese/Città; Sito; NACE; (se disponibile) CBC; una frase su cosa fa.  
Oppure carica l’Excel con colonna ‘ACCETTATA’ valorizzata.”

Passo 0.2 — Analizza pattern (per ogni accettata)  
Visita sito (Homepage, About, Services/Products, Clients/Portfolio, Brands, Wholesale/Trade, Shop). Estrai:
- D1 CBC prevalente: CBC501–513  
- D2 Tipo entità TP (neutro): Full-fledged/Contract/Toll Manufacturer; FFD; LRD; Principal; Routine Service; Holding  
- D3 Prodotti/servizi: top 3–5 + canale (B2B/B2C/misto)  
- D4 Asset & IP: marchi/brevetti/piattaforme; asset prevalenti; Intangible/TA basso/medio/alto  
- D5 Rischi: inventario, credito, mercato/FX (b/m/a)  
- D6 Settore & NACE: codici tipici + segmento (premium/luxury, ecc.)  
- D7 Mercato: locale/UE/globale; comparabilità geografica  
- D8 Scala: fatturato/dipendenti; flag outlier >10x

Passo 0.3 — Costruisci cluster + profilo ideale  
Raggruppa accettate in 2–5 cluster: CBC, tipo entità, prodotti/servizi, clientela, asset/IP, rischi, NACE, geografie, scala.  
Definisci profilo ideale (must-have vs nice-to-have) + Red Flag (forti vs attenzione).

Passo 0.4 — Chiedi conferma  
Mostra profilo ideale e chiedi conferma di cluster/perimetro, eccezioni/borderline, soglie:  
Intangible/TA (default 20%), extra-functions/products (default 20% ricavi), scala (>10x), geografie.

Passo 0.5 — Calibra tolleranza (obbligatorio)  
Chiedi: quante candidate? quante comparabili minime?  
Imposta modalità: A) >30 Stringente | B) 15–30 Standard | C) <15 Tollerante.  
Target: affidabilità ≥ 85% (no 100% match; vietate differenze materiali non rettificabili).

Elenco CBC per etichetta:  
CBC501 R&S | CBC502 IP | CBC503 Procurement | CBC504 Produzione | CBC505 Vendite/Marketing/Distribuzione |  
CBC506 Supporto | CBC507 Servizi a terzi | CBC508 Finanza intragruppo | CBC509 Finanza regolamentata |  
CBC510 Assicurazioni | CBC511 Holding equity | CBC512 Dormiente | CBC513 Altro

════════════════════════════════════════════════════════════════════
Fase 1 — Screening candidate (riga per riga in Excel)
════════════════════════════════════════════════════════════════════
Per ogni riga del foglio “Analisi” (nome può cambiare ogni anno):

Step 1 — Leggi dal foglio  
Company name; BvD ID; City/Country; Website address; Trade descr.; Full overview; NACE; Intangible/TA; Nr years; DB descr.

Step 2 — Visita il sito (fonte primaria)  
About; Services/Products; Clients/Portfolio; Brands; Wholesale/Trade; Shop.  
Se sito KO: X in Other + Detail “Website not reachable — data/ora”.

Step 2-bis — Cross-check Sito vs Orbis  
Se incongruenze (NACE retail vs sito B2B, GUO presente, IP alto, ecc.):  
prevale il dato più sfavorevole; documenta in Detail.

Step 3 — Profilo funzionale  
Assegna: CBC prevalente + tipo entità TP (neutro) + cluster più vicino.

Step 3-bis — Dati finanziari (TNMM)  
Se Nr years <3: Borderline (1–2) o X in Other (0 anni) con Detail “Insufficient financial data for TNMM — N years available”.

Step 4 — Principio di tolleranza (prima di X)  
Q1 Differenza è materiale per margini/PLI/rischi? Se no → non X.  
Q2 È rettificabile con aggiustamento ragionevole? Se sì → nota, non X.  
Q3 Modalità (tollerante/standard/rigida) in base alla numerosità.

Step 5 — Matrice esclusione (X o vuoto)  
A Non-independent | B Trademarks, patents and other intangibles | C Different functions |  
D Additional functions | E Different products/services | F Additional products/services |  
G Non-comparable sector | H Other (+Detail obbligatorio)  
Obbligo: per ogni X scrivi motivazione specifica.

Step 6 — Esito  
Accettata: 0 X | Rigettata: ≥1 X | Borderline: dubbi/info incomplete ma non sufficienti per X.

Step 7 — Codice rigetto + causa (solo se rigettata)  
1 Non-independent | 2 IP/Intangibles | 3 Different functions | 4 Additional functions |  
5 Different products | 6 Additional products | 7 Sector | 8 Other.

Step 8 — Descrizione società (obbligatoria)  
1) Chi è + CBC + tipo entità  
2) Cosa fa + clienti + B2B/B2C  
3) Modello + asset + rischi  
4) Note (incongruenze/tolleranza/aggiustamenti)

Step 9 — Colonne accessorie  
Fonte review: “Web Review”; Website: copia da input.

════════════════════════════════════════════════════════════════════
Fase 2 — Coerenza, Confidenza, Controllo Finale
════════════════════════════════════════════════════════════════════
Step 10 — Regole di coerenza (Orbis vs Sito)  
- Indipendenza: se GUO/azionisti corporate → preferisci “Non-independent”.  
- NACE/Settore: se sito indica B2B servizi e NACE è retail → prevale dato più sfavorevole.  
- IP/Intangibili: se marchi/brevetti/piattaforme propri → X in “Trademarks, patents and other intangibles”.  
- Geografia/scala: se scala >10x vs profilo ideale → segnala “attenzione” (non X automatico).

Step 11 — Confidenza (0–100)  
Punteggio basato su match profilo ideale:  
Funzioni (30%) | Prodotti/servizi (20%) | CBC/Tipo entità (20%) |  
Settore/NACE (10%) | Indipendenza (10%) | Asset/IP & rischi (10%)  
La modalità di tolleranza (Fase 0.5) regola la soglia di accettazione.

Step 12 — Stato avanzamento (ogni 10 righe)  
“Analizzate [N] su [TOT]. Accettate: [A] | Rigettate: [R] | Borderline: [B]  
Problemi: [website KO, dati insufficienti, incoerenze NACE, ecc.]”

Step 13 — Summary finale  
“SCREENING COMPLETATO  
Totale analizzate: [N]  
Accettate: [A] ([%]) | Rigettate: [R] ([%]) | Borderline: [B] ([%])  
→ Non-indipendente: [N1] | IP/Intangibili: [N2] | Funzioni diverse: [N3] | Funzioni aggiuntive: [N4]  
→ Prodotti diversi: [N5] | Prodotti aggiuntivi: [N6] | Settore non comparabile: [N7] | Altro: [N8]”

════════════════════════════════════════════════════════════════════
Fase 3 — Output finale (Report + CSV)
════════════════════════════════════════════════════════════════════
Output A: report conteggi  
Output B: CSV incollabile in Excel con colonne:
Company | Fonte | Website | Non-indep | Trademarks | Diff.Funct | Add.Funct | Diff.Prod | Add.Prod | Sector | Other | Detail |  
Risultato | Codice | Causa | Descrizione | Cluster | Confidence  
Nota: “Fonte” = “Web Review”; “Website” copiato da input Excel.

Appendice — Allineamento colonne Excel (compatibilità “Analisi”)
- Legge: Company name; BvD ID; City/Country; Website address; Trade descr.; Full overview; NACE; Intangible/TA; Nr years; DB descr.  
- Scrive: Matrice X; Esito; Codice; Causa; Descrizione; Cluster; Confidence; Fonte; Website.

Mappatura Colonne “Smart” quando intestazioni o posizioni cambiano  
- Individua il foglio analisi cercando intestazioni chiave nelle prime 20 righe:  
  “Company name”, “Website address”, “NACE”, “Intangible/TA”, “Screening qualitativo e giudizio finale”.  
- Le colonne di matrice esclusione possono variare posizione. Usa il riconoscimento fuzzy:  
  Cerca intestazioni contenenti (case-insensitive, spazi e punteggiatura ignorati):  
  “Società non indipendente”, “Marchi, brevetti e altri intangibili”,  
  “Funzioni diverse”, “Funzioni ulteriori”,  
  “Prodotti diversi”, “Prodotti ulteriori”,  
  “Settore non comparabile”, “Altro”.  
- Se gli header non sono presenti o sono abbreviati, usa sinonimi/keyword:  
  Non-independent | Independence | Trademarks/Patents/IP | Different functions | Additional functions |  
  Different products | Additional products | Non-comparable sector | Other.  
- Se mancano header (es. righe multiple di ‘X’ senza titoli):  
  1) Identifica la “riga titoli” cercando la prima riga che NON è tutta “X” e ha almeno 3 campi testo non vuoti.  
  2) Se non esiste, prendi la riga 1 come titoli e applica matching per somiglianza (contains).  
- Range di ricerca raccomandato: colonne 1–160 (copre gli indici tipici: 3, 4, 5, 7, 18, 60, 90, 116).  
- Quando trovi la colonna, scrivi “X” solo se la motivazione è chiara (Step 4/5); altrimenti lascia vuoto o “Borderline” in giudizio.  
- Valida coerenza: nessuna riga “Accettata” può avere X in matrice; ogni “Rigettata” deve avere ≥1 X; “Altro” richiede Detail.

╔══════════════════════════════════════════════════════════════════╗
║                         Fine Skill v3.4                          ║
╚══════════════════════════════════════════════════════════════════╝
