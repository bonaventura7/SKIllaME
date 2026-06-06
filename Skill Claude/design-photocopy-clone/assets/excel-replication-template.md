# Excel Recreation Instructions Template

**Source**: [blueprint meta.sourceFiles]
**Target**: New blank Excel workbook

## Global Setup
1. Open Microsoft Excel (or compatible, e.g. Google Sheets with limitations, LibreOffice).
2. File > New > Blank Workbook.
3. Page Layout > Size > A4 or Letter, Orientation Landscape if original was (match blueprint dimensions where relevant for print).
4. View > Ruler, View > Gridlines, View > Page Break Preview for reference.
5. (Optional) Set workbook theme colors to match blueprint.globalStyles.themeColors.

## Per-Sheet Instructions

### Sheet 1: [Sheet Name or "Dashboard"]
**Page Setup** (if print-critical):
- Page Layout > Print Area: select the used range.
- Page Layout > Margins > Custom (match original if known).
- Page Layout > Orientation and Scaling.

**Column & Row Setup**:
- Set column widths (in cm or characters): 
  - Column A: 3.50 cm (or 12 characters)
  - Column B: ...
- Set row heights (in points or cm):
  - Row 1: 25 pt
  - etc.

**Background / Title Area** (if full-sheet styling):
- Select the entire used range or specific header rows.
- Home > Fill Color: #[HEX] for solid backgrounds.
- Or add a large rectangle shape (Insert > Shapes) behind data for colored header bands.

**Data & Tables**:
- Enter all values exactly as in blueprint (numbers, text, dates).
- For formulas: Enter the exact formula in the cell (e.g. =SUM(B2:B10)). Do not paste values.
- Apply cell styles:
  - Select range > Home > Font: family, size pt, Bold, Color #[HEX].
  - Fill: Pattern or solid #[HEX].
  - Border: All borders or specific sides, weight, color.
  - Alignment: Horizontal [Left/Center/Right], Vertical [Top/Middle/Bottom], Wrap text, Merge cells (select range > Merge & Center).
- For tables: Select data range > Insert > Table (or Ctrl+T). Then Table Design tab to apply banded rows, header style, etc.

**Charts**:
- Select data range for the chart.
- Insert > Charts > [Bar / Line / Pie / Combo] (match blueprint chartType).
- Move and resize chart to exact position (use Format > Size).
- Format:
  - Right-click chart > Format Data Series: fill colors per series from blueprint.
  - Chart Title, Legend, Axes, Gridlines: match styles, colors, fonts.
  - Data labels: show/hide, position, font.

**Images / Shapes** (floating):
- Insert > Pictures or Shapes.
- Position precisely using the Format tab (Size & Properties > Position > Horizontal/Vertical absolute).
- Apply fills, lines, effects to shapes as per blueprint elements.

**Conditional Formatting** (if present):
- Home > Conditional Formatting > New Rule.
- Match the rules from original (color scales, icon sets, data bars, formula-based).

## Additional Sheets
Repeat the column/row setup + data population pattern.
Use consistent styling across sheets for repeating elements (e.g. header rows always use the same fill and font).

## Named Ranges & Defined Names (if used in original)
- Formulas > Name Manager > Define names exactly as extracted.

## Final Polish & Verification
- Freeze panes if original had them (View > Freeze Panes).
- Print preview and adjust to match original printed appearance.
- Save as .xlsx.
- For fidelity check: Compare cell-by-cell values + visual styles. Use "View > New Window" + "Arrange All > Vertical" for side-by-side.

**Formulas & Data Integrity Notes**:
- All formulas from blueprint must be entered verbatim.
- If data is large, consider linking to a data sheet or external source.

**Workarounds**:
- If exact font unavailable, use closest and note substitution.
- For very complex conditional formatting or pivot tables, recreate the visual result and document the source data.

This produces a fully functional, editable Excel workbook with photocopy-grade visual and structural fidelity.
