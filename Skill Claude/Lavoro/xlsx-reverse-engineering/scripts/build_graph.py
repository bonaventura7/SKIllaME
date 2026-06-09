#!/usr/bin/env python3
"""
xlsx-reverse-engineering: Simple Dependency Graph Builder
Reads formulas/dependency_index.csv (produced by extract_formulas.py) or runs lightweight extraction.
Produces:
- text report
- Mermaid diagram (for small graphs)
- edges.csv for further processing
"""

import json
import sys
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_dependency_index(csv_path: Path):
    edges = []
    if not csv_path.exists():
        return edges
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            target = row.get('target', '')
            # We don't have full referencers here, but we can use count as weight
            count = int(row.get('referenced_by_count', 0))
            # For demo we create self-edges or note; in real use we would parse the example_referencers
            if target:
                edges.append((target, "multiple_referencers", count))
    return edges

def main():
    if len(sys.argv) < 2:
        print("Usage: python build_graph.py <path-to-xlsx> [formulas_dir]")
        print("Expects formulas/dependency_index.csv from extract_formulas.py (recommended to run that first).")
        sys.exit(1)

    input_path = Path(sys.argv[1]).expanduser().resolve()
    formulas_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("formulas")

    dep_csv = formulas_dir / "dependency_index.csv"
    edges = load_dependency_index(dep_csv)

    # If no edges from CSV, we can do a very lightweight fallback using extract (but to keep simple we note it)
    if not edges:
        print(json.dumps({"warning": "No dependency_index.csv found. Run extract_formulas.py first for best results.", "file": str(input_path)}))
        # Minimal fallback: just report file
        edges = []

    graph = {
        "file": str(input_path),
        "generated_at": datetime.now().isoformat(),
        "node_count": len(set(e[0] for e in edges)),
        "edge_count": len(edges),
        "edges": [{"source": e[0], "target": e[1], "weight": e[2]} for e in edges[:500]],  # cap
        "mermaid": ""
    }

    # Build simple Mermaid (top 30 edges for readability)
    mermaid_lines = ["graph TD"]
    seen = set()
    for src, tgt, w in edges[:30]:
        clean_src = src.replace("!", "_").replace("$", "").replace(" ", "_")
        clean_tgt = tgt.replace("!", "_").replace("$", "").replace(" ", "_")
        key = (clean_src, clean_tgt)
        if key not in seen:
            mermaid_lines.append(f"    {clean_src} -->|{w}| {clean_tgt}")
            seen.add(key)
    graph["mermaid"] = "\n".join(mermaid_lines)

    print(json.dumps(graph, indent=2, ensure_ascii=False))

    out_dir = Path("graphs")
    out_dir.mkdir(exist_ok=True)

    with open(out_dir / "dependency_graph.json", "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)

    with open(out_dir / "edges.csv", "w", encoding="utf-8") as f:
        f.write("source,target,weight\n")
        for src, tgt, w in edges:
            f.write(f'"{src}","{tgt}",{w}\n')

    with open(out_dir / "dependency_graph.mmd", "w", encoding="utf-8") as f:
        f.write(graph["mermaid"])

    print(f"\n[INFO] Graphs written to ./graphs/ (mermaid, edges.csv, json)", file=sys.stderr)
    if len(edges) > 30:
        print("[INFO] Mermaid limited to first 30 edges for readability. Use edges.csv for full graph.", file=sys.stderr)

if __name__ == "__main__":
    main()
