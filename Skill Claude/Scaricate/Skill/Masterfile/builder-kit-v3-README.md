# Builder Kit SBNP v3

## Componenti generati

- `sbnp-masterfile-template-factory-SKILL-v3.md`
- `style_analyzer.py`

## Scopo

Questo kit unisce:
1. una skill ad alta intensità documentale per generare/sanitizzare template Masterfile SBNP;
2. uno script Python per estrarre automaticamente pattern di stile da uno o più file `.docx`.

## Uso rapido

### 1) Analizzare lo stile di documenti sorgente
```bash
python style_analyzer.py file1.docx file2.docx --json-out style_report.json --md-out style_report.md
```

### 2) Usare la skill v3 come specifica operativa
Leggere `sbnp-masterfile-template-factory-SKILL-v3.md` per:
- intake documentale;
- design extraction;
- style cognition;
- sanitize workflow;
- quality gate finale.

## Output previsti

### style_analyzer.py
- `style_report.json`
- `style_report.md`

### skill v3
- template `.docx`
- playbook
- checklist
- QA gate
- style report
- report di sanitizzazione

## Note

- Lo script analizza testo, heading style, formule ricorrenti, ritmo frasale e lessico rilevante.
- La skill governa il processo e definisce i guardrail operativi.
