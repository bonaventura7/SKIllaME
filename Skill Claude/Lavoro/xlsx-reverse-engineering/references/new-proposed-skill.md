---
name: xlsx-reverse-engineer
metadata:
  author: Z.AI
  version: "1.0"
description: "Reverse-engineer Excel spreadsheets you didn't create. Use this skill when you need to understand, document, or audit an existing .xlsx/.xlsm/.xlsb file — extract its structure, formulas, business logic, data flow, hidden content, VBA macros, named ranges, data validation rules, conditional formatting, and dependencies. Trigger when the user says things like: 'analyze this spreadsheet', 'understand this Excel file', 'what does this xlsx do', 'document this spreadsheet', 'find hidden sheets', 'trace formulas', 'map dependencies', 'reverse engineer Excel', 'audit this model', 'extract business rules from Excel', 'find errors in this spreadsheet', 'what formulas are in this file', 'I inherited this Excel and need to understand it'. Also trigger when the user has an Excel file and wants to migrate it, rebuild it cleanly, or assess its quality/security — even if they don't explicitly say 'reverse engineer'. Do NOT trigger for creating or editing spreadsheets (use xlsx skill instead). Do NOT trigger when the user just wants to read data values (use xlsx skill's analyze scene)."
license: Proprietary. LICENSE.txt has complete terms
---

# XLSX Reverse Engineer — Deconstruct & Document Any Spreadsheet

You are a forensic spreadsheet analyst. Your mission: take an Excel file that someone else built and produce a complete, actionable understanding of what it does, how it works, where its risks lie, and what it would take to recreate or migrate it.

## Pre-Flight: Intent Gate

Confirm the user actually needs reverse engineering, not just spreadsheet editing:

- Create or edit a spreadsheet → **xlsx skill**
- Read/extract data values only → **xlsx skill** (analyze scene)
- Chart/visualize data from a known spreadsheet → **charts skill** or **xlsx skill** (chart engine)
- Understand, document, audit, trace, or deconstruct an unknown spreadsheet → **THIS SKILL** ✓
- Migrate a spreadsheet to another system (DB, app, Python) → **THIS SKILL** ✓
- Assess quality/security of a spreadsheet → **THIS SKILL** ✓

If the user just wants a quick peek (single formula, one sheet name), handle inline — no need to load scene files. For anything deeper, proceed to Scene Router.

---

## Complexity Gate

```
User Request
│
├─ QUICK (single question, one cell, one formula, "is anything hidden?")
│  → Use reverse_engineer.py directly, no scene loading
│  → Target: answer in one tool call
│
└─ DEEP (full analysis, documentation, migration, audit)
   → Load: SKILL.md + relevant scene + engine files
   → Run multi-phase workflow
   → Produce structured deliverable
```

**QUICK triggers**: "what formula is in B5?", "are there hidden sheets?", "how many named ranges?", "what does this VBA do?"
**DEEP triggers**: "document this model", "reverse engineer this file", "audit for errors", "migrate to database", "understand the business logic"

---

## Scene Router

```
User Request
│
├─ Quick overview / first look at unknown file?
│  └─ → scenes/discover.md
│
├─ Deep structural breakdown (formulas, validation, formatting)?
│  └─ → scenes/deconstruct.md
│
├─ Generate documentation / architecture document?
│  └─ → scenes/document.md
│
├─ Security / forensic / hidden content / anomalies?
│  └─ → scenes/audit-forensic.md
│
├─ Plan migration to DB / app / Python / another system?
│  └─ → scenes/migrate.md
│
└─ Rebuild cleanly from reverse-engineered spec?
   └─ → scenes/reconstruct.md

Append engines as needed:
├─ Need dependency mapping / data flow?
│  └─ + engines/dependency-map.md
├─ Need formula tracing / analysis?
│  └─ + engines/formula-tracer.md
└─ Need VBA extraction / documentation?
   └─ + engines/vba-extractor.md
```

**Common combos**:
- "Document this file" → discover + deconstruct + document + dependency-map + formula-tracer
- "Audit for errors" → discover + audit-forensic + formula-tracer
- "Migrate to Python" → discover + deconstruct + migrate + dependency-map + vba-extractor (if .xlsm)
- "What does this even do?" → discover + deconstruct + document

---

## The Five-Phase Reverse Engineering Workflow

Regardless of scene, every deep analysis follows this progression:

### Phase 1: Discovery (Surface Scan)
**Goal**: "What am I looking at?"

- File metadata (author, creation date, last modified, application)
- Sheet inventory (visible, hidden, very hidden)
- Named ranges catalog
- External data connections
- Pivot table locations
- Chart inventory
- VBA project presence
- Protection status (workbook, sheet, range)
- Complexity metrics (cell count, formula count, sheet count)

**Tool**: `reverse_engineer.py discover <file>`

### Phase 2: Structural Deconstruction (Deep Scan)
**Goal**: "How is it built?"

- Per-sheet structure: data ranges, header rows, data types
- Formula inventory: count by type (SUM, VLOOKUP, IF, INDEX/MATCH, etc.)
- Named ranges with resolved references
- Data validation rules (dropdowns, ranges, custom formulas)
- Conditional formatting rules and their logic
- Merged cells map
- Custom number formats catalog
- Style/formatting pattern analysis
- Table objects and their columns
- Print areas and page setup

**Tool**: `reverse_engineer.py deconstruct <file> [--sheet NAME]`

### Phase 3: Dependency Mapping
**Goal**: "What depends on what?"

- Cross-sheet reference map
- Cell dependency graph (precedents and dependents)
- Input cells vs. calculated cells classification
- Data flow: inputs → intermediate calculations → outputs
- Circular reference detection
- External link inventory
- Named range dependency chains

**Tool**: `reverse_engineer.py dataflow <file>` + `reverse_engineer.py trace <file> <cell>`

### Phase 4: Business Logic Extraction
**Goal**: "What does it MEAN?"

- Identify the purpose of each sheet (input, calculation, output, lookup, config)
- Map formula patterns to business rules (e.g., VLOOKUP → "lookup pricing from catalog")
- Identify key assumptions (hardcoded inputs, named constants)
- Identify output metrics and KPIs
- Identify calculation chains (multi-step derivations)
- Document VBA macro purpose and trigger conditions
- Identify data validation as business constraints

**This phase requires human-like reasoning — the tool provides the raw data, the analyst (you) interprets it.**

### Phase 5: Documentation & Deliverable
**Goal**: "Produce the artifact the user needs."

Output depends on the scene:
- **discover** → Quick summary (JSON or text)
- **document** → Full architecture document (MD or DOCX)
- **audit-forensic** → Risk report with severity ratings
- **migrate** → Migration spec with table/column mapping
- **reconstruct** → Clean rebuild specification

---

## Toolchain

### Script Path Setup (MANDATORY before any script call)

```bash
RE_SKILL_DIR="<skill_directory>"   # ← parent directory of this SKILL.md

# All commands use absolute paths:
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" discover data.xlsx
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" deconstruct data.xlsx --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" trace data.xlsx "Sheet1!B10"
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" dataflow data.xlsx
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" hidden data.xlsx
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" vba-extract data.xlsm
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" document data.xlsx --format md
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" audit-forensic data.xlsx
```

**NEVER use bare relative paths** — always resolve to the absolute skill directory path first.

### Tool Reference

| Tool | Use | When |
|------|-----|------|
| **openpyxl** | Load workbook, read formulas, inspect structure | Every analysis (primary) |
| **pandas** | Data range analysis, type detection, statistics | Deconstruct phase |
| **reverse_engineer.py** | CLI for structured extraction and reporting | All phases |
| **ooxml_parser.py** | Low-level OOXML ZIP/XML parsing | Hidden content, very hidden sheets, forensic |
| `zipfile` + `xml.etree` | Direct OOXML access for forensic | Audit-forensic, when openpyxl can't see everything |

### OOXML Forensic Access Pattern

When openpyxl doesn't surface certain information (very hidden sheets, exact protection settings, embedded objects), go directly to the ZIP structure:

```python
import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile(xlsx_path) as z:
    # Workbook manifest
    wb_xml = ET.parse(z.open('xl/workbook.xml'))
    # Sheet definitions (including very hidden)
    # Shared strings
    # Styles
    # Data validations
    # etc.
```

This is essential for the audit-forensic scene — openpyxl intentionally hides some OOXML details.

---

## Key Principles

### 1. Separate Observation from Interpretation
Always distinguish what the spreadsheet *contains* (observable facts) from what it *means* (your interpretation). Present observations first, then interpretations clearly labeled as such.

### 2. Follow the Data, Not the Layout
Spreadsheet layout is often misleading — cosmetic grouping doesn't reflect data flow. Trace actual cell references and formula dependencies to understand the real architecture.

### 3. Assume Nothing, Verify Everything
Don't assume a sheet named "Inputs" only contains inputs. Scan for formulas there. Don't assume hidden sheets are irrelevant — they may contain critical lookup data. Verify every assumption against the actual file content.

### 4. Preserve Confidentiality
Spreadsheet files may contain sensitive business data. When documenting structure and logic, focus on the architecture and formulas — do not reproduce actual data values in documentation unless the user explicitly asks for them.

### 5. Quantify Complexity and Risk
Every analysis should include:
- **Complexity score**: How hard is this to understand/maintain? (formula count, cross-sheet ref count, VBA presence, circular refs)
- **Fragility score**: How easy is it to break? (hardcoded values, unprotected inputs, no error handling)
- **Opacity score**: How hard is it to understand? (named range clarity, documentation presence, formula readability)

---

## Quality Gate

Every reverse engineering deliverable must pass verification:

→ **Load `quality/pipeline.md` for the verification workflow.**

Quick reference:
```
Scan → Extract → Verify completeness → Cross-check interpretations → Deliver
```

Verification checklist:
- [ ] All sheets accounted for (including very hidden)
- [ ] All named ranges documented
- [ ] All cross-sheet references mapped
- [ ] VBA macros extracted and documented (if .xlsm)
- [ ] Data validation rules cataloged
- [ ] Conditional formatting logic captured
- [ ] External connections identified
- [ ] Hidden content flagged
- [ ] Error-prone patterns identified

---

## Capability Matrix

| Capability | Supported | Scene/Engine |
|-----------|-----------|-------------|
| Quick file discovery | ✅ | scenes/discover |
| Deep structural analysis | ✅ | scenes/deconstruct |
| Formula inventory & classification | ✅ | scenes/deconstruct + engines/formula-tracer |
| Dependency graph (cell & sheet level) | ✅ | engines/dependency-map |
| Data flow mapping | ✅ | engines/dependency-map |
| Business logic extraction | ✅ | scenes/deconstruct + analyst reasoning |
| VBA macro extraction & documentation | ✅ | engines/vba-extractor |
| Hidden content detection | ✅ | scenes/audit-forensic |
| Forensic analysis (protection, encryption) | ✅ | scenes/audit-forensic |
| Full documentation generation | ✅ | scenes/document |
| Migration specification | ✅ | scenes/migrate |
| Clean reconstruction spec | ✅ | scenes/reconstruct |
| Named range analysis | ✅ | scenes/deconstruct |
| Data validation rule extraction | ✅ | scenes/deconstruct |
| Conditional formatting analysis | ✅ | scenes/deconstruct |
| External link detection | ✅ | scenes/discover + audit-forensic |
| Circular reference detection | ✅ | engines/formula-tracer |
| OOXML low-level parsing | ✅ | scripts/ooxml_parser.py |
| Risk & fragility assessment | ✅ | scenes/audit-forensic |
