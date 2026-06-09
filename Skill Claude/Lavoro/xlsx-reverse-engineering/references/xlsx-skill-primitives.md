# xlsx Skill Primitives — Safe Reuse for Reverse Engineering

This skill is designed to **compose with** (not replace) the official `xlsx` skill from anthropics/skills.

Extracted and adapted key patterns that are safe and valuable during reverse engineering work. Always prefer these battle-tested approaches over reinventing.

## 1. Library Selection (from xlsx SKILL.md)

- **openpyxl** — Use for **everything involving formulas, formatting, structure, and precise cell access**.
  - Load: `load_workbook(path, data_only=False)` → preserves formulas exactly (critical for RE).
  - Load for values: `load_workbook(path, data_only=True)` **ONLY after running recalc**.
  - Warning (repeated from xlsx): If you save with `data_only=True`, formulas are **permanently lost**.
  - Large files: `read_only=True` (for reading) or `write_only=True`.
  - Cell coordinates are 1-based.

- **pandas** — Best for **data profiling, bulk operations, statistics, and quick overviews**.
  - `pd.read_excel(path, sheet_name=None)` → dict of all sheets.
  - Always specify `dtype` for IDs/dates to avoid inference bugs.
  - Map back to Excel rows: remember DataFrame index 0 = Excel row 1 (or adjust for headers).

**Rule for this RE skill**: Use openpyxl for logic extraction. Use pandas for value distribution analysis. Never mix in a way that loses formula information.

## 2. Formula Discipline (Critical for Accurate RE)

From xlsx:
- Excel files created/modified by openpyxl contain formulas as strings but **not calculated values**.
- **Always** use the provided recalc mechanism before trusting values.
- Prefer Excel formulas over Python calculations when the goal is to understand the *original* model.

In RE context:
- Extract the raw formula string first (`[Confirmed]`).
- Then (after recalc) compare the computed value.
- Discrepancies = interesting findings (stale cache? circular? error?).

## 3. Recalculation (Use the Existing Script)

```bash
python /path/to/xlsx/scripts/recalc.py input.xlsx [timeout_seconds]
```

The script:
- Sets up LibreOffice macro if needed.
- Runs `calculateAll()`.
- Returns JSON:
  ```json
  {
    "status": "success" | "errors_found",
    "total_errors": 0,
    "total_formulas": 1247,
    "error_summary": { "#REF!": { "count": 2, "locations": ["Sheet1!B5", ...] } }
  }
  ```
- Also scans for all standard Excel errors.

**In this RE skill**: Treat a successful recalc as a major verification gate. Log the `total_formulas` and any errors prominently in `REVERSE-EXCEL.md`.

If the environment lacks LibreOffice, document it and fall back to formula-text-only analysis.

## 4. Reading & Editing Existing Files (Inspection Mode)

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')  # data_only=False by default for formulas
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    # ws.sheet_state → 'visible', 'hidden', or 'veryHidden' (very useful for RE!)
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                # This is a formula — gold for logic extraction
                print(f"{sheet_name}!{cell.coordinate}: {cell.value}")
```

**RE-specific tips**:
- `ws.sheet_state` and `ws.sheet_properties` give visibility info.
- `wb.defined_names` → all named ranges (check `.attr_text` and hidden status).
- For very large sheets: iterate with limits or use `ws.iter_rows(min_row=..., max_row=...)`.

## 5. Professional / Financial Model Conventions (Useful Context)

Even during pure RE, note whether the file follows (or violates) these:
- Blue text = inputs
- Black = formulas
- Green = cross-sheet internal links
- Red = external links
- Yellow bg = key assumptions
- Specific number formats, source documentation comments next to hardcodes.

These observations help reconstruct the *author's intent* and quality of the model.

## 6. Common Pitfalls to Watch For (RE Lens)

- Row offset errors: pandas row 5 ≈ Excel row 6 (with header).
- Formula references that look wrong but are correct for the author's layout.
- Cached values that are stale (recalc will surface this).
- Multiple sheets with similar names or data (duplication vs intentional separation).
- Far-right columns or very deep rows (often overlooked in manual review).

## 7. When to Hand Off to xlsx Skill

During an RE engagement you may discover the need to:
- Create a "clean" version of a sheet for comparison.
- Fix obvious formula errors to enable better analysis.
- Export data to a new model.

In those cases: explicitly switch context and say "Switching to xlsx skill to [specific task]".

## Summary for This Skill

- **openpyxl + data_only=False** = your primary lens for "source code" (formulas).
- **recalc.py** = your verifier for "runtime" behavior.
- **pandas** = your data profiler.
- **Raw OOXML unpack** (our scripts) = your assembly-level / hidden feature inspector.

Use the above primitives wherever they accelerate reliable extraction. Do not re-implement what the xlsx skill already does well.

When writing any ad-hoc Python during the engagement, follow the xlsx code style guidelines: minimal, concise, no unnecessary prints or comments in the code itself.
