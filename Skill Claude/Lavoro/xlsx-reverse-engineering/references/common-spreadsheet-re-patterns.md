# Common Spreadsheet Reverse Engineering Patterns & Red Flags

This reference catalogs recurring idioms, obfuscation techniques, and security-relevant patterns found in real-world Excel files. Use during Phases 3-5 of the workflow.

## 1. Business Logic Idioms (Reconstruct These)

### Lookups & Joins
- `=VLOOKUP(A2, Rates!$A$2:$D$100, 3, FALSE)` or modern `XLOOKUP`
- `=INDEX(Rates!$C$2:$C$100, MATCH(A2, Rates!$A$2:$A$100, 0))`
- Pattern meaning: "Pull the tax rate / price / description for this key from a reference table."
- Often the "master data" lives on a hidden or separate sheet.

### Conditional / Branching Logic
- `=IF(A2>100, "High", IF(A2>50, "Medium", "Low"))`
- `=IFS(...)` or `SWITCH`
- Nested IFs → treat as decision tree / state machine.
- `=IFERROR(..., default)` → error handling / fallback.

### Aggregations with Criteria
- `SUMIFS`, `COUNTIFS`, `AVERAGEIFS`, `SUMPRODUCT((condition1)*(condition2)*values)`
- SUMPRODUCT is powerful and often used for matrix-style calculations or "hidden" filters.

### Running Totals / State
- `=SUM($B$2:B2)` (expanding range) — classic running balance.
- Circular references with iteration enabled (File > Options > Formulas > Enable iterative calculation) → intentional feedback loops (e.g., goal-seek simulations).

### Named Ranges as "Variables"
- `TaxRate` instead of hard-coded 0.21
- Hidden named ranges often store config, thresholds, or even small lookup tables.
- Can reference other sheets or contain formulas themselves.

## 2. Obfuscation & Anti-Analysis Techniques (Red Flags)

### Formula Obfuscation
- `=N(A1)` or `=T(A1)` — forces type conversion, sometimes used to hide values or break simple parsers.
- `=CHOOSE(..., encoded list)` or using `CODE`/`CHAR` to build strings dynamically.
- Extremely long nested formulas (hundreds of chars) — often auto-generated or deliberately hard to read.
- Using `INDIRECT` or `OFFSET` with constructed addresses (dynamic, hard to static-analyze).
- `=EVALUATE(...)` (old Excel 4.0 macro language, still works in some contexts) — extremely dangerous, can execute arbitrary code.

### Hiding Data & Logic
- **veryHidden sheets**: `state="veryHidden"` in workbook.xml. Cannot be unhidden via UI without VBA or XML edit. Frequently used for "secret" data, rates, or code.
- Hidden rows/columns containing intermediate calculations or source data.
- White text on white background or font size 1 for "invisible" labels.
- Data in comments or header/footer (rare but seen).
- Named ranges with `hidden="1"`.

### Protection as Obfuscation
- Sheet protection with password (often trivial to remove via XML edit: delete `<sheetProtection>` or set `password` attribute to empty).
- Workbook protection.
- "Lock" cells but allow selection — combined with hidden rows.

### Macro / Code Execution Vectors (.xlsm)
- `ThisWorkbook` or `Sheet` module with `Workbook_Open`, `Auto_Open`, `Auto_Close`.
- `Shell`, `CreateObject("WScript.Shell")`, `CallByName`, etc.
- DDE links (`=DDE(...)` or external links starting with `file://` or `http` in old formats).
- Embedded objects or ActiveX that auto-execute.

## 3. Security & Malware Patterns (Especially Relevant for Audits)

From security research (e.g., "Evil Excel", macro malware, data exfiltration):
- Very hidden sheet + auto-open macro that copies data or beacons.
- Formulas that construct PowerShell / cmd commands in cells then execute via VBA.
- External data connections that pull from attacker-controlled servers on refresh.
- Use of `WEBSERVICE` function (can make outbound HTTP).
- Long base64 or hex strings in cells (possible payloads).
- Conditional formatting that changes cell values or triggers side effects (rare).
- "Zero-day" style: abusing new Excel features (dynamic arrays, LAMBDA, Python in Excel) for obfuscation.
- Password-protected VBA projects (harder to inspect).

**Action**: Any of the above → elevate to `anomalies.md` with high priority. Recommend full VBA extraction + external static analysis.

## 4. Data Model Reconstruction Patterns

- Look for consistent "key" columns across sheets (customer ID, product SKU, date).
- Tables (ListObjects) often represent entities.
- Pivot tables reveal the "official" aggregated view the author cared about.
- Cross-sheet references with `SheetName!A1` style = module boundaries.
- "Input" sheets (blue cells per financial standards) vs "Calc" vs "Output".

## 5. Verification Heuristics

- After extracting a formula, always ask: "Does the post-recalc value match what the formula should produce for the sample inputs?"
- For a lookup: verify the source table actually contains the key being looked up.
- Circular refs: check if iteration is enabled in workbook settings.
- "Magic numbers" in formulas: trace back to named ranges or assumption cells (document their sources per xlsx skill financial standards).

## Recommended Search Patterns (when grepping XML or using Python)

```python
# Pseudocode for agent
suspicious = ["EVALUATE", "SHELL", "CreateObject", "WEBSERVICE", "INDIRECT", "OFFSET", "CALL"]
for cell in all_cells:
    if any(s in str(formula).upper() for s in suspicious):
        flag as anomaly
```

Use the bundled `analyze_anomalies.py` as a starting point and extend it with new patterns discovered during the engagement.

**Remember**: Most "clever" Excel files are not malicious — they are just the result of 15 years of organic growth by a non-programmer power user. Distinguish accidental complexity from intentional obfuscation.
