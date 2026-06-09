# Excel OOXML Reverse Engineering Quick Reference Guide

This is a focused cheat-sheet for low-level inspection of .xlsx/.xlsm files (which are ZIP archives of XML + binary parts). Use for hidden elements, protections, and anomalies that openpyxl may abstract away or not expose fully.

**Always start with unpacking** (see scripts/unpack_xlsx.py) or use `unzip -l file.xlsx` for quick listing.

## Critical Files & What to Look For (RE Priorities)

### 1. [Content_Types].xml
- Declares all parts and content types.
- Look for:
  - `application/vnd.ms-excel.sheet.macroEnabled.main+xml` → indicates .xlsm (VBA present)
  - Custom or unusual content types (potential payloads)

### 2. xl/_rels/workbook.xml.rels
- Relationships: how parts link.
- Key for:
  - `vbaProject.bin` (macro binary — high RE value)
  - External links / DDE
  - Custom XML parts
  - Printer settings, etc.

### 3. xl/workbook.xml (Workbook level — highest value for structure)
- `<sheets>` list:
  - `name`, `sheetId`, `r:id` (link to rels)
  - `state="hidden"` or `state="veryHidden"` (critical for obfuscated data/logic!)
- `<definedNames>` / `<definedName>`:
  - `name`, `hidden="1"`, `value` (can contain formulas or references)
  - Often used for "variables", constants, or hidden config.
- `<workbookProtection>` (password attributes — note: often weak/legacy)
- `<calcPr>` (calculation settings, iteration enabled?)
- File version, compatibility info.

### 4. xl/worksheets/sheetN.xml (per sheet — core logic & data)
- `<sheetData>`:
  - `<row r="..." hidden="1">` — hidden rows (data often stashed here)
  - `<c r="A1" t="s">` (shared string) or `t="str"` (formula string)
  - `<f>` element = the actual formula text (what you want for RE)
  - `<v>` = cached value (may be stale)
- `<sheetProtection>` (password, options for editing)
- `<sheetViews>` / `<sheetView>` for zoom, selection, etc.
- Conditional formatting: `<conditionalFormatting>` rules (can encode logic)
- Data validations: `<dataValidations>`
- Merged cells, outlines (grouping)
- `<tableParts>` for Excel Tables (ListObjects)

**Pro tip for formulas**: Search for `<f>` tags. Cross-reference with sharedStrings.xml for string values.

### 5. xl/sharedStrings.xml
- Centralized strings (including in formulas sometimes).
- Large files often have thousands of entries. Useful for finding labels, error messages, encoded data.

### 6. xl/styles.xml
- Number formats, fonts, fills, borders.
- Can reveal "hidden" formatting used for obfuscation or visual logic (e.g., white text on white bg).

### 7. xl/vbaProject.bin (only in .xlsm)
- OLE compound document containing the VBA project.
- **Cannot be easily parsed in pure Python without additional libs.**
- Workaround: Extract the binary blob. Then recommend external tools:
  - oletools / olebrowse
  - VBA Decompiler
  - pcode2code or similar
- Look in rels for its relationship ID.

### 8. Other High-Value Parts
- `xl/externalLinks/` + rels — external workbook references (DDE risks)
- `xl/pivotTables/`, `xl/pivotCaches/` — pivot definitions and cached data (can contain original source queries)
- `xl/charts/` — chart data series and formulas
- `xl/queryTables/` or `xl/connections.xml` — Power Query / data connections (refresh logic)
- `customXml/` or `docProps/` — custom metadata, sometimes used for config or payloads
- `xl/worksheets/_rels/sheetN.xml.rels` — per-sheet relationships (hyperlinks, etc.)

## Common RE Queries (Shell / Python)
```bash
# List everything
unzip -l file.xlsx | grep -E '\.xml$|\.bin$'

# Find hidden sheets quickly
unzip -p file.xlsx xl/workbook.xml | grep -o 'state="[^"]*"' 

# Extract all formulas (rough)
unzip -p file.xlsx 'xl/worksheets/*.xml' | grep -o '<f[^>]*>[^<]*</f>' | head -20

# Search for suspicious strings
unzip -p file.xlsx xl/sharedStrings.xml | grep -i 'exec\|cmd\|http\|powershell'
```

## Notes on Encryption / Protection
- Workbook/sheet passwords are **not strong crypto** in many cases (legacy hashing).
- Full file encryption (ECMA-376) is stronger but still attackable with tools if you have the password or legal right.
- When unpacking an encrypted file, many XML parts will be unreadable or the unzip will fail on encrypted streams.
- Always report exactly what was accessible.

## Version & Compatibility Flags
- Look in workbook.xml for `<fileVersion>`, app name, etc.
- Different Excel versions store certain features differently (e.g., dynamic arrays in newer).

**Rule**: When in doubt, unpack + inspect the raw XML. openpyxl is excellent for high-level but deliberately hides some "internal" details that are gold for reverse engineering.

Cross-reference with the `xlsx` skill's openpyxl usage for higher-level views.
