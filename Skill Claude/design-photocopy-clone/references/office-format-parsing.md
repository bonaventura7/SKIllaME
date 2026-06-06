# Office Open XML Format Parsing Guide (for design-photocopy-clone)

## Overview
All .pptx, .xlsx, .docx files are ZIP archives (Office Open XML / OOXML standard). 
The canonical way to extract design data without proprietary libraries is:
1. Unzip the archive (use `unzip -l` for listing, or Python zipfile).
2. Parse key XML files using XML tools (lxml, xml.etree.ElementTree, or even grep/sed for quick wins).
3. Resolve relationships via .rels files.
4. Map internal IDs to human-readable elements.

**Always start here** for the structural path. This gives exact positions, styles, and hierarchy before any visual approximation.

## Universal Structure
- `[Content_Types].xml` — Declares all parts and their content types.
- `_rels/.rels` — Top-level relationships (points to ppt/, xl/, word/, docProps/).
- `docProps/core.xml` + `app.xml` — Metadata (author, title, slide count, etc.).

## PowerPoint (.pptx) Specific
- `ppt/presentation.xml` — Presentation-level settings, slide size (sldSz in EMUs), slide master IDs.
- `ppt/slides/slideN.xml` — Individual slide content.
  - `<p:sp>` or `<p:pic>` or `<p:grpSp>` : Shapes, pictures, groups.
  - `<p:txBody>` : Text body containing `<a:p>` paragraphs and `<a:r>` runs.
  - `<a:off x="..." y="..."/>` and `<a:ext cx="..." cy="..."/>` : Position and size (in EMUs: 914400 EMU = 1 inch).
  - `<a:solidFill><a:srgbClr val="1A365D"/></a:solidFill>` : Colors (direct hex or theme reference via a:schemeClr).
  - `<a:latin typeface="Calibri"/>` + `<a:cs .../>` for fonts.
  - `<a:effectLst>` for shadows, glows, etc.
- `ppt/slideMasters/slideMaster1.xml` and `slideLayouts/` — Master styles and placeholders. Inherit from here for consistent design.
- `ppt/theme/theme1.xml` — Color scheme (dk1, lt1, accent1-6, etc.), font scheme, format scheme.
- `ppt/_rels/slideN.xml.rels` — Links to images, charts, etc. in media/ or charts/.
- Animations: `ppt/slides/_rels/` or timing in slide XML (p:timing).

**Parsing Tip**: Search for `a:off` and `a:ext` to get every positioned element. Text is under `a:t` tags inside runs.

**EMU to cm conversion**: EMU / 360000 = cm (since 914400 EMU/inch, 2.54 cm/inch → 360000 EMU/cm).

## Excel (.xlsx) Specific
- `xl/workbook.xml` — Sheet names, order, defined names.
- `xl/worksheets/sheetN.xml` — Cell data, merged cells, column widths, row heights, drawings.
  - `<c r="A1">` cells with `<v>` value or shared string index.
  - `<c r="A1" s="2">` style index (points to styles.xml).
  - `<mergeCells>` for merged ranges.
- `xl/styles.xml` — Cell styles (fonts, fills, borders, number formats, alignments). Very rich for design.
  - `<font>` with name, size, color, bold, etc.
  - `<fill>` with pattern or gradient.
  - `<border>` left/right/top/bottom styles.
- `xl/drawings/drawingN.xml` + `xl/charts/` for embedded charts and images (positions in twoCellAnchor or oneCellAnchor).
- `xl/theme/theme1.xml` — Same as PPT.
- Shared strings in `xl/sharedStrings.xml` for text optimization.

**Design extraction focus**: Column widths (in characters or cm), row heights (in points), cell styles per range, chart visual properties (separate chart XML has series colors, plot area, etc.).

## Word / PDF (.docx) Specific
- `word/document.xml` — Main content.
  - `<w:p>` paragraphs (with `<w:pPr>` properties: spacing, alignment, indentation).
  - `<w:r>` runs with `<w:rPr>` (font, color, bold).
  - `<w:tbl>` tables with `<w:tr>`, `<w:tc>` cells, cell properties (tcW width, shading, borders).
  - Floating objects via `<w:drawing>` or `<w:pict>` with position (wp:posOffset or simple positioning).
- `word/styles.xml` — Paragraph and character styles.
- `word/theme/theme1.xml`.
- Sections in `w:sectPr` (page size, margins, headers/footers).

**PDFs**: No XML. Convert to images or use OCR + layout analysis tools. Treat primarily as visual source.

## Recommended Extraction Sequence (for scripts)
1. Unzip to temp dir or stream.
2. Read [Content_Types].xml to confirm type.
3. Read top .rels to find presentation.xml / workbook.xml / document.xml.
4. Parse theme for color palette first (critical for fidelity).
5. Parse main content file, walking the element tree.
6. For each positioned element collect:
   - type
   - id (or generate stable one)
   - position (convert EMU → cm or px)
   - style (fill, line, font, effects)
   - content
7. Resolve any rId references to actual media or charts.
8. Cross-reference with visual data later.

## Tools & Commands (Agent Can Run)
- `unzip -l file.pptx | head -30` (structure overview)
- `unzip -p file.pptx ppt/slides/slide1.xml | head -c 5000` (peek content)
- Python: `zipfile`, `xml.etree.ElementTree` (stdlib), or install `lxml` if needed for robustness.
- For quick color extraction: grep for `srgbClr val=`

## Limitations & Workarounds
- Binary blobs (embedded objects, some charts) require additional handling or visual fallback.
- Some advanced features (VBA, custom XML) ignored for design focus.
- Theme color resolution: Always resolve to concrete hex when possible by looking up in theme.
- Large files: Stream parse or extract only first N slides for initial analysis.

Use this guide in combination with the visual path for HA results. Structural gives the "why" and editability; visual gives the "what it actually looks like on screen".
