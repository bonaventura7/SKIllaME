# CLAUDE.md — Istruzioni per Claude Code, OpenHands, Perplexity

> Letto automaticamente da Claude Code, OpenHands e Perplexity Spaces.
> Versione: 2.0 | Aggiornato: Giugno 2026

---

## Contesto Utente

- **Ruolo**: Tributarista + Senior Solutions Architect
- **Studio**: Biscozzi Nobili & Partners, Boves (CN) — Piemonte
- **Specializzazione**: Transfer Pricing, fiscalità internazionale, workflow HA
- **Stack tecnico preferito**: Python 3.12+, FastAPI, n8n, OpenHands, OpenRouter

---

## Regole di Comportamento

### Obbligatorio
1. **Brainstorm prima** — mai rispondere senza analisi preliminare
2. **Piano strutturato** — sempre prima del codice o della soluzione
3. **TDD** per codice: RED → GREEN → REFACTOR
4. **Quality gate** prima di consegnare qualsiasi output
5. **Cita sempre** la fonte normativa (art. + testo normativo + anno)
6. **Rollback plan** per ogni cambiamento rilevante
7. **Skill auto-load** — carica le skill da `.github/skills/` quando pertinenti

### Skill Trigger → File
- Transfer Pricing → `.github/skills/transfer-pricing/SKILL.md`
- Fiscalità internazionale → `.github/skills/fiscalita-internazionale/SKILL.md`
- Workflow / automazione → `.github/skills/architettura-workflow/SKILL.md`
- Pillar Two / GloBE → `.github/skills/pillar-two/SKILL.md`

---

## Preferenze Tecniche

```yaml
language: Python 3.12+
framework: FastAPI + Pydantic v2
test: pytest + coverage ≥ 80%
linting: ruff + mypy strict
security: bandit, no bare except, no eval/exec
logging: structured JSON + correlation_id
tracing: OpenTelemetry
secrets: env vars / HashiCorp Vault (mai hardcoded)
```

---

## Output Default per Risposte Complesse

```
## 🧠 Mente Locale
## 📋 Piano Operativo  
## ✅ Soluzione
## 🔧 Workaround / Fallback
## ⚠️ Rischi e Mitigazioni
## 🔍 Validazione
## 🚀 Prossimi Passi
```
