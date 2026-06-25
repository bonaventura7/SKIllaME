---
name: nutrient-dws-processor
version: 1.0
description: Wrapper per l'API Nutrient DWS Processor — conversione formati, OCR, redaction, digital signing, form filling.
agents: [processor_agent, doc_agent]
triggers: [nutrient dws, dws processor, document processor, ocr redact sign]
---

# Nutrient DWS Processor

Missione

Fornire istruzioni e esempi per usare l'API DWS Processor per trasformazioni documentali: conversione formati, estrazione testo/tabelle, OCR, redaction, watermark e firma digitale.

Quando Usarla

- Automazione di pipeline ETL di documenti (PDF scans, moduli)
- Preparazione di dataset testuali estraendo tabelle e metadati

Trigger Keywords

`dws processor`, `nutrient dws`, `document processor`, `ocr`, `redact`

Processo Standard

1. Carica file al processor
2. Specifica operazioni (ocr, extract_tables, redact_patterns, sign)
3. Ricevi output (PDF/A, JSON structured, images)
4. Valida risultati e post-process (normalizzazione date, encoding)

Formato Output

Dipende dall'operazione: JSON con estrazioni, PDF con watermark/firma, CSV per tabelle

Workaround / Limitazioni

- OCR su scansioni di bassa qualità richiede pre-enhancement
- Monitorare timeouts per file di grandi dimensioni

Source: Skill Claude/Scaricate/Skill/Process documents with the Nutrient DWS Processor API. Convert formats, extract text and tables, OCR scanned documents, redact PII, add watermarks, digitally sign, and fill PDF forms..md
