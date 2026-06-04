#!/usr/bin/env python3
"""retouch.py — Multi-comando photo-perfect SLIM.

Subcommand pattern (git-style):
  retouch.py photo  IN [--preset N] [--out P]              ← ritocco singolo
  retouch.py vinted DIR --item-type T --out DIR            ← set Vinted da cartella
  retouch.py batch  DIR --preset N --out DIR [--jobs N]    ← batch parallelo
  retouch.py bg     IN [--replace COLOR|transparent] [--shadow] [--out P]
  retouch.py enhance IN [--auto] [--wb auto] [--denoise L] [--sharpen]

Default (senza subcomando) → 'photo'.
"""
from __future__ import annotations
import json, time, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# import dal core (stessa directory)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import (make_parser, check_input, process, load_recipe,
                  remove_bg, grey_world_wb, auto_exposure, clahe,
                  denoise as nr, unsharp, strip_exif,
                  out, err, VALID_EXTS)
from PIL import Image

# ════════════════════════════════════════════════════════════════
# COMANDO: photo (ritocco singolo)
# ════════════════════════════════════════════════════════════════
def cmd_photo(a):
    check_input(a.input)
    dst = a.out or a.input.with_name(f"{a.input.stem}_retouched.jpg")
    try: out(process(a.input, a.preset, dst))
    except Exception as e: err(str(e))

# ════════════════════════════════════════════════════════════════
# COMANDO: vinted (set completo da cartella)
# ════════════════════════════════════════════════════════════════
ITEM2PRESET = {
    "sweater":"vinted-clothing","tshirt":"vinted-clothing","jeans":"vinted-clothing",
    "dress":"vinted-clothing","jacket":"vinted-clothing","shoes":"vinted-shoes",
    "bag":"vinted-accessory","generic":"vinted-clothing",
}
def cmd_vinted(a):
    if not a.input_dir.is_dir(): err("non è una cartella")
    roles = load_recipe(a.item_type); preset = ITEM2PRESET[a.item_type]
    imgs = sorted([f for f in a.input_dir.iterdir() if f.suffix.lower() in VALID_EXTS])
    if not imgs: err("nessuna immagine")
    a.out.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); manifest = {"item_type":a.item_type,"preset":preset,"photos":[]}
    for i, src in enumerate(imgs):
        role = roles[i] if i < len(roles) else f"extra_{i+1}"
        name = f"{i+1:02d}_{role}.jpg" if a.rename == "auto" else src.name
        dst = a.out / name
        try:
            r = process(src, preset, dst)
            manifest["photos"].append({"seq":i+1,"role":role,"source":src.name,
                "output":dst.name,"status":r["status"],"size_mb":r["metrics"]["output_size_mb"]})
        except Exception as e:
            manifest["photos"].append({"seq":i+1,"role":role,"source":src.name,
                "status":"error","error":str(e)})
    (a.out/"_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    ok_all = all(p.get("status") in ("ok","degraded") for p in manifest["photos"])
    out({"status":"ok" if ok_all else "partial","item_type":a.item_type,"preset":preset,
         "processed":len(imgs),"output_dir":str(a.out),
         "manifest":str(a.out/"_manifest.json"),"roles_used":roles[:len(imgs)],
         "duration_s":round(time.time()-t0,2),"photos":manifest["photos"]})

# ════════════════════════════════════════════════════════════════
# COMANDO: batch (parallelo)
# ════════════════════════════════════════════════════════════════
def cmd_batch(a):
    if not a.input_dir.is_dir(): err("non è una cartella")
    pat = "**/*" if a.recursive else "*"
    files = [f for f in a.input_dir.glob(pat) if f.is_file() and f.suffix.lower() in VALID_EXTS]
    if not files: err("nessuna immagine")
    a.out.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); results, errors = [], []
    work = lambda f: process(f, a.preset, a.out / f.relative_to(a.input_dir).with_suffix(".jpg"))
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(work, f): f for f in files}
        for fu in as_completed(futs):
            try: results.append(fu.result())
            except Exception as e: errors.append({"file":str(futs[fu]),"error":str(e)})
    out({"status":"ok" if not errors else "partial","preset":a.preset,
         "processed":len(results),"errors":errors,
         "total_in_mb":round(sum(r["metrics"]["input_size_mb"] for r in results),2),
         "total_out_mb":round(sum(r["metrics"]["output_size_mb"] for r in results),2),
         "duration_s":round(time.time()-t0,2),"output_dir":str(a.out)})

# ════════════════════════════════════════════════════════════════
# COMANDO: bg (rimozione/sostituzione sfondo)
# ════════════════════════════════════════════════════════════════
COLORS = {"white":"#FFFFFF","black":"#000000","gray":"#F7F7F5","lightgray":"#EFEFEC"}
def cmd_bg(a):
    check_input(a.input)
    t0 = time.time(); img = Image.open(a.input).convert("RGB")
    transp = a.replace.lower() == "transparent"
    color = None if transp else COLORS.get(a.replace.lower(), a.replace)
    sh = {"enabled":True,"opacity":0.18,"blur":25,"offset_y":8} if a.shadow else None
    res = remove_bg(img, replace=color, shadow=sh)
    ext = "png" if transp else "jpg"
    dst = a.out or a.input.with_name(f"{a.input.stem}_nobg.{ext}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if transp: res.save(dst, "PNG", optimize=True)
    else: res.convert("RGB").save(dst, "JPEG", quality=94, optimize=True, progressive=True)
    out({"status":"ok","input":str(a.input),"output":[str(dst)],
         "operations":["bg-remove"]+(["bg-replace","shadow"] if not transp else []),
         "metrics":{"duration_s":round(time.time()-t0,2)}})

# ════════════════════════════════════════════════════════════════
# COMANDO: enhance (puntuale)
# ════════════════════════════════════════════════════════════════
def cmd_enhance(a):
    check_input(a.input)
    if a.auto:
        a.wb = a.wb or "auto"; a.exposure = a.exposure or "auto"
        a.denoise = a.denoise or "light"; a.sharpen = True
    t0 = time.time(); img = Image.open(a.input).convert("RGB"); ops = []
    if a.wb == "auto":       img = grey_world_wb(img); ops.append("wb")
    if a.exposure == "auto": img = auto_exposure(img);  ops.append("exposure")
    img = clahe(img); ops.append("clahe")
    if a.denoise and a.denoise != "none": img = nr(img, a.denoise); ops.append(f"denoise-{a.denoise}")
    if a.sharpen: img = unsharp(img, 0.6, 1.1, 3); ops.append("sharpen")
    img = strip_exif(img)
    dst = a.out or a.input.with_name(f"{a.input.stem}_enhanced.jpg")
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "JPEG", quality=92, optimize=True, progressive=True)
    out({"status":"ok","input":str(a.input),"output":[str(dst)],"operations":ops,
         "metrics":{"duration_s":round(time.time()-t0,2)}})

# ════════════════════════════════════════════════════════════════
# DISPATCHER
# ════════════════════════════════════════════════════════════════
def main():
    from pathlib import Path
    p = make_parser("photo-perfect — multi-comando (photo|vinted|batch|bg|enhance)")
    sub = p.add_subparsers(dest="cmd")

    # photo (default se nessun subcomando)
    sp = sub.add_parser("photo", help="ritocco singolo")
    sp.add_argument("input", type=Path)
    sp.add_argument("--preset", default="general-enhance")
    sp.add_argument("--out", type=Path)

    sv = sub.add_parser("vinted", help="set Vinted da cartella")
    sv.add_argument("input_dir", type=Path)
    sv.add_argument("--item-type", default="generic", choices=list(ITEM2PRESET))
    sv.add_argument("--out", type=Path, required=True)
    sv.add_argument("--rename", choices=["auto","off"], default="auto")

    sb = sub.add_parser("batch", help="batch parallelo")
    sb.add_argument("input_dir", type=Path)
    sb.add_argument("--preset", default="general-enhance")
    sb.add_argument("--out", type=Path, required=True)
    sb.add_argument("--recursive", action="store_true")
    sb.add_argument("--jobs", type=int, default=2)

    sg = sub.add_parser("bg", help="rimozione sfondo")
    sg.add_argument("input", type=Path)
    sg.add_argument("--replace", default="transparent")
    sg.add_argument("--shadow", action="store_true")
    sg.add_argument("--out", type=Path)

    se = sub.add_parser("enhance", help="enhance puntuale")
    se.add_argument("input", type=Path)
    se.add_argument("--auto", action="store_true")
    se.add_argument("--wb", choices=["auto","off"])
    se.add_argument("--exposure", choices=["auto","off"])
    se.add_argument("--denoise", choices=["none","light","medium","strong"])
    se.add_argument("--sharpen", action="store_true")
    se.add_argument("--out", type=Path)

    a = p.parse_args()
    if a.cmd is None: p.print_help(); sys.exit(0)

    {"photo":cmd_photo,"vinted":cmd_vinted,"batch":cmd_batch,
     "bg":cmd_bg,"enhance":cmd_enhance}[a.cmd](a)

if __name__ == "__main__": main()
