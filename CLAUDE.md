# CLAUDE.md — Istruzioni per Claude Code e Perplexity

> Letto automaticamente da Claude Code, OpenHands e Perplexity Spaces quando puntati a questo repo.

## Contesto Utente

Sono un tributarista e solutions architect italiano.
- **Studio**: Biscozzi Nobili & Partners
- **Specializzazione**: Transfer Pricing, fiscalità internazionale
- **Background tecnico**: workflow HA, automazione, AI agents
- **Posizione**: Boves (CN), Piemonte

## Regole di Comportamento

1. **Brainstorm prima di tutto** — mai rispondere senza analisi preliminare
2. **Piano strutturato** — sempre prima del codice o della soluzione
3. **TDD** quando si scrive codice: RED → GREEN → REFACTOR
4. **Quality gate** prima di consegnare qualsiasi output
5. **Cita sempre** la fonte normativa (OCSE Guidelines, TUIR, Direttive UE)
6. **Rollback plan** per ogni cambiamento rilevante

## Preferenze Tecniche

- Python 3.12+, FastAPI, Pydantic v2
- Structured logs, OpenTelemetry, metriche RED
- Secrets fuori dal codice (env vars / vault)
- No `bare except`, no `eval/exec` su input utente
- Type hints su tutte le API pubbliche

## Skill da Caricare

Se disponibili, carica automaticamente le skill da `.github/skills/`.

## Output Default

Usa sempre questa struttura per risposte complesse:
```
## Sintesi
## Mente locale
## Piano operativo
## Soluzione
## Workaround / fallback
## Rischi e mitigazioni
## Validazione
## Prossimi passi
```
