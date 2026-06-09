# Reference: OOXML File Structure

## Overview

Excel .xlsx files are actually ZIP archives containing XML files following the Office Open XML (OOXML) standard (ECMA-376). Understanding this structure is essential for forensic analysis and accessing data that openpyxl may not expose.

## ZIP Archive Structure

```
[Content_Types].xml          ← MIME type registry for all parts
_rels/.rels                  ← Root relationships
docProps/
  app.xml                     ← Application properties (company, links, sheets count)
  core.xml                    ← Core properties (author, dates, revision)
  custom.xml                  ← Custom properties (user-defined metadata)
xl/
  workbook.xml                ← Workbook definition (sheets, named ranges, protection)
  _rels/workbook.xml.rels     ← Workbook relationships
  sharedStrings.xml           ← Shared string table (all text values)
  styles.xml                  ← Cell styles, formats, fonts, fills
  connections.xml             ← External data connections
  calcChain.xml               ← Calculation order chain
  vbaProject.bin              ← VBA binary (only in .xlsm)
  workbook.bin                ← Workbook binary (only in .xlsb)

  worksheets/
    sheet1.xml                ← Individual sheet data (cells, formulas, values)
    sheet2.xml
    ...
    _rels/
      sheet1.xml.rels         ← Per-sheet relationships (charts, drawings)

  charts/
    chart1.xml                ← Chart definitions
    chart2.xml

  drawings/
    drawing1.xml              ← Drawing layer (shapes, images, embedded objects)

  media/
    image1.png                ← Embedded images
    image2.jpg

  theme/
    theme1.xml                ← Theme definition

  embeddings/
    oleObject1.bin            ← Embedded OLE objects
    Microsoft_Excel_Worksheet.xlsx  ← Embedded workbooks

  pivotCache/
    pivotCacheDefinition1.xml ← Pivot cache definitions
    pivotCacheRecords1.xml    ← Pivot cache records

  printerSettings/
    printerSettings1.bin      ← Print configuration

  threadedComments/
    threadedComment1.xml      ← Threaded comments (newer Excel versions)

  worksheetsMetadata/
    metadata.xml              ← Cell metadata

customXml/
  item1.xml                   ← Custom XML data parts
  itemProps1.xml
  _rels/

xl/metadata/
  metadata.xml                ← Rich data metadata
