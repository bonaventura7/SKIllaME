# Fidelity Checklist & Audit Protocol (design-photocopy-clone)

Use this exhaustive checklist for every replica before delivery. Score each page 0-100. Overall score = average. Target: ≥90 for "photocopy" claim. Document everything.

## Global / Setup (10 points)
- [ ] Container dimensions match original exactly (width × height in cm or inches).
- [ ] Page/slide/sheet count matches.
- [ ] Background(s) match (color, gradient, image, pattern, opacity).
- [ ] Theme colors resolved and applied consistently.
- [ ] Master layouts / default styles respected or explicitly overridden with justification.
- [ ] Overall aspect ratio and margins preserved.

## Layout & Positioning (25 points)
- [ ] Every element's top-left corner (x,y) within 0.15 cm / 4 px of original.
- [ ] Width and height of every element within 0.15 cm / 4 px.
- [ ] Rotation, flip, and shear (if any) match.
- [ ] Z-order / stacking exactly preserved (no element appears in front/behind incorrectly).
- [ ] Alignment: All left-aligned items share the same left edge (± tolerance); same for right, center, top, bottom baselines.
- [ ] Distribution: Even spacing between repeated elements (cards, columns, icons) — measure gaps.
- [ ] Margins from slide/page edges consistent.
- [ ] No elements clipped or overflowing unless original did.
- [ ] Groups maintain relative internal positioning.

## Colors & Fills (15 points)
- [ ] All solid fills: exact #HEX match (or documented closest).
- [ ] Gradients: stop colors, angles, and type (linear/radial) match.
- [ ] Patterns and textures approximated or noted.
- [ ] Transparency / alpha values preserved.
- [ ] Theme color references resolved correctly to final rendered color.
- [ ] No color shifts introduced (e.g. "accent1" correctly mapped).

## Typography & Text (20 points)
- [ ] All text content matches 100% (including spaces, line breaks, special characters).
- [ ] Font family: original or closest documented substitute.
- [ ] Font size (pt) within 0.5 pt.
- [ ] Font weight (bold, semibold, etc.), style (italic, underline), and effects (shadow on text) match.
- [ ] Color of every text run exact.
- [ ] Alignment (left/center/right/justify), vertical alignment, and text direction match.
- [ ] Line spacing, paragraph spacing, and indentation match.
- [ ] Bullet/numbering style and indentation preserved.
- [ ] Text boxes have correct word wrap and auto-size behavior (or fixed height as original).
- [ ] Mixed formatting within single text box (bold + regular runs) reproduced.

## Lines, Borders & Effects (10 points)
- [ ] Line weight (pt), color, style (solid/dashed/dotted), and cap/join types.
- [ ] Borders on shapes/tables: all four sides (or specified) match width + color.
- [ ] Shadows: color, offset (x/y), blur radius, spread, and opacity.
- [ ] Other effects (glow, reflection, soft edges, 3D bevel) either replicated in target format or explicitly noted as "approximated / native only".
- [ ] Transparency on lines/effects preserved.

## Tables & Structured Data (10 points)
- [ ] Exact number of rows and columns.
- [ ] Cell merge ranges identical.
- [ ] Cell content (text + formatting) per cell.
- [ ] Table-level styles (header row, alternating rows, total row) applied.
- [ ] Individual cell fills, borders, fonts, alignment, padding.
- [ ] Column widths and row heights (in cm or points) match.
- [ ] For Excel: formulas preserved or noted (with cell references).

## Charts, Images & Special Elements (10 points)
- [ ] Chart type, series count, data points, and visual styling (colors, markers, labels, legend position, gridlines, axes formatting).
- [ ] Image positions, sizes, crops, rotations, and effects.
- [ ] Alt text / descriptions preserved where present.
- [ ] SmartArt or complex groups decomposed into equivalent shapes + text (or noted).
- [ ] Hyperlinks, actions, and interactive elements documented (even if not fully replicable in all formats).

## Multi-Page / Consistency (5 points)
- [ ] Repeating elements (headers, footers, logos, card templates) are identical across instances.
- [ ] Slide transitions / animations described in metadata (HTML replica may simulate key ones with CSS).
- [ ] Headers, footers, page numbers, and section properties consistent.

## Functional Equivalence (5 points)
- [ ] In Excel replicas: formulas calculate correctly when data is entered.
- [ ] In PPT: placeholders and masters applied logically.
- [ ] No data loss (all original text/numbers present).
- [ ] Accessibility notes carried forward (contrast, alt text, reading order where detectable).

## Scoring & Reporting
- Assign 0-100 per category above.
- **Overall Fidelity Score** = weighted average (use the point weights above).
- **Per-Page Score** (repeat checklist per slide/sheet).
- **Discrepancies Log**: For every item that scores < full points, record:
  - Element ID + description
  - Expected vs Actual
  - Method that caused issue
  - Proposed fix or accepted trade-off
- **Final Verdict**:
  - ≥95: "Photocopy Grade — Ready for production use"
  - 90-94: "Excellent Clone — Minor documented differences"
  - 80-89: "High Fidelity — Good for most uses; review specific areas"
  - <80: "Partial Clone — Significant workarounds applied; recommend native editing or human review"

## HA Protocol
1. Run checklist internally after generating each major output.
2. If overall <90, automatically trigger another extraction pass (e.g. request better screenshots or re-parse specific XML).
3. Include the full scored checklist + discrepancies in the final response to the user.
4. Always offer: "Would you like me to iterate on any page/element with lower confidence?"

## Quick Sanity Filters (Run First)
- Text count per page matches (±1 for minor formatting artifacts).
- No negative positions or dimensions > container.
- At least one background element covering most of the page.
- Color contrast sufficient for text (WCAG note if relevant).

Print or copy this checklist into your thinking for every task. It is the quality gate that makes this skill trustworthy for enterprise HA document workflows.
