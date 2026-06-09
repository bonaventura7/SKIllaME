#!/usr/bin/env python3
"""
xlsx-reverse-engineering: Low-level OOXML Unpack & Inspection Helper
Extracts the .xlsx (ZIP) to a directory for raw XML analysis.
Provides quick inspection commands and structured listing of key RE-relevant parts.
Safe and read-only. Great for finding hidden sheets, protections, vbaProject, etc. that openpyxl may not surface.
"""

import json
import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

KEY_RE_PARTS = [
    "xl/workbook.xml",
    "xl/_rels/workbook.xml.rels",
    "[Content_Types].xml",
    "xl/sharedStrings.xml",
    "xl/styles.xml",
]

def main():
    if len(sys.argv) < 2:
        print("Usage: python unpack_xlsx.py <path-to-xlsx> [output_dir]")
        print("If output_dir not given, uses ./unpacked-<filename-stem>/")
        sys.exit(1)

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        print(json.dumps({"error": f"File not found: {input_path}"}))
        sys.exit(1)

    if len(sys.argv) > 2:
        out_dir = Path(sys.argv[2]).expanduser().resolve()
    else:
        out_dir = Path.cwd() / f"unpacked-{input_path.stem}"

    if out_dir.exists():
        # Clean previous for idempotency in RE sessions
        shutil.rmtree(out_dir, ignore_errors=True)

    out_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "file": str(input_path),
        "extracted_to": str(out_dir),
        "extracted_at": datetime.now().isoformat(),
        "members": [],
        "key_files_found": [],
        "vba_present": False,
        "quick_inspection": {},
        "notes": "Use this directory for grep, xmllint, or Python etree inspection of raw structure."
    }

    try:
        with zipfile.ZipFile(input_path, 'r') as zf:
            members = zf.namelist()
            results["members"] = members

            # Extract everything (for full inspection; can be large but necessary for RE)
            zf.extractall(out_dir)

            # Quick flags
            results["vba_present"] = any("vbaProject" in m for m in members)

            # Locate key files and do basic content preview
            for key in KEY_RE_PARTS:
                if key in members:
                    results["key_files_found"].append(key)
                    try:
                        content = zf.read(key).decode('utf-8', errors='replace')[:2000]
                        results["quick_inspection"][key] = content
                    except Exception as e:
                        results["quick_inspection"][key] = f"<read error: {e}>"

            # Special: look for sheet XMLs and workbook for state
            sheet_files = [m for m in members if m.startswith("xl/worksheets/sheet") and m.endswith(".xml")]
            results["sheet_xml_count"] = len(sheet_files)

            # Try to extract hidden state quickly from workbook.xml if present
            if "xl/workbook.xml" in members:
                wb_xml = zf.read("xl/workbook.xml").decode('utf-8', errors='replace')
                if 'state="veryHidden"' in wb_xml or "veryHidden" in wb_xml:
                    results["quick_inspection"]["very_hidden_sheets_detected"] = True
                if 'state="hidden"' in wb_xml:
                    results["quick_inspection"]["hidden_sheets_detected"] = True

    except zipfile.BadZipFile:
        results["error"] = "Not a valid ZIP / possibly encrypted or corrupted xlsx"
    except Exception as e:
        results["error"] = str(e)

    # Write structured output
    print(json.dumps(results, indent=2, ensure_ascii=False))

    # Also write a human-friendly summary file
    summary_path = out_dir / "UNPACK_SUMMARY.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"XLSX Unpacked: {input_path}\n")
        f.write(f"Extracted to: {out_dir}\n")
        f.write(f"Time: {results['extracted_at']}\n\n")
        f.write("=== Key RE Files Present ===\n")
        for kf in results.get("key_files_found", []):
            f.write(f"  - {kf}\n")
        f.write(f"\nVBA project present: {results.get('vba_present')}\n")
        f.write(f"Sheet XMLs: {results.get('sheet_xml_count', 'unknown')}\n\n")
        f.write("=== Quick Inspection Snippets (first 500 chars) ===\n")
        for k, v in results.get("quick_inspection", {}).items():
            f.write(f"\n--- {k} ---\n")
            f.write(str(v)[:500] + "\n")

    print(f"\n[INFO] Full extraction in {out_dir}", file=sys.stderr)
    print(f"[INFO] Human summary: {summary_path}", file=sys.stderr)
    print("[INFO] Now you can: grep -r 'state=\"veryHidden\"' " + str(out_dir) + "  or inspect specific XMLs", file=sys.stderr)

if __name__ == "__main__":
    main()
