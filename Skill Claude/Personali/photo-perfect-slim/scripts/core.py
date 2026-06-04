#!/usr/bin/env python3
"""core.py — Utility condivise photo-perfect SLIM.
Legge preset e prompt da ../skill.json (assets.presets / assets.prompts).
"""
from __future__ import annotations
import argparse, json, sys, time, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKILL_JSON = ROOT / "skill.json"
VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}

# ───────── Lazy import HA ─────────
def _try(m):
    try: return __import__(m)
    except ImportError: return None

PIL  = _try("PIL")
np   = _try("numpy")
cv2  = _try("cv2")
rembg = _try("rembg")

if PIL is None or np is None:
    print(json.dumps({"status":"error","error":"pip install Pillow numpy"})); sys.exit(2)

from PIL import Image, ImageEnhance, ImageFilter, ImageOps  # noqa
import numpy as np  # noqa

# ───────── JSON I/O ─────────
def out(payload: dict, code: int = 0) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False)); sys.exit(code)

def err(msg: str, **x) -> None:
    out({"status":"error","error":msg, **x}, 1)

# ───────── Loader unificato (cache in-memory) ─────────
_SKILL_CACHE = None
def _skill() -> dict:
    global _SKILL_CACHE
    if _SKILL_CACHE is None:
        _SKILL_CACHE = json.loads(SKILL_JSON.read_text())
    return _SKILL_CACHE

def load_preset(name: str) -> dict:
    presets = _skill()["assets"]["presets"]["presets"]
    if name not in presets:
        err(f"preset sconosciuto: {name}", available=list(presets))
    return presets[name]

def load_recipe(item_type: str) -> list[str]:
    rec = _skill()["assets"]["presets"]["vinted_pack_recipes"]
    return rec.get(item_type, rec["generic"])

def load_prompt(name: str | None, text: str | None) -> tuple[str, str]:
    bank = _skill()["assets"]["prompts"]
    neg = bank["negative_prompts"]["common"]
    if text: return text, neg
    if name and name in bank["prompts"]:
        return bank["prompts"][name], neg
    err(f"prompt sconosciuto: {name}", available=list(bank["prompts"]))

# ───────── Operazioni colore ─────────
def grey_world_wb(img):
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    m = [a[...,i].mean() for i in range(3)]
    if min(m) < 1: return img
    g = sum(m)/3
    for i in range(3): a[...,i] *= g/m[i]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))

def auto_exposure(img, target=128.0):
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    luma = 0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
    cur = luma.mean()
    if cur < 1: return img
    f = max(0.65, min(1.35, target/cur))
    return Image.fromarray(np.clip(a*f,0,255).astype(np.uint8))

def clahe(img):
    if cv2 is None: return img
    a = cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2LAB)
    l,A,b = cv2.split(a)
    l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(l)
    return Image.fromarray(cv2.cvtColor(cv2.merge((l,A,b)), cv2.COLOR_LAB2RGB))

def sat_vib(img, sat=1.0, vib=1.0):
    if abs(sat-1)>1e-3: img = ImageEnhance.Color(img).enhance(sat)
    if abs(vib-1)>1e-3:
        a = np.asarray(img.convert("HSV"), dtype=np.float32)
        boost = 1 + (vib-1) * (1 - a[...,1]/255.0)
        a[...,1] = np.clip(a[...,1]*boost, 0, 255)
        img = Image.fromarray(a.astype(np.uint8), "HSV").convert("RGB")
    return img

def contrast(img, c=1.0):
    return ImageEnhance.Contrast(img).enhance(c) if abs(c-1)>1e-3 else img

def denoise(img, level="light"):
    if not level or level=="none": return img
    if cv2 is not None:
        h = {"light":3,"medium":7,"strong":12}.get(level,5)
        return Image.fromarray(cv2.fastNlMeansDenoisingColored(np.asarray(img.convert("RGB")), None, h, h, 7, 21))
    r = {"light":0.6,"medium":1.0,"strong":1.6}.get(level,0.8)
    return img.filter(ImageFilter.GaussianBlur(radius=r))

def unsharp(img, amount=0.5, radius=1.0, threshold=3):
    return img.filter(ImageFilter.UnsharpMask(radius=radius, percent=int(amount*150), threshold=threshold))

# ───────── Sfondo ─────────
def remove_bg(img, replace=None, shadow=None):
    if rembg is not None: rgba = rembg.remove(img)
    elif cv2 is not None: rgba = _grabcut(img)
    else: return img
    if not replace: return rgba
    bg = Image.new("RGBA", rgba.size, replace)
    if shadow and shadow.get("enabled"):
        bg = _contact_shadow(bg, rgba, shadow)
    return Image.alpha_composite(bg, rgba.convert("RGBA")).convert("RGB")

def _grabcut(img):
    a = np.asarray(img.convert("RGB")); h,w = a.shape[:2]
    mask = np.zeros((h,w), np.uint8)
    rect = (int(w*.05), int(h*.05), int(w*.9), int(h*.9))
    cv2.grabCut(a, mask, rect, np.zeros((1,65)), np.zeros((1,65)), 5, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask==2)|(mask==0), 0, 255).astype("uint8")
    return Image.fromarray(np.dstack([a,m]), "RGBA")

def _contact_shadow(bg, subj_rgba, cfg):
    alpha = subj_rgba.convert("RGBA").split()[-1]
    sh = Image.new("L", bg.size, 0)
    sh.paste(alpha, (0, cfg.get("offset_y",8)))
    sh = sh.filter(ImageFilter.GaussianBlur(radius=cfg.get("blur",25)))
    sh_arr = (np.array(sh, dtype=np.float32) * cfg.get("opacity",0.18)).clip(0,255).astype(np.uint8)
    overlay = Image.new("RGBA", bg.size, (0,0,0,0))
    overlay.putalpha(Image.fromarray(sh_arr))
    return Image.alpha_composite(bg, overlay)

# ───────── Crop / Save / Compliance ─────────
def square_crop(img, pad_pct=6):
    w,h = img.size; side = min(w,h); pad = int(side*pad_pct/100)
    canvas = Image.new("RGB", (side,side), (247,247,245))
    inner = ImageOps.contain(img, (side-2*pad, side-2*pad))
    iw,ih = inner.size
    canvas.paste(inner, ((side-iw)//2, (side-ih)//2))
    return canvas

def resize_to(img, w, h):
    return img.resize((w,h), Image.LANCZOS)

def strip_exif(img):
    c = Image.new(img.mode, img.size); c.putdata(list(img.getdata())); return c

def save_with_cap(img, path: Path, fmt="JPEG", quality=92, max_mb=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, fmt, quality=quality, optimize=True, progressive=True)
    if max_mb:
        for q in (88,85,82,78):
            if path.stat().st_size/1024/1024 <= max_mb: break
            img.save(path, fmt, quality=q, optimize=True, progressive=True)
    return path.stat().st_size/1024/1024

# ───────── Pipeline orchestrator ─────────
def process(input_path: Path, preset_name: str, out_path: Path) -> dict:
    t0 = time.time()
    preset = load_preset(preset_name)
    ops, warn, fb = [], [], 1
    img = Image.open(input_path).convert("RGB")
    in_mb = input_path.stat().st_size/1024/1024

    c = preset.get("color", {})
    if c.get("white_balance","").startswith("auto"): img = grey_world_wb(img); ops.append("wb")
    if c.get("exposure_ev") == "auto":               img = auto_exposure(img); ops.append("exposure")
    if cv2 is not None: img = clahe(img); ops.append("clahe"); fb = 2
    else:               warn.append("cv2 missing: skipped CLAHE")
    img = sat_vib(img, c.get("saturation",1.0), c.get("vibrance",1.0)); ops.append("sat-vib")
    img = contrast(img, c.get("contrast",1.0));                          ops.append("contrast")

    d = preset.get("detail", {})
    if d.get("denoise"): img = denoise(img, d["denoise"]); ops.append(f"denoise-{d['denoise']}")
    if d.get("sharpen"):
        s = d["sharpen"]
        img = unsharp(img, s.get("amount",.5), s.get("radius",1.0), s.get("threshold",3))
        ops.append("unsharp")

    bg = preset.get("background", {})
    if bg.get("action") == "replace":
        if rembg is None and cv2 is None:
            warn.append("no bg engine: install rembg+onnxruntime or opencv-python")
        else:
            img = remove_bg(img, bg.get("color"), bg.get("shadow"))
            ops.append("bg"); fb = 2

    o = preset.get("output", {})
    if preset.get("crop",{}).get("mode") == "square":
        img = square_crop(img, preset["crop"].get("padding_pct",6)); ops.append("crop")
    if "width" in o and "height" in o:
        img = resize_to(img, o["width"], o["height"]); ops.append("resize")

    if preset.get("compliance",{}).get("strip_exif"):
        img = strip_exif(img); ops.append("exif")

    fmt = o.get("format","jpg").upper().replace("JPG","JPEG")
    out_mb = save_with_cap(img, out_path, fmt, o.get("quality",92),
                           preset.get("compliance",{}).get("max_size_mb"))

    return {
        "status": "degraded" if warn else "ok",
        "input": str(input_path), "output": [str(out_path)],
        "preset": preset_name, "operations": ops,
        "fallback_level": fb, "warnings": warn,
        "metrics": {"input_size_mb": round(in_mb,2), "output_size_mb": round(out_mb,2),
                    "duration_s": round(time.time()-t0,2), "output_dims": list(img.size)},
    }

# ───────── CLI helpers ─────────
def make_parser(desc: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=desc)

def check_input(path: Path):
    if not path.exists(): err(f"file non trovato: {path}")
