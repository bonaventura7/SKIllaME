#!/usr/bin/env python3
"""setup.py — Installa dipendenze smart (rileva mancanti)."""
import importlib.util, json, subprocess, sys

REQ = {"Pillow":"PIL", "numpy":"numpy"}
REC = {"opencv-python":"cv2", "rembg":"rembg", "onnxruntime":"onnxruntime"}
OPT = {"requests":"requests"}

def has(m): return importlib.util.find_spec(m) is not None
def pip_install(pkgs):
    if not pkgs: return True
    try: subprocess.check_call([sys.executable,"-m","pip","install","--quiet",*pkgs]); return True
    except subprocess.CalledProcessError: return False

def main():
    rep = {"installed_now":[], "failed":[]}
    for label, group in (("required",REQ), ("recommended",REC)):
        rep[label] = {p: has(m) for p,m in group.items()}
        missing = [p for p,m in group.items() if not has(m)]
        if missing:
            ok = pip_install(missing)
            (rep["installed_now"] if ok else rep["failed"]).extend(missing)
    rep["optional"] = {p: has(m) for p,m in OPT.items()}
    rep["status"] = "ok" if all(has(m) for m in REQ.values()) else "error"
    print(json.dumps(rep, indent=2))

if __name__ == "__main__": main()
