# xlsx-reverse-engineering Skill

**Reverse Engineering for Excel / Spreadsheet Archeology**

A specialized Agent Skill (per skills.sh / anthropics/skills standard) for deep, systematic, auditable reverse engineering of existing .xlsx, .xlsm and similar files.

## What's New (latest additions)
- 3 new scripts: `analyze_anomalies.py` (full pattern scanner), `build_graph.py` (Mermaid + edges), `verify.py` (cross-check gate)
- Rich synthetic test file + full pipeline run (see `examples/`)
- `REVERSE-EXCEL.md` template + filled demo example
- Trigger evaluation set (`references/trigger_eval.json`) for description optimization
- Full Italian translation: `SKILL.it.md`

## What it does
- Treats Excel workbooks as complex legacy "programs".
- Produces reliable, source-cited artifacts (`REVERSE-EXCEL.md`, inventories, graphs, anomaly reports).
- Strict anti-hallucination with `[Confirmed]/[Inferred]/[Unknown]` + provenance.
- Iterative workflow with living task list.
- Composes with the official `xlsx` skill (reuses openpyxl, recalc, pandas patterns).

## Installation / Usage
Copy the `xlsx-reverse-engineering/` folder into your skills directory or publish as repo.

**Recommended first prompt:**
"Use the xlsx-reverse-engineering skill on `path/to/your.xlsx`. Start with inventory and unpack."

See `SKILL.md` (English) or `SKILL.it.md` (Italian) for precise triggering rules.

## Directory Structure
```
xlsx-reverse-engineering/
├── SKILL.md / SKILL.it.md
├── README.md
├── LICENSE.txt
├── scripts/ (6 executable helpers)
├── references/ (4 guides + trigger_eval.json)
└── examples/
    ├── sample_re_test.xlsx (synthetic test file with hidden/veryHidden, obfuscation, named ranges)
    ├── REVERSE-EXCEL.md.template
    └── REVERSE-EXCEL-sample_re_test.md (demo filled report)
```

## Quick Test (with included sample)
```bash
cd xlsx-reverse-engineering
python scripts/inventory.py examples/sample_re_test.xlsx
python scripts/unpack_xlsx.py examples/sample_re_test.xlsx
python scripts/extract_formulas.py examples/sample_re_test.xlsx
python scripts/analyze_anomalies.py examples/sample_re_test.xlsx unpacked-...
python scripts/build_graph.py examples/sample_re_test.xlsx
python scripts/verify.py examples/sample_re_test.xlsx
```

The pipeline successfully detects:
- veryHidden sheet (SecretConfig)
- Hidden named range (TaxRateHidden)
- Obfuscation pattern (INDIRECT + N)
- Clean growth formulas

## Design Philosophy
High Availability / Resilience + Smart Problem Solving + Composition over duplication (as requested by Senior Solutions Architect role).

Created by combining reverse-engineering skills patterns from the skills.sh ecosystem with the production xlsx skill from anthropics/skills.

For real files: drop your .xlsx in `examples/` or any path and run the scripts. Update the REVERSE-EXCEL.md as you go.

## Latest Refinements (this session)
- **Description optimization**: Updated `description` in both `SKILL.md` and `SKILL.it.md` using the `trigger_eval.json` set. Made it more precise with explicit trigger phrases, better "Do NOT" examples, and clearer separation from the regular `xlsx` skill.
- **Inventory.py**: Minor fixes for modern openpyxl `defined_names` handling (now robustly iterates and extracts hidden/visible named ranges correctly).
- **More sample data**: Added `examples/sample_financial_re.xlsx` — a richer financial projection model with complex formulas, obfuscation, external link simulation, and veryHidden control flags.
- Full pipeline can be re-run on the new sample for additional validation.

The trigger description is now better calibrated for accurate skill selection.

## Major Evolution (this session)
- Adopted the structured 4-phase pipeline proposed (inspect → audit → extract_logic → generate_report).
- New core scripts implemented according to the detailed spec:
  - `inspect_xlsx.py`
  - `formula_audit.py`
  - `extract_logic.py`
  - `generate_report.py` (produces a professional multi-sheet Excel documentation report)
- Added rich third sample: `sample_pivot_macro_re.xlsx` (heavy SUMIFS/pivot simulation, macro area with comments, veryHidden control, complex formulas, named ranges).
- Updated `SKILL.md` with the exact new description and full workflow you provided.
- Full pipeline now ends with a real `.xlsx` report (examples/report_pivot_macro.xlsx generated successfully in testing).

The skill now better matches the productized, report-generating vision while retaining useful low-level helpers (unpack, etc.).

## Latest Major Improvements (this session)

### 1. generate_report.py significantly enhanced
- 8+ professional sheets (Cover, Sheet Inventory, Formula Analysis, Issues & Warnings, Business Logic, Dependencies, Named Ranges, Recommendations)
- Professional formatting inspired by xlsx skill (blue headers, borders, severity color coding: red=high, yellow=medium, green=low)
- Clear note about integrating with xlsx skill's `recalc.py` for verified values
- Ready for future charts (structure already prepared)

### 2. Full Italian translation
- `SKILL.it.md` now contains the complete structured specification (new description + 4-phase workflow + script details) translated professionally.

### 3. Enhanced script details
- `formula_audit.py`: Added real (basic) dependency graph (cell-to-cell references) + improved function usage statistics.
- `extract_logic.py`: Much more sophisticated model type detection, financial pattern recognition, assumption heuristics, and risk indicators.

### 4. Tighter integration with xlsx recalc
- Added explicit recommendations in reports and workflow to run `xlsx/scripts/recalc.py` before analysis when verified values are needed.
- Future versions can consume recalculated files for value-based analysis.

All changes tested successfully on the rich `sample_pivot_macro_re.xlsx` (pivot simulation + macro area).

## New Features Added

### Direct support for pre-recalculated files (`--data-only`)
All analysis scripts (`inspect_xlsx.py`, `formula_audit.py`, `extract_logic.py`) now accept `--data-only`.
- When used, they load the workbook with `data_only=True` to read calculated values.
- In reports, you will see both `formula` and `value` for sampled cells.
- Best practice: Run `xlsx/scripts/recalc.py yourfile.xlsx` first, then use `--data-only`.

### New orchestrator: `run_full_analysis.py`
Single command to run the entire pipeline:

```bash
python scripts/run_full_analysis.py yourfile.xlsx \
  --output-dir ./my_analysis \
  --recalc \
  --data-only \
  --report-name MyReverseEngineeringReport.xlsx
```

Features:
- Optional recalc (tries to find xlsx skill's recalc.py)
- Automatic JSON artifact management
- Calls all 4 phases + report generation
- Supports `--data-only` end-to-end

### Demo "real file" test
A realistic small file (`examples/realistic_user_file.xlsx`) was created and successfully analyzed with the new runner.

To test with **your real file**:
```bash
python scripts/run_full_analysis.py /path/to/your/real-file.xlsx --data-only
```

(If you have run recalc.py on it beforehand, add `--data-only` for value verification.)

## Potenziamento con le nuove reference (scenes + engines)

I file forniti (SKILL.md avanzato + scenes/ + engines/) sono **estremamente utili** per migliorare e potenziare la skill.

**Cosa aggiungono:**
- Architettura scene-based (discover, deconstruct, document, audit-forensic, migrate, reconstruct)
- Engines specializzati (formula-tracer, vba-extractor, dependency-map, ooxml-structure)
- Workflow dettagliati, classificazioni di rischio, verification pipeline
- Separazione chiara quick vs deep analysis

**Integrazione fatta:**
- Cartelle `scenes/` e `engines/` popolate con le reference
- `run_full_analysis.py` ora supporta `--scene deconstruct`, `--scene audit-forensic`, `--scene full`, ecc.
- SKILL.md principale aggiornato con la versione avanzata (scene router + 5-phase workflow)
- Mantenuta compatibilità con i nostri script pratici (inspect/audit/extract/generate + data-only + runner)

La skill è passata da "buona suite di script" a "piattaforma forense modulare per reverse engineering di Excel".

Per usare le nuove scene:
```bash
python scripts/run_full_analysis.py file.xlsx --scene deconstruct --data-only
python scripts/run_full_analysis.py file.xlsx --scene audit-forensic
```

## Latest Potenziamento (from uploaded full spec + user analysis)

Integrated the complete scene/engine architecture from the provided documentation:

- **Auto scene selection** in `run_full_analysis.py` based on prompt keywords (e.g. "audit" → audit-forensic, "migrate" → migrate).
- **Verification pipeline** from `pipeline.md` implemented as `--verify` (completeness, accuracy, deliverable quality checks). Produces `*_verification.json` with PASS/NEEDS_REVIEW.
- **Formula Decomposer** new engine (`formula_decomposer.py`) implementing recursive breakdown of nested formulas (directly from formula-tracer.md and formula-patterns.md). Reduces opacity and enables semantic mapping.
- **Rich test workbook** `examples/complex_forensic_test.xlsx` created with:
  - 150 rows + Excel Table
  - Mega-nested formula with SUMPRODUCT + INDEX/MATCH
  - Hidden + veryHidden sheets
  - Macro simulation area with risk comments
  - Multiple named ranges (one hidden)

Full demo run with prompt-based auto-selection + verification + decomposition succeeded with perfect verification score (7/7).

The skill now has:
- Fallback awareness (documented)
- Scene/Engine modular structure (scenes/ + engines/ populated)
- Practical HA runner with verification
- Decomposition engine (first step toward semantic business logic extraction)

Next high-value items from the architect checklist (ready for implementation):
- Full openpyxl → ooxml_parser fallback chain in inspect
- Risk Heatmap in generate_report (table + severity colors)
- Deeper VBA static analysis + IOC extraction
