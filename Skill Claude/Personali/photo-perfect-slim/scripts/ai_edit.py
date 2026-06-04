#!/usr/bin/env python3
"""ai_edit.py — Livello 3 (cloud AI via OpenRouter).
Uso:
  python ai_edit.py IN --prompt NAME [--out P]   ← editing immagine
  python ai_edit.py --gen "testo libero"          ← generazione da zero
"""
from __future__ import annotations
import base64, json, os, sys, time
from pathlib import Path

try: import requests
except ImportError:
    print(json.dumps({"status":"error","error":"pip install requests"})); sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import make_parser, load_prompt, out, err

API = "https://openrouter.ai/api/v1/chat/completions"
M1  = "google/gemini-3-pro-image-preview"
M2  = "black-forest-labs/flux-2-pro"

def enc(p: Path) -> str:
    ext = p.suffix.lstrip(".").lower().replace("jpg","jpeg")
    return f"data:image/{ext};base64,{base64.b64encode(p.read_bytes()).decode()}"

def call(model, prompt, img_b64, key):
    content = [{"type":"text","text":prompt}]
    if img_b64: content.append({"type":"image_url","image_url":{"url":img_b64}})
    r = requests.post(API, timeout=120,
        json={"model":model,"messages":[{"role":"user","content":content}]},
        headers={"Authorization":f"Bearer {key}","Content-Type":"application/json",
                 "HTTP-Referer":"https://photo-perfect.dev","X-Title":"photo-perfect"})
    r.raise_for_status(); return r.json()

def extract(resp, dst: Path) -> bool:
    try:
        msg = resp["choices"][0]["message"]
        if msg.get("images"):
            url = msg["images"][0].get("image_url",{}).get("url") or msg["images"][0].get("url","")
            if url.startswith("data:"):
                dst.write_bytes(base64.b64decode(url.split(",",1)[1])); return True
        if isinstance(msg.get("content"), list):
            for b in msg["content"]:
                if b.get("type") == "image_url" and b["image_url"]["url"].startswith("data:"):
                    dst.write_bytes(base64.b64decode(b["image_url"]["url"].split(",",1)[1])); return True
    except (KeyError, IndexError): pass
    return False

def main():
    p = make_parser("AI edit cloud (OpenRouter)")
    p.add_argument("input", nargs="?", type=Path)
    p.add_argument("--prompt"); p.add_argument("--prompt-text"); p.add_argument("--gen")
    p.add_argument("--model", default=M1)
    p.add_argument("--out", type=Path, default=Path("ai_output.png"))
    p.add_argument("--api-key", default=os.getenv("OPENROUTER_API_KEY"))
    a = p.parse_args()
    if not a.api_key: err("OPENROUTER_API_KEY mancante", hint="https://openrouter.ai/keys")
    t0 = time.time()
    if a.gen:
        prompt, b64 = a.gen, None
    else:
        if not a.input or not a.input.exists(): err("input richiesto se non --gen")
        prompt, neg = load_prompt(a.prompt, a.prompt_text)
        prompt += f"\n\nNegative: {neg}"; b64 = enc(a.input)
    try: resp = call(a.model, prompt, b64, a.api_key); used = a.model
    except requests.HTTPError:
        resp = call(M2, prompt, b64, a.api_key); used = M2
    if not extract(resp, a.out): err("nessuna immagine nella risposta", raw=resp)
    out({"status":"ok","input":str(a.input) if a.input else None,"output":[str(a.out)],
         "model":used,"fallback_level":3,"prompt_used":a.prompt or "custom",
         "metrics":{"duration_s":round(time.time()-t0,2)}})

if __name__ == "__main__": main()
