---
name: photo-perfect
version: 2.0.0-slim
description: |
  Ritocco foto HA per uso generale e marketplace (Vinted, eBay, Amazon).
  Pipeline 3 livelli (Pillow → OpenCV+rembg → Cloud AI Gemini/FLUX).
  Vestiti, scarpe, borse, oggetti singoli, product shot. Output JSON.
  Edizione SLIM: 8 file totali. Tutti i preset e prompt in skill.json.
  Trigger: "ritocco foto", "foto vinted", "scontorna", "product shot",
  "batch foto", "rimuovi sfondo", "enhance image", "preparare foto vestito".
license: MIT
agents: [claude-code, cursor, codex, gemini, windsurf, cline, copilot]
tags: [photo, vinted, ecommerce, retouch, background-removal, slim]
---

# 📸 photo-perfect (SLIM — 8 file)

## 🧠 Decision tree (esegui PRIMA di agire)

```
1. SOGGETTO?
   vestito → preset vinted-clothing  (retouch.py photo  oppure vinted)
   scarpe  → preset vinted-shoes     (retouch.py photo  oppure vinted)
   borsa   → preset vinted-accessory (retouch.py photo  oppure vinted)
   oggetto → preset product-white    (retouch.py photo  oppure batch)
   ritratto→ preset portrait-natural (retouch.py photo)
   generico→ preset general-enhance  (retouch.py photo  oppure enhance)
   vecchia → preset restore-old      (retouch.py photo)

2. QUANTE FOTO?
   1                   → retouch.py photo IN [--preset N]
   N (stesso preset)   → retouch.py batch DIR --preset N --out DIR
   set Vinted          → retouch.py vinted DIR --item-type T --out DIR

3. SOLO SFONDO?       → retouch.py bg IN [--replace COLOR|transparent]
4. SOLO ENHANCE?      → retouch.py enhance IN --auto
5. CASO COMPLESSO?    → ai_edit.py IN --prompt NAME (richiede API key)
```

## 🛡️ Pipeline HA — fallback automatici

| Livello | Engine | Sempre on |
|---|---|---|
| 1 | Pillow + NumPy | ✅ |
| 2 | OpenCV (CLAHE/denoise) + rembg (bg) | se installati |
| 3 | OpenRouter (Gemini 3 Pro Image / FLUX.2 Pro) | opt-in API key |

Se un livello fallisce → degrada al successivo, `status: degraded`, warning nel JSON.

## 🚀 Quick start

```bash
python scripts/setup.py                                                    # install deps
python scripts/retouch.py photo foto.jpg --preset vinted-clothing          # 1 foto
python scripts/retouch.py vinted ./scatti/ --item-type sweater --out ./v/  # set completo
python scripts/retouch.py batch ./prodotti/ --preset product-white --out ./o/ --jobs 4
python scripts/retouch.py bg foto.jpg --replace transparent                # scontorno
python scripts/retouch.py enhance foto.jpg --auto                          # enhance
python scripts/ai_edit.py foto.jpg --prompt vinted_clothing_cleanup        # AI cloud
```

## 🚫 Compliance Vinted (hard-coded)

- ❌ Niente watermark / testo / logo overlay
- ❌ Non rimuovere difetti reali (macchie, pilling, fori)
- ❌ Non alterare brand label / tag autenticità
- ✅ Strip EXIF GPS · sRGB forzato · compressione auto se > 20 MB

## 📂 Files (8 totali)

```
photo-perfect/
├── SKILL.md                ← questa skill def
├── skill.json              ← manifest + 7 preset + prompt AI (3-in-1)
├── .gitignore
├── references/handbook.md  ← § 1 Vinted · § 2 Product · § 3 Retouch · § 4 Color · § 5 Troubleshoot
└── scripts/
    ├── core.py             ← logica condivisa
    ├── retouch.py          ← multi-comando (photo|vinted|batch|bg|enhance)
    ├── ai_edit.py          ← cloud AI separato (deps diverse)
    └── setup.py            ← installer
```

## 📤 Output JSON (tutti gli script)

```json
{"status":"ok|degraded|partial|error","input":"...","output":["..."],
 "preset":"...","operations":[...],"fallback_level":1|2|3,
 "warnings":[...],"metrics":{"input_size_mb":0,"output_size_mb":0,
 "duration_s":0,"output_dims":[w,h]}}
```

## ⚡ Install

```bash
npx skills add your-org/photo-perfect       # via skills.sh
# oppure manuale:
git clone <repo> ~/.claude/skills/photo-perfect
cd $_ && python scripts/setup.py
```

## 🔗 Spec
- Standard: https://skills.sh — Spec: https://agentskills.io
- License: MIT
