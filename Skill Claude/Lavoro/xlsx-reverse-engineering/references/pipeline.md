# Quality Pipeline — Verification Workflow for Reverse Engineering

## Overview

Every reverse engineering deliverable must be verified for completeness and accuracy before delivery. Unlike the xlsx skill's quality pipeline (which verifies created files), this pipeline verifies that our analysis and documentation are thorough and correct.

## Three-Phase Verification

### Phase 1: Completeness Check

Verify that all aspects of the spreadsheet have been analyzed:

- [ ] **All sheets accounted for** — including very hidden sheets
- [ ] **All named ranges documented** — including hidden ones
- [ ] **All cross-sheet references mapped** — no orphan references
- [ ] **All data validation rules cataloged** — every constraint
- [ ] **All conditional formatting rules captured** — every visual rule
- [ ] **All VBA macros extracted and documented** (if .xlsm)
- [ ] **All external connections identified**
- [ ] **All hidden content flagged** — hidden rows, columns, sheets, named ranges
- [ ] **All merged cells noted** — these affect formula behavior
- [ ] **All table objects identified** — with their columns and ranges

### Phase 2: Accuracy Check

Verify that our analysis is correct:

- [ ] **Formula counts match** — tool output vs spot-check
- [ ] **Named range references resolve** — each named range points to a valid range
- [ ] **Cross-sheet references are bidirectional** — if Sheet1 references Sheet2, Sheet2 should appear in the data flow
- [ ] **Sheet role classification is reasonable** — input sheets should have mostly values, calculation sheets should have mostly formulas
- [ ] **Data flow graph is consistent** — no impossible cycles (except intentional circular refs)
- [ ] **Risk assessment is proportionate** — HIGH findings are genuinely high risk

### Phase 3: Deliverable Quality Check

Verify the output meets the user's needs:

- [ ] **User's question is answered** — if they asked a specific question, it's answered directly
- [ ] **Interpretations are clearly labeled** — separate facts from analyst opinions
- [ ] **Actionable recommendations** — every risk has a recommended action
- [ ] **Appropriate detail level** — not too shallow, not overwhelming
- [ ] **Consistent language** — matches user's language throughout
- [ ] **No sensitive data exposed** — actual data values not reproduced unless requested

## Verification Commands

```bash
# Cross-check: discover sheet count vs deconstruct
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" discover <file> --pretty | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Sheets in discover: {d[\"complexity_metrics\"][\"sheet_count\"]}')"

# Cross-check: hidden content completeness
python3 "$RE_SKILL_DIR/scripts/ooxml_parser.py" <file> --pretty --section workbook | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f'Sheet: {s[\"name\"]}, State: {s[\"state\"]}') for s in d.get('workbook',{}).get('sheets',[])]"

# Cross-check: formula error scan using xlsx skill's audit tool
python3 "$XLSX_SKILL_DIR/xlsx.py" audit <file>
```

## Special Verification Cases

### Very Hidden Sheets
Very hidden sheets require OOXML access — openpyxl alone may not detect them. Always run `ooxml_parser.py` in addition to the main tools.

### VBA-Driven Values
Cells written by VBA appear as values (not formulas) but are actually computed. These create invisible dependencies. If VBA is present, cross-reference the VBA code with the cell values to identify VBA-written cells.

### Named Range Shadows
A workbook-level named range and a sheet-level named range can have the same name. The sheet-level one takes precedence on that sheet. Check for naming conflicts.

### External References
External file references may point to files that don't exist anymore. These will show as #REF! errors when opened but may show the last cached value in data_only mode. Check for these using the `audit-forensic` command.

## Output Quality Standards

### For Documentation Deliverables
- Every section has substantive content (no "TODO" or empty sections)
- Business logic is expressed in plain language, not just formula notation
- Risk ratings are justified with evidence
- Recommendations are specific and actionable

### For Migration Specifications
- Every input area has a target mapping
- Every formula has a target implementation approach
- VBA macros have explicit migration decisions (keep, replace, remove)
- Migration complexity is honestly assessed

### For Forensic Reports
- Findings are fact-based and verifiable
- Severity ratings follow the classification guide
- No exaggeration of risks for dramatic effect
- Clear separation of security findings from style/best-practice observations
