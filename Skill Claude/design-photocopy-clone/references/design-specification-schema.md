# Design Blueprint Specification (Canonical Output Format)

This is the single source of truth for all replicas produced by design-photocopy-clone.

Use the JSON schema below (or equivalent YAML). Every replication output (HTML, instructions, generators) MUST be derived directly from this blueprint to guarantee consistency.

## Top-Level Structure

```json
{
  "meta": {
    "version": "1.0",
    "sourceFiles": ["quarterly-review.pptx"],
    "extractedAt": "2026-06-06T10:30:00Z",
    "slideOrPageDimensions": {
      "width": 33.87,
      "height": 19.05,
      "unit": "cm",
      "originalUnit": "EMU"
    },
    "totalPages": 12,
    "overallConfidence": 91,
    "extractionMethodsUsed": ["structural", "visual"],
    "notes": "Brand colors resolved from theme. Some fonts substituted."
  },
  "globalStyles": {
    "themeColors": {
      "dk1": "#000000",
      "lt1": "#FFFFFF",
      "accent1": "#1A365D",
      "accent2": "#2B6CB0",
      "hyperlink": "#0563C1"
    },
    "fontScheme": {
      "major": "Calibri Light",
      "minor": "Calibri"
    },
    "defaultTextStyle": {
      "fontFamily": "Calibri",
      "sizePt": 18,
      "color": "#333333"
    }
  },
  "pages": [
    {
      "pageId": "slide-01",
      "pageNumber": 1,
      "type": "title-slide",
      "title": "Q2 2026 Results",
      "background": {
        "type": "solid",
        "color": "#1A365D",
        "opacity": 1.0
      },
      "elements": [
        {
          "id": "title-text-01",
          "type": "text",
          "zIndex": 10,
          "position": {
            "x": 2.54,
            "y": 5.08,
            "width": 28.78,
            "height": 4.0,
            "unit": "cm",
            "rotation": 0
          },
          "style": {
            "fontFamily": "Calibri Light",
            "fontSizePt": 54,
            "fontWeight": "bold",
            "color": "#FFFFFF",
            "textAlign": "center",
            "verticalAlign": "middle",
            "lineHeight": 1.1
          },
          "content": {
            "plainText": "Q2 2026 Results",
            "runs": [
              {"text": "Q2 2026 Results", "bold": true, "color": "#FFFFFF"}
            ]
          },
          "confidence": 95,
          "methods": ["structural", "visual"]
        },
        {
          "id": "subtitle-text-01",
          "type": "text",
          "zIndex": 9,
          "position": { "x": 2.54, "y": 10.16, "width": 28.78, "height": 2.0, "unit": "cm" },
          "style": {
            "fontFamily": "Calibri",
            "fontSizePt": 24,
            "color": "#E2E8F0",
            "textAlign": "center"
          },
          "content": { "plainText": "Strategic Overview & Financial Highlights" },
          "confidence": 92,
          "methods": ["structural"]
        },
        {
          "id": "accent-bar-01",
          "type": "shape",
          "shapeType": "rectangle",
          "zIndex": 5,
          "position": { "x": 0, "y": 17.5, "width": 33.87, "height": 1.55, "unit": "cm" },
          "style": {
            "fill": { "type": "solid", "color": "#2B6CB0" },
            "stroke": { "type": "none" }
          },
          "content": null,
          "confidence": 98,
          "methods": ["structural", "visual"]
        }
      ],
      "notes": "Title slide uses corporate dark blue background with accent bar at bottom."
    }
  ],
  "repeatingPatterns": [
    {
      "patternId": "kpi-card",
      "description": "Standard KPI card used on 8 slides",
      "templateElement": { /* full element spec here or reference */ }
    }
  ],
  "audit": {
    "fidelityScore": 93,
    "discrepancies": [],
    "assumptions": [
      "Font 'Calibri Light' may appear slightly different on macOS; used system equivalent in HTML replica."
    ]
  }
}
```

## Key Fields Explained

**meta.slideOrPageDimensions**
- Always record the exact container size from the source.
- Common: 16:9 widescreen = 33.87cm × 19.05cm (or 13.333" × 7.5").

**globalStyles.themeColors**
- Extract from theme1.xml (a:clrScheme).
- Always resolve to concrete hex where possible.

**pages[].elements[]**
- **type**: text | shape | table | chart | picture | group | line | placeholder
- **shapeType** (for shapes): rectangle | roundRect | oval | triangle | arrow | star | etc. | custom
- **position**: x, y (top-left), width, height. Always include unit.
- **zIndex**: Critical for layering (higher = on top). Infer from XML order or visual stacking.
- **style**: Rich object. Examples:
  - fill: {type: "solid" | "gradient" | "pattern" | "image", color: "#...", gradientStops: [...] }
  - stroke / line: {type, color, widthPt, dashStyle}
  - shadow: {color, offsetX, offsetY, blur, spread}
  - font details as shown.
- **content**:
  - For text: plainText + optional rich `runs[]`
  - For table: `rows: number`, `cols: number`, `cells: [[{text, style}, ...]]`, `mergedRanges: [...]`
  - For chart: `chartType`, `series: [...]`, `data` (if extracted)
- **confidence**: 0-100 integer. Weighted average of methods.
- **methods**: Array of ["structural", "visual", "heuristic", "user-provided"]

**repeatingPatterns**
- Detect and extract templates for efficiency (e.g. 12 identical cards → one template + list of positions/instances).

## Schema Notes for Agents
- All dimensions in "cm" by default for office tools (easy to use in PowerPoint/Excel dialogs).
- Provide both "cm" and "px" (at 96dpi or user-specified) in HTML replicas.
- For Excel: Add per-sheet "columnWidthsCm": [3.2, 4.5, ...], "rowHeightsPt": [...]
- Include hyperlinks, alt text, and accessibility notes when present.
- Version the blueprint. Support "patch" operations for updates.

## Validation Rules
- Every element must have id, type, position, style, confidence.
- Positions must be within the page dimensions.
- Text content must match source exactly.
- Sum of zIndex layers should make visual sense.

Use this schema religiously. It is the contract that makes "photocopy" replication reliable and portable across tools.
