# PowerPoint Recreation Instructions Template

**Source**: [Insert blueprint meta.sourceFiles]
**Target**: New blank PowerPoint presentation (16:9 widescreen recommended unless original differs)

## Global Setup
1. Open Microsoft PowerPoint (or compatible).
2. File > New > Blank Presentation.
3. Design > Slide Size > Widescreen (16:9) or Custom: Width 13.333 inches (33.87 cm), Height 7.5 inches (19.05 cm).
4. (Optional but recommended) Apply the original theme if .thmx file extracted, or manually set theme colors from blueprint.globalStyles.themeColors.
5. View > Ruler and View > Gridlines for precise positioning.

## Per-Slide Instructions

### Slide 1: [Page Title or "Title Slide"]
**Background**:
- Insert > Shapes > Rectangle.
- Position: Left 0 cm, Top 0 cm, Width 33.87 cm, Height 19.05 cm.
- Fill: Solid [exact color from blueprint].
- Line: No Line.
- Send to Back (right-click > Send to Back).

**Element 1: [Description, e.g. Main Title Text Box]**
- Insert > Text Box.
- Position & Size: Left X.XX cm, Top Y.YY cm, Width W.WW cm, Height H.HH cm.
- Text: "Exact text here" (copy-paste from blueprint).
- Font: [family], [size] pt, [Bold/Regular/Italic], Color #[HEX].
- Paragraph: Alignment [Left/Center/Right], Line spacing [value].
- (If multiple runs) Format each run individually.

**Element 2: [Shape, e.g. Accent Rectangle]**
- Insert > Shapes > [Rectangle / Rounded Rectangle / etc.].
- Position & Size: ...
- Fill: Solid or Gradient (stops: color1 at 0%, color2 at 100%, direction).
- Line: [width] pt, color #[HEX], or No Line.
- Effects: Format Shape > Shadow > [settings] (or note "add shadow manually: color #000000, blur 8pt, offset 3pt down").

**Element 3: [Table example]**
- Insert > Table > [rows] rows × [cols] columns.
- Position & Size.
- Select table > Table Design tab:
  - Apply style or manual: Header row fill #[HEX], etc.
  - Merge cells as specified in blueprint.
  - Populate cells with exact text + individual cell formatting.

**Repeat for all elements in z-order (bottom to top).**

**Final Polish for this slide**:
- Select all elements that should align → Align > [options].
- Group related elements if they move together.
- Add any animations (Animations tab) as noted in blueprint metadata: e.g. "Fade entrance, 0.5s, on click" for element ID "title-text-01".

## Additional Slides
Copy the pattern above for every page. 
For repeating patterns (e.g. KPI cards):
- Create the first instance fully.
- Then duplicate the group and adjust only the position + data content.

## Master / Layout Tips
- If the original used a specific slide master or layout:
  - View > Slide Master.
  - Duplicate the closest layout.
  - Apply the background and common elements (logo, footer) to the master.
  - Then use that layout for content slides.

## Export & Verification
- Save as .pptx.
- Run the fidelity checklist against original (side-by-side view at 100% zoom).
- File > Export > Create PDF/XPS or PNG screenshots for final comparison.

**Notes from Blueprint**:
- [Insert any specific assumptions or workarounds here]
- Fonts: If "Calibri Light" not available, substitute "Calibri" or "Arial" and note it.

This template produces a fully editable native file that matches the photocopy standard.
