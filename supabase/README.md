# Supabase — TP Box

**Progetto**: `igtthymjeujkgfpmgoqj` | Regione: eu-west-3 | Status: ACTIVE_HEALTHY

## Schema DB

### `news_sources` — Whitelist fonti primarie istituzionali

> **REGOLA D'ORO**: solo fonti primarie istituzionali (OCSE, AdE, MEF, HMRC, IRS, ATO, CBDT, EU Commission).
> **ZERO** link/riferimenti ad aggregatori terzi (no regfollower, no taxsignals).

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | UUID | PK |
| `name` | TEXT | Nome fonte (UNIQUE) |
| `category` | TEXT | TP / VAT / P2 / AA |
| `country` | TEXT | ISO 3166-1 alpha-2 (IT, EU, US, UK, CA, AU, IN, INT) |
| `feed_url` | TEXT | URL RSS/Atom (NULL se HTML_WATCH) |
| `watch_type` | TEXT | RSS \| ATOM \| HTML_WATCH |
| `css_selector` | TEXT | Selector per HTML_WATCH |
| `enabled` | BOOL | Circuit breaker manuale |
| `last_fetched_at` | TIMESTAMPTZ | Ultimo fetch OK |
| `health_status` | TEXT | OK \| WARN \| ERROR \| DISABLED |
| `fail_count` | INT | Counter errori (≥3 = sospesa) |

### `news_items` — Articoli con workflow editoriale

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | UUID | PK |
| `title` | TEXT | Titolo articolo |
| `summary` | TEXT | Sommario in italiano (max 200 parole) |
| `content_markdown` | TEXT | Contenuto completo (opzionale) |
| `category` | TEXT | TP / VAT / P2 / AA |
| `country` | TEXT | ISO paese |
| `source_name` | TEXT | FK → news_sources.name |
| `source_url` | TEXT | URL originale articolo |
| `pdf_url` | TEXT | Link PDF ufficiale |
| `pdf_local_path` | TEXT | Path Supabase Storage |
| `normative_references` | JSONB | `[{tipo, numero, fonte, data, url}]` |
| `status` | TEXT | DRAFT → IN_REVIEW → PUBLISHED → ARCHIVED |
| `url_hash` | TEXT | MD5(source_url) — deduplicazione |
| `reviewed_by` | TEXT | Editor che ha approvato |
| `published_at` | TIMESTAMPTZ | Auto-set quando status = PUBLISHED |

## Workflow Editoriale

```
Fonte RSS/HTML → Agente AI → DRAFT
  → Editor umano review → IN_REVIEW
  → Approvazione → PUBLISHED
  → (24 mesi) → ARCHIVED
```

⚠️ **Nessuna pubblicazione automatica.** Il trigger `trg_news_items_published_at` setta `published_at` automaticamente ma lo status deve essere impostato manualmente dall'editor.

## RLS Policies

- `public_read_published`: SELECT pubblico solo su status = 'PUBLISHED'
- `service_role_full`: Edge Function — accesso completo
- `authenticated_full`: Editor autenticati — accesso completo

## Edge Function

`supabase/functions/fetch-primary-news/index.ts`

Deploy:
```bash
supabase functions deploy fetch-primary-news --project-ref igtthymjeujkgfpmgoqj
```

Segreti necessari (Supabase Vault):
```bash
supabase secrets set OPENAI_API_KEY=sk-... --project-ref igtthymjeujkgfpmgoqj
```

## GitHub Action

`.github/workflows/fetch-tax-news.yml`

Secret necessari su GitHub:
- `SUPABASE_URL` = `https://igtthymjeujkgfpmgoqj.supabase.co`
- `SUPABASE_SERVICE_ROLE_KEY` = service role key da Supabase Dashboard
- `OPENAI_API_KEY` = chiave OpenAI

## Normativa di riferimento

- **Transfer Pricing**: art. 110, comma 7 TUIR + Provvedimento AdE 21/11/2023 + OECD TPG 2022
- **Pillar Two**: D.Lgs. 209/2023 (recepimento Direttiva UE 2022/2523) + OECD GloBE Model Rules
- **VAT/IVA**: DPR 633/1972 + Direttiva UE 2006/112/CE
- **Anti-Avoidance**: art. 10-bis L. 212/2000 + ATAD 2016/1164 + BEPS Action 6
