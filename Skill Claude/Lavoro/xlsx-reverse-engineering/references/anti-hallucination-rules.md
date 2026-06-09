# Anti-Hallucination & Provenance Rules for xlsx-reverse-engineering

Strict adherence to these rules is what separates reliable reverse engineering from casual summarization. Every output must follow this discipline.

## Mandatory Tagging System

For **every** claim, finding, conclusion, or reconstructed rule:

- `[Confirmed]`: Directly visible in the file artifact.
  - Must include precise source citation.
  - Example: `[Confirmed] Formula in Sheet1!C15 = "=SUM(B2:B14)" (openpyxl + xl/worksheets/sheet1.xml)`

- `[Inferred]`: Logically follows from 2+ Confirmed items with clear reasoning.
  - Cite the Confirmed sources.
  - Example: `[Inferred] The 'Effective Tax Rate' is pulled from the Rates sheet via INDEX/MATCH on column A (see Sheet1!C15 [Confirmed] and Rates!A2:D50 [Confirmed]).`

- `[Unknown]` or `[Assumption]`: Cannot be determined from the file alone.
  - Explicitly state what additional context would resolve it.
  - Example: `[Unknown] Purpose of the 'Control' sheet — appears to hold configuration but no documentation or usage found in formulas.`

- Never use vague language like "probably", "seems to", "I think it calculates..." without a tag.

## Citation Formats (Use Consistently)

1. **Cell references** (preferred when openpyxl can see it):
   - `SheetName!A1` or `SheetName!A1:B10` (range)
   - For data frames: `pandas index 4 (Excel row 5), column 'Revenue'`

2. **Raw OOXML** (when openpyxl abstracts or misses it):
   - `xl/workbook.xml:<sheet name="HiddenData" state="veryHidden" ...>`
   - `xl/worksheets/sheet3.xml:<row r="27" hidden="1">` (approximate line or use grep context)
   - `xl/worksheets/sheet1.xml:<f aca="1">=COMPLEX_FORMULA(...)</f>` (use exact substring)

3. **Named / Defined**:
   - `definedName "TaxRate" = 0.21 (workbook.xml)`
   - `named range "InputRange" refers to Sheet2!$A$2:$A$100`

4. **Script / Tool output**:
   - `recalc.py: total_errors=0, total_formulas=1247`
   - `inventory.py: sheet 'Calc' has 342 formulas`

5. **Cross-verification**:
   - "Value after recalc matches formula expectation: Sheet1!C15 = 12450 [Confirmed via data_only load]"

## Rules to Prevent Drift

- **Source of Truth Order** (when conflicting):
  1. Raw XML (lowest level)
  2. openpyxl structure (formulas, sheet states)
  3. Recalculated values (pandas / data_only)
  4. User-provided context (lowest — always flag as external)

- **When to mark [Unknown]**:
  - Business purpose / "why" (unless documented in comments or named ranges)
  - Intent behind complex nested formulas (you can describe *what* it does, not *why* the author chose it)
  - Behavior under edge cases not present in the data
  - External system integrations (what happens when the linked file is missing?)

- **Never**:
  - Invent plausible business rules ("This is probably the revenue forecast model...")
  - Assume a sheet name implies function ("The 'Data' sheet must be the source of truth")
  - Claim a formula "calculates X" without showing the formula + at least one verified input/output pair
  - Ignore discrepancies between formula text and cached value (flag them)

## Documentation in REVERSE-EXCEL.md

Every entry in the living document should follow this mini-template when adding findings:

```markdown
### Finding: <short title>

**Certainty**: [Confirmed] / [Inferred] / [Unknown]

**Source(s)**: 
- Sheet1!F22 formula: `=...`
- xl/workbook.xml line ~45: state="veryHidden"

**Observation**: ...
**Reconstructed Rule / Implication**: ...
**Verification**: Cross-checked against recalc output / sample row 12.
**Open Questions**: ...
```

## Self-Audit Checklist (Run at End of Major Phases)

Before marking a phase complete:
- [ ] All new findings have proper tags + citations.
- [ ] At least 3 random findings were spot-checked against raw source.
- [ ] No "probably" or "I believe" statements without tags.
- [ ] Discrepancies (e.g. formula vs value) are logged, not silently resolved.
- [ ] `REVERSE-EXCEL.md` task list was updated.
- [ ] Any [Unknown] items were added to the open questions / assumptions section.

## Interaction with xlsx Skill Patterns

When reusing xlsx skill guidance (financial color coding, formula best practices, etc.), treat those as *observations about the file's style* and cite the cells that follow (or violate) them. Do not impose new standards unless the task is to audit against a known template.

**Golden Rule**: If you cannot point to a specific cell, XML element, or script output as the origin of a statement, it does not belong in the final artifacts.

Violating these rules defeats the entire purpose of this skill. The agent must self-enforce ruthlessly.
