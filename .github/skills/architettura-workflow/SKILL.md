---
name: architettura-workflow
description: >-
  Progettazione di workflow complessi ad alta resilienza (HA). Usa per
  automazioni, pipeline dati, agenti AI, integrazioni n8n/API, sistemi
  fault-tolerant con retry, circuit breaker, DLQ e rollback plan.
tags: [architettura, HA, resilienza, workflow, automazione, n8n, agenti-AI]
---

# Skill: Architettura Workflow HA

## Quando Usarla

Attiva per:
- Progettazione workflow di automazione (n8n, Make, Zapier, Python)
- Integrazione API con requisiti di affidabilità elevata
- Pipeline dati per analisi fiscale/TP
- Sistemi multi-agente (LangChain, CrewAI, OpenHands, n8n AI)
- Qualsiasi processo che richiede fault-tolerance, retry, monitoring

## Principi HA Applicati

### Resilienza
- **Timeout** espliciti su ogni chiamata esterna (mai infiniti)
- **Retry** con exponential backoff + jitter (max 3 tentativi)
- **Circuit breaker**: apri dopo N fallimenti consecutivi, ripristina gradualmente
- **Bulkhead**: isola componenti critici (no cascading failure)
- **DLQ** (Dead Letter Queue): cattura messaggi falliti per re-processing manuale
- **Idempotency**: ogni operazione deve essere sicura se ripetuta

### Osservabilità
```
- Structured logs (JSON) con correlation_id
- Metriche RED: Rate, Errors, Duration
- Health check endpoint: /health, /ready
- Alerting su SLO-based error budget
- OpenTelemetry tracing end-to-end
```

### Sicurezza
- Secrets in env vars o vault (mai hardcoded)
- Least privilege su ogni integrazione
- Input validation prima di ogni elaborazione
- No dati sensibili nei log

## Template Workflow Standard

```
[Trigger] → [Validate Input] → [Enrich/Transform]
     ↓ error                        ↓ error
  [DLQ/Alert]               [Retry w/ backoff]
                                     ↓ success
                            [Execute Core Logic]
                                     ↓
                            [Emit Event/Response]
                                     ↓
                            [Log + Metrics]
```

## Workaround Smart Policy

Se la soluzione ideale è bloccata:
1. **Cosa facciamo ora**: descrivi la soluzione temporanea
2. **Perché funziona**: motivazione tecnica
3. **Limite**: cosa non copre
4. **Rischio residuo**: cosa può andare storto
5. **Evoluzione**: piano verso soluzione definitiva con timeline

## Stack Preferito

| Layer | Tool | Note |
|-------|------|------|
| Orchestrazione | n8n self-hosted | Open source, HA con PostgreSQL |
| Backend | Python 3.12 + FastAPI | Async, type hints, Pydantic v2 |
| AI Agents | OpenHands / LangGraph | Con OpenRouter per model routing |
| Monitoring | Prometheus + Grafana | O Datadog se cloud |
| Secrets | HashiCorp Vault / env | Mai nel codice |
| DB | PostgreSQL | Con read replica per HA |

## Output Atteso

1. Diagramma architettura (Mermaid o ASCII)
2. Piano implementazione step-by-step
3. Checklist HA/resilienza
4. Rollback plan
5. Runbook operativo
