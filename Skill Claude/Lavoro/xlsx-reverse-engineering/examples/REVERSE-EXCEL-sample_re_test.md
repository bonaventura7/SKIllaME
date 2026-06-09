# REVERSE-EXCEL.md - sample_re_test.xlsx

**File**: `examples/sample_re_test.xlsx`
**Started**: 2026-06-09
**Status**: Complete (demo run)

## File Metadata
- Size: ~8KB
- Sheets: 3 (MainCalc visible, HiddenRates hidden, SecretConfig veryHidden)
- Has macros: No
- Recalc performed: No (demo without LibreOffice values)

## High-Level Summary
This is a synthetic test workbook designed to exercise reverse engineering patterns:
- Visible calculation sheet with expanding formulas and cross-sheet potential.
- Hidden sheet containing rates (classic obfuscation).
- **veryHidden** sheet with "secret" configuration (high-value RE target).
- Mix of visible and hidden named ranges.
- Obfuscation example using `INDIRECT` + `N()`.
- Cross references and potential external link simulation.

## Task Checklist
- [x] Phase 0: Intake & Bootstrap (inventory.py)
- [x] Phase 1: Structural Archeology (unpack + hidden detection)
- [x] Phase 2: Data Archeology (structure only in this demo)
- [x] Phase 3: Formula & Logic Decompilation (extract_formulas.py)
- [x] Phase 4: Advanced Features
- [x] Phase 5: Anomaly & Security Analysis (analyze_anomalies.py detected veryHidden + INDIRECT)
- [x] Phase 6: Synthesis (graph + findings)
- [x] Phase 7: Verification (verify.py)
- [x] Final Executive Summary

## Key Findings (with tags)

### Finding 1: Very Hidden Configuration Sheet
**Certainty**: [Confirmed]
**Source(s)**: inventory.py (state="veryHidden"), unpacked xl/workbook.xml
**Observation**: Sheet "SecretConfig" is marked veryHidden and contains "MasterKey" and "Threshold" values.
**Reconstructed Rule**: Likely holds sensitive thresholds or config not meant to be visible to normal users.
**Verification**: Confirmed via both openpyxl sheet_state and raw XML.

### Finding 2: Hidden Named Range for Tax Rate
**Certainty**: [Confirmed]
**Source(s)**: inventory.py + defined names scan
**Observation**: "TaxRateHidden" points to HiddenRates!$B$1 and is marked hidden.
**Reconstructed Rule**: The tax rate is intentionally hidden from the normal UI/defined name list.

### Finding 3: Obfuscated Formula using INDIRECT + N
**Certainty**: [Confirmed]
**Source(s)**: MainCalc!G2 formula `=N(INDIRECT("B"&6))`
**Observation**: Uses two common obfuscation techniques together.
**Reconstructed Rule**: Attempts to dynamically reference and type-convert a value (common in both legitimate complex models and malicious files).

### Finding 4: Expanding Year-over-Year Growth
**Certainty**: [Confirmed]
**Source(s)**: MainCalc!B6:B10 formulas using `=B{prev}*(1+$B$2)`
**Reconstructed Rule**: Standard compound growth model starting from B1 input with B2 as rate. Clean and maintainable pattern.

## Open Questions / Assumptions
- Purpose of the "SecretConfig" sheet is unknown without business context.
- Whether the INDIRECT pattern is intentional obfuscation or legacy workaround.

## Recommendations
- Review the veryHidden sheet contents manually (it may contain more data than sampled).
- Consider removing or documenting hidden named ranges before migration.
- Replace the INDIRECT obfuscation with direct references if possible.

## Next Actions
1. Run with actual recalc (if LibreOffice available) to verify values.
2. Extract full formulas from the veryHidden sheet.
3. Build Mermaid dependency graph for the MainCalc sheet.

---
*Demo run with synthetic file created for skill validation.*
