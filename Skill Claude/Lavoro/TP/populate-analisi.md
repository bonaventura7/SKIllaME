---
name: "populate-analisi"
description: "Maps and inserts Screening Results data into the Excel Analisi worksheet, ensuring that all existing formulas remain untouched. Invoke when the user asks to auto-populate the Analisi sheet or to review and configure the source-to-target mapping rules.."
---

# Populate Analisi

## Scopo
Automatizzare il popolamento del foglio "Analisi" partendo dal foglio "Results/Risultati" generato dallo screening, preservando le formule esistenti e mappando correttamente le colonne.

## Quando attivare
Attiva questa skill quando l’utente chiede di:
- Popolare automaticamente il foglio "Analisi"
- Mappare colonne tra "Results" e "Analisi"
- Preservare formule e gestire controlli di coerenza

## Input richiesti (sempre)
1. Triennio da elaborare (es. 2021 2022 2023)
2. Indicatore finanziario principale da calcolare o verificare
3. File Excel sorgente e fogli corretti (“Results/Risultati” e “Analisi”)

## Procedura operativa
1. Validare presenza fogli e intestazioni
2. Identificare riga header e mappare le colonne per pattern
3. Allineare righe per Company Name o BvD ID
4. Popolare solo le colonne di input e sintesi
5. Preservare le formule nelle colonne calcolate
6. Eseguire controlli di coerenza (mismatch, anni mancanti, formati)

## Regole di compilazione
- Non sovrascrivere formule nel foglio "Analisi"
- Convertire “n.a.” in celle vuote
- Normalizzare i valori percentuali in numeri
- Evidenziare i flag NACE per review manuale

## Fase 4: Gestione errori e bug check
- Mismatch nomi società tra “Results” e “Analisi”
- Formato numerico non coerente (testo vs numero)
- Anni mancanti o non allineati al triennio richiesto

## Implementazione tecnica
Usa lo script:

```bash
python confronto_analisi.py --input "C:\path\to\file.xlsx" --years 2021 2022 2023
```

Lo script:
- Popola i campi di sintesi e i dati annuali disponibili
- Preserva le formule
- Aggiunge “Data Update” e “Source” se le colonne sono presenti
- Riporta mismatch e anni mancanti a fine esecuzione

## Output atteso
- File `_Analisi_Popolato.xlsx` con dati inseriti e formule intatte
- Riepilogo mismatch e anni mancanti stampato a console
