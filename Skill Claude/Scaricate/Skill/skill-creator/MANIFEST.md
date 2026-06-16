# 📦 MANIFEST — Skill-Creator (Anthropic)

> **Origine:** https://github.com/anthropics/skills/tree/main/skills/skill-creator
> **Data download:** 16 giugno 2026
> **Metodo:** GitHub tarball `main` branch + estrazione selettiva della sottocartella
> **Integrità:** ✅ 100% — tutti i 18 file hanno git-blob SHA-1 identico all'API GitHub

---

## 🎯 A cosa serve

**Skill Creator** è una *meta-skill* (una skill che serve a creare altre skill). Permette di:

1. ✍️ **Creare nuove skill** da zero
2. ✏️ **Modificare skill esistenti**
3. 📊 **Misurare le performance** di una skill (benchmarking con analisi della varianza)
4. 🎯 **Ottimizzare la description** per migliorare il triggering (cioè quando Claude decide di usarla)

### Il loop fondamentale

```
Decidi cosa deve fare → Scrivi bozza → Crea test prompts →
Lancia eval (con skill vs senza skill = baseline) →
Review umana + benchmark quantitativo →
Migliora → Ripeti → Pacchettizza (.skill file)
```

---

## 📁 STRUTTURA SCARICATA (18 file, ~272 KB)

```
skill-creator/
├── LICENSE.txt                          11.345 B   Apache 2.0
├── SKILL.md                             33.168 B   📘 File principale (486 righe)
│
├── agents/                                          Sub-agents per compiti specializzati
│   ├── analyzer.md                       10.376 B   Analizza perché una versione batte l'altra
│   ├── comparator.md                      7.287 B   Confronto blind A/B tra due output
│   └── grader.md                          9.049 B   Valuta assertions contro output
│
├── assets/                                          Template HTML
│   └── eval_review.html                   7.058 B   Template per review umana delle trigger evals
│
├── eval-viewer/                                     Viewer HTML interattivo
│   ├── generate_review.py                16.365 B   Genera HTML report da workspace iteration
│   └── viewer.html                       44.998 B   Viewer interattivo (Outputs + Benchmark tab)
│
├── references/                                      Documentazione di riferimento
│   └── schemas.md                        12.061 B   Schemi JSON: evals.json, grading.json, benchmark.json
│
└── scripts/                                         Automazione Python (8 moduli)
    ├── __init__.py                            0 B   Marker package
    ├── aggregate_benchmark.py             14.386 B   Aggrega metriche (mean ± stddev, delta)
    ├── generate_report.py                 12.847 B   Genera report markdown
    ├── improve_description.py             11.116 B   Ottimizza description (loop di triggering)
    ├── package_skill.py                    4.234 B   Crea .skill file (ZIP-like)
    ├── quick_validate.py                   3.972 B   Validazione rapida skill
    ├── run_eval.py                        11.464 B   Esegue eval su test prompts
    ├── run_loop.py                        13.605 B   Loop completo di ottimizzazione description
    └── utils.py                            1.661 B   Utilities condivise
```

---

## 🔐 INTEGRITY CHECK (SHA-1 git blob)

Tutti i 18 file verificati con calcolo git-blob SHA-1:

| File | SHA-1 (atteso da GitHub) | Verifica |
|---|---|---|
| LICENSE.txt | `4f881c52d1f72f4cfb720e339e2d35c3058d01a9` | ✅ |
| SKILL.md | `65b3a402dbd09b8e83f9d637c6b553875189085c` | ✅ |
| agents/analyzer.md | `14e41d6068635f4dd3fb878fd1626312395dda63` | ✅ |
| agents/comparator.md | `80e00eb45db3ee53a132fc2ba97fd59a7339e563` | ✅ |
| agents/grader.md | `558ab05c0a9a8bb062ef4c51823d4d76c3acf7c4` | ✅ |
| assets/eval_review.html | `938ff32aed9bffabf723bd5492d720f4736c8e4d` | ✅ |
| eval-viewer/generate_review.py | `7fa5978631fed1ed545591dbb2b0eb21ce3f3d08` | ✅ |
| eval-viewer/viewer.html | `6d8e96348a02e66c3363d2ff3b3ae58ac11e6382` | ✅ |
| references/schemas.md | `b6eeaa2d4a34c1653069585c6c5603da39a5bdbe` | ✅ |
| scripts/__init__.py | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | ✅ |
| scripts/aggregate_benchmark.py | `3e66e8c105be9bab9f0e9c61f0d1482619401580` | ✅ |
| scripts/generate_report.py | `959e30a0014ec165c41a2bb7420b7dfe1416bbac` | ✅ |
| scripts/improve_description.py | `06bcec76122446986e3610c20a39c466de36f495` | ✅ |
| scripts/package_skill.py | `f48eac444656ddc41204aac1760a217951ce609e` | ✅ |
| scripts/quick_validate.py | `ed8e1dddce77b16af13c6f36b3fe86c4ac7c590c` | ✅ |
| scripts/run_eval.py | `e58c70bea39d5b252a1e819f242bbdcdf20e8b87` | ✅ |
| scripts/run_loop.py | `30a263d674ef19de11c756d6f7537f91a421909e` | ✅ |
| scripts/utils.py | `51b6a07dd57174197a937034b7eecebd5768ff8a` | ✅ |

**Esito:** 18/18 file identici al repository ufficiale.

---

## 🧠 ANATOMIA DI UNA SKILL (riferimento da SKILL.md)

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Codice eseguibile per task deterministici/ripetitivi
    ├── references/ - Docs caricati in contesto quando servono
    └── assets/     - File usati in output (template, icone, font)
```

### Sistema di loading progressivo (3 livelli)

1. **Metadata** (name + description) → **sempre in contesto** (~100 parole)
2. **SKILL.md body** → **in contesto quando la skill triggera** (<500 righe ideali)
3. **Bundled resources** → **on-demand** (illimitati, gli script possono eseguire senza caricarli)

---

## 🚀 COME USARLA

### Uso base (Claude Code / Cowork)

1. **Trigger:** chiedi *"crea una skill per X"* oppure *"migliora questa skill esistente"*
2. La skill ti guida attraverso:
   - Capture Intent (cosa deve fare la skill)
   - Interview & Research
   - Scrivere SKILL.md (con YAML frontmatter)
   - Creare test cases in `evals/evals.json`
   - Spawn di sub-agents per ogni test (with-skill + baseline)
   - Grading (sub-agent `grader.md`) + Aggregation (script `aggregate_benchmark.py`)
   - Viewer interattivo (`generate_review.py`)
   - Iterazione fino a soddisfazione
   - Packaging (`package_skill.py` → `.skill` file)

### Comandi CLI principali

```bash
# Validazione rapida
python -m scripts.quick_validate <path-to-skill>

# Aggrega metriche di un'iterazione
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>

# Loop ottimizzazione description (richiede claude CLI)
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose

# Pacchettizza skill in .skill file
python -m scripts.package_skill <path/to/skill-folder>
```

---

## 🎓 BEST PRACTICES ESTRATTI DALLA SKILL

### Per scrivere una SKILL.md efficace

1. **description "pushy"** — Claude tende a *non* triggereare le skill. Scrivi la description in modo che "spinga" all'uso (es. *"Use this whenever the user mentions X, even if they don't explicitly ask"*).
2. **Principio of Lack of Surprise** — niente malware, niente exploit. Niente sorprese rispetto a quanto dichiarato.
3. **Tono imperativo** — usa "DO this" non "MUST this". Spiega il *perché*.
4. **Esempi concreti** — includi Input/Output per i pattern ripetuti.
5. **Sotto-organizzazione per dominio** — `references/aws.md`, `references/gcp.md`, `references/azure.md` → Claude legge solo il file rilevante.

### Per migliorare iterativamente

1. **Generalizza dal feedback**, non overfittare su pochi esempi.
2. **Tieni il prompt lean** — togli ciò che non porta valore.
3. **Spiega il *perché*** — gli LLM sono *smart*, rispondono meglio a ragionamenti che a MUST rigidi.
4. **Cerca lavoro ripetuto** nei transcript dei test → se tutti i sub-agents scrivono lo stesso helper script, mettilo in `scripts/`.

---

## 📜 LICENZA

**Apache License 2.0** — vedi `LICENSE.txt`.
Copyright Anthropic.

---

## ⚙️ NOTE TECNICHE SUL DOWNLOAD

- **Metodo usato:** `curl` su GitHub tarball (più efficiente di 18 fetch singoli)
- **Dimensione tarball:** 3.6 MB (compressa), 272 KB (estraendo solo skill-creator)
- **Branch scaricato:** `main`
- **Ultimo commit noto (al download):** 20 aprile 2026 (`b9e19e6`)
- **Repository:** https://github.com/anthropics/skills — 17.9k fork, 151k star

---

*Manifest generato automaticamente dopo download + integrity check.*
