#!/usr/bin/env python3
"""
extract_office_structure.py
Part of design-photocopy-clone skill for skills.sh

Purpose: Structural extraction helper for .pptx, .xlsx, .docx files.
Unzips the Office Open XML file and extracts key design-relevant information:
- Basic metadata
- Slide/sheet/page dimensions
- Theme colors (resolved hex where possible)
- List of top-level elements with approximate positions, types, and text content
- Table structures (basic)
- Color and font samples

Pure Python stdlib only (zipfile + xml.etree.ElementTree). No external dependencies.

Usage:
    python3 extract_office_structure.py /path/to/presentation.pptx
    python3 extract_office_structure.py /path/to/workbook.xlsx --max-pages 5

Output: Structured text/JSON-like report to stdout. Can be parsed by agent or human.

Limitations:
- Positions are in EMUs (convert: cm = EMU / 360000)
- Does not resolve every complex effect or animation (focus on core design)
- For full visual fidelity, combine with screenshots + vision analysis
- Large files or many embedded objects: may be slow or truncated

This is a starting point for the structural path in the HA workflow.
"""

import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import json
from collections import defaultdict
from typing import Any, Dict, List, Optional

# Common OOXML namespaces (simplified)
NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}

def register_namespaces():
    for prefix, uri in NS.items():
        ET.register_namespace(prefix, uri)

register_namespaces()

def emu_to_cm(emu: int) -> float:
    """Convert EMUs to centimeters. 914400 EMU = 1 inch, 2.54 cm/inch."""
    if not emu:
        return 0.0
    return round(emu / 360000, 2)

def get_text_from_element(elem: ET.Element) -> str:
    """Extract all text from <a:t> or <w:t> tags recursively."""
    texts = []
    for t in elem.iter():
        if t.tag.endswith('}t') or t.tag == '{http://schemas.openxmlformats.org/drawingml/2006/main}t':
            if t.text:
                texts.append(t.text)
    return ''.join(texts).strip()

def resolve_color(elem: ET.Element) -> Optional[str]:
    """Try to extract a hex color from srgbClr or sysClr."""
    for child in elem.iter():
        if child.tag.endswith('srgbClr'):
            val = child.get('val')
            if val:
                return f"#{val.upper()}"
        if child.tag.endswith('sysClr'):
            val = child.get('lastClr') or child.get('val')
            if val:
                return f"#{val.upper()}"
    return None

def extract_theme_colors(zf: zipfile.ZipFile) -> Dict[str, str]:
    """Extract theme color scheme (best effort)."""
    colors = {}
    theme_paths = [
        'ppt/theme/theme1.xml',
        'xl/theme/theme1.xml',
        'word/theme/theme1.xml'
    ]
    for path in theme_paths:
        try:
            with zf.open(path) as f:
                tree = ET.parse(f)
                root = tree.getroot()
                scheme = root.find('.//a:clrScheme', NS)
                if scheme is not None:
                    for clr in scheme:
                        name = clr.tag.split('}')[-1] if '}' in clr.tag else clr.tag
                        hex_color = resolve_color(clr)
                        if hex_color:
                            colors[name] = hex_color
                    break
        except Exception:
            continue
    return colors

def parse_slide_or_sheet_elements(zf: zipfile.ZipFile, content_path: str, file_type: str) -> List[Dict[str, Any]]:
    """Parse main content for elements (positions, text, basic styles)."""
    elements = []
    try:
        with zf.open(content_path) as f:
            tree = ET.parse(f)
            root = tree.getroot()
    except Exception as e:
        return [{"error": f"Failed to parse {content_path}: {str(e)}"}]

    # PowerPoint slides
    if file_type == 'pptx':
        for sp in root.iter():
            tag = sp.tag.split('}')[-1] if '}' in sp.tag else sp.tag
            if tag in ('sp', 'pic', 'grpSp'):
                elem = {"type": tag, "id": sp.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', 'unknown')}
                # Position
                off = sp.find('.//a:off', NS)
                ext = sp.find('.//a:ext', NS)
                if off is not None:
                    x = int(off.get('x', 0))
                    y = int(off.get('y', 0))
                    elem["position_emu"] = {"x": x, "y": y}
                    elem["position_cm"] = {"x": emu_to_cm(x), "y": emu_to_cm(y)}
                if ext is not None:
                    cx = int(ext.get('cx', 0))
                    cy = int(ext.get('cy', 0))
                    elem["size_emu"] = {"cx": cx, "cy": cy}
                    elem["size_cm"] = {"width": emu_to_cm(cx), "height": emu_to_cm(cy)}

                # Text
                text = get_text_from_element(sp)
                if text:
                    elem["text"] = text[:200] + ("..." if len(text) > 200 else "")

                # Simple color sample
                fill = sp.find('.//a:solidFill', NS)
                if fill is not None:
                    color = resolve_color(fill)
                    if color:
                        elem["fill_color"] = color

                elements.append(elem)

    # Excel worksheets (simplified)
    elif file_type == 'xlsx':
        # Look for sheetData
        sheet_data = root.find('.//x:sheetData', NS)
        if sheet_data is not None:
            for row in sheet_data.findall('.//x:row', NS):
                row_num = row.get('r')
                for cell in row.findall('.//x:c', NS):
                    cell_ref = cell.get('r')
                    val = cell.find('.//x:v', NS)
                    if val is not None and val.text:
                        elements.append({
                            "type": "cell",
                            "ref": cell_ref,
                            "row": row_num,
                            "value": val.text[:100]
                        })

    # Word (basic paragraphs and tables)
    elif file_type == 'docx':
        for p in root.findall('.//w:p', NS):
            text = get_text_from_element(p)
            if text:
                elements.append({"type": "paragraph", "text": text[:150]})
        for tbl in root.findall('.//w:tbl', NS):
            elements.append({"type": "table", "rows": len(tbl.findall('.//w:tr', NS))})

    return elements[:50]  # Limit for readability

def analyze_file(file_path: str, max_pages: int = 10) -> Dict[str, Any]:
    """Main analysis function."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    result: Dict[str, Any] = {
        "file": os.path.basename(file_path),
        "file_type": None,
        "dimensions_cm": None,
        "theme_colors": {},
        "pages": [],
        "total_elements_found": 0,
        "notes": "Structural extraction only. Combine with visual analysis for full photocopy fidelity."
    }

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Detect type
            namelist = zf.namelist()
            if 'ppt/presentation.xml' in namelist:
                result["file_type"] = "pptx"
                content_base = 'ppt/slides/slide'
                ext = '.xml'
                # Get slide size
                try:
                    with zf.open('ppt/presentation.xml') as f:
                        tree = ET.parse(f)
                        sld_sz = tree.find('.//p:sldSz', NS)
                        if sld_sz is not None:
                            cx = int(sld_sz.get('cx', 0))
                            cy = int(sld_sz.get('cy', 0))
                            result["dimensions_cm"] = {
                                "width": emu_to_cm(cx),
                                "height": emu_to_cm(cy)
                            }
                except Exception:
                    pass
            elif 'xl/workbook.xml' in namelist:
                result["file_type"] = "xlsx"
                content_base = 'xl/worksheets/sheet'
                ext = '.xml'
                result["dimensions_cm"] = {"width": "N/A (grid)", "height": "N/A (grid)"}
            elif 'word/document.xml' in namelist:
                result["file_type"] = "docx"
                content_base = 'word/document'
                ext = '.xml'
                result["dimensions_cm"] = {"width": "varies by section", "height": "varies"}
            else:
                result["file_type"] = "unknown"
                return result

            result["theme_colors"] = extract_theme_colors(zf)

            # Extract per-page/sheet content
            page_count = 0
            for name in sorted(namelist):
                if name.startswith(content_base) and name.endswith(ext):
                    page_count += 1
                    if page_count > max_pages:
                        break
                    elements = parse_slide_or_sheet_elements(zf, name, result["file_type"])
                    result["pages"].append({
                        "page_id": name,
                        "elements": elements,
                        "element_count": len(elements)
                    })
                    result["total_elements_found"] += len(elements)

            result["total_pages_extracted"] = len(result["pages"])
            result["total_pages_in_file"] = page_count  # approximate

    except zipfile.BadZipFile:
        result["error"] = "Not a valid ZIP/Office file"
    except Exception as e:
        result["error"] = str(e)

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_office_structure.py <file.pptx|xlsx|docx> [--max-pages N]")
        print("Example: python3 extract_office_structure.py presentation.pptx --max-pages 3")
        sys.exit(1)

    file_path = sys.argv[1]
    max_pages = 10
    if '--max-pages' in sys.argv:
        try:
            idx = sys.argv.index('--max-pages')
            max_pages = int(sys.argv[idx + 1])
        except (ValueError, IndexError):
            pass

    report = analyze_file(file_path, max_pages)

    # Pretty print
    print("=" * 70)
    print(f"STRUCTURAL DESIGN EXTRACTION REPORT")
    print(f"File: {report.get('file')}")
    print(f"Type: {report.get('file_type')}")
    print(f"Dimensions (cm): {report.get('dimensions_cm')}")
    print(f"Theme Colors Sample: {list(report.get('theme_colors', {}).items())[:6]}")
    print(f"Pages Extracted: {report.get('total_pages_extracted', 0)} / ~{report.get('total_pages_in_file', '?')}")
    print(f"Total Elements Found (limited): {report.get('total_elements_found', 0)}")
    print("=" * 70)

    if 'error' in report:
        print(f"ERROR: {report['error']}")
        return

    for i, page in enumerate(report.get('pages', []), 1):
        print(f"\n--- Page/Slide/Sheet {i}: {page['page_id']} ---")
        print(f"Elements: {page['element_count']}")
        for elem in page['elements'][:8]:  # Show first 8 per page for brevity
            print(f"  • {elem.get('type', 'unknown')}: ", end="")
            if 'text' in elem:
                print(f"\"{elem['text']}\"", end="")
            if 'position_cm' in elem:
                pos = elem['position_cm']
                print(f" @ ({pos.get('x')}, {pos.get('y')}) cm", end="")
            if 'fill_color' in elem:
                print(f" fill={elem['fill_color']}", end="")
            if 'ref' in elem:
                print(f" cell {elem.get('ref')}", end="")
            print()
        if len(page['elements']) > 8:
            print(f"  ... and {len(page['elements']) - 8} more elements (truncated)")

    print("\n" + "=" * 70)
    print("NEXT STEPS FOR FULL PHOTOCOPY CLONE (per skill instructions):")
    print("1. Provide high-resolution screenshots of the slides/sheets for visual path.")
    print("2. Feed this report + images into the agent running the design-photocopy-clone skill.")
    print("3. Request HTML replica, native instructions, or Python generator from the blueprint.")
    print("=" * 70)

if __name__ == "__main__":
    main()
