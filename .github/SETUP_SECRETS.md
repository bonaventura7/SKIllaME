# 🔐 Setup Segreti — News Monitor GitHub Actions

## Come configurare

**GitHub → Repository → Settings → Secrets and variables → Actions → New repository secret**

---

## Segreti obbligatori

| Nome segreto | Dove trovarlo | Esempio formato |
|---|---|---|
| `SUPABASE_ACCESS_TOKEN` | [supabase.com/dashboard/account/tokens](https://supabase.com/dashboard/account/tokens) | `sbp_...` |
| `SUPABASE_PROJECT_REF` | Dashboard → Project Settings → General | `abcdefghijklmnop` (16 char) |
| `SUPABASE_ANON_KEY` | Dashboard → Settings → API → **anon public** | `eyJhbGci...` |
| `CRON_SECRET` | Genera con `openssl rand -hex 32` | `a1b2c3...` (64 char) |

## Segreto opzionale

| Nome segreto | Dove trovarlo |
|---|---|
| `SLACK_WEBHOOK_URL` | Slack → Manage Apps → Incoming Webhooks |

---

## Sicurezza Edge Function — X-Cron-Secret

Poiché `verify_jwt = false` in `supabase/config.toml`, la funzione deve validare
il segreto custom nell'header `X-Cron-Secret`.

### Snippet da aggiungere in `supabase/functions/fetch-primary-news/index.ts`

```typescript
// ─── Guard: X-Cron-Secret (invocazione da GitHub Actions) ───
const CRON_SECRET = Deno.env.get('CRON_SECRET')
const incomingSecret = req.headers.get('X-Cron-Secret')

if (!CRON_SECRET || !incomingSecret || incomingSecret !== CRON_SECRET) {
  return new Response(
    JSON.stringify({ error: 'Unauthorized: invalid or missing cron secret' }),
    { status: 401, headers: { 'Content-Type': 'application/json' } }
  )
}
// ─── fine guard ─────────────────────────────────────────────
```

### Imposta CRON_SECRET su Supabase

```bash
# Stesso valore del segreto GitHub CRON_SECRET
supabase secrets set CRON_SECRET=<il-tuo-valore-hex> \
  --project-ref <SUPABASE_PROJECT_REF>
```

Oppure dalla Dashboard: **Supabase → Edge Functions → fetch-primary-news → Secrets**

---

## Schedule configurato

| Cron expression | Giorno | Ora UTC | Ora italiana (CEST) |
|---|---|---|---|
| `0 7 * * 1` | Lunedì | 07:00 | 09:00 |
| `0 7 * * 4` | Giovedì | 07:00 | 09:00 |

---

## Trigger manuale

### Via GitHub CLI

```bash
# Run standard
gh workflow run "news-monitor.yml"

# Con parametri
gh workflow run "news-monitor.yml" \
  -f force_refresh=true \
  -f dry_run=false

# Dry run (non scrive su DB)
gh workflow run "news-monitor.yml" \
  -f dry_run=true
```

### Via GitHub UI

**Actions → 📰 News Monitor — Fetch & Ingest → Run workflow**

---

## Verifica funzionamento

Dopo il primo run, controlla:

1. **GitHub Actions Summary** — tabella con `items_fetched / inserted / duplicates`
2. **Supabase Dashboard → Table Editor → news_items** — righe con `status = DRAFT`
3. **Supabase → Edge Functions → Logs** — dettaglio esecuzione funzione

---

## Architettura HA del workflow

```
github.schedule (lun + gio 07:00 UTC)
        │
        ▼
   JOB 1: deploy
   supabase functions deploy fetch-primary-news
        │
        │ needs: deploy (se fallisce → stop)
        ▼
   JOB 2: invoke
   POST /functions/v1/fetch-primary-news
   Header: X-Cron-Secret
   Retry: 3x con delay 10s
   Timeout: 120s
        │
        │ if: failure()
        ▼
   JOB 3: notify-failure
   GitHub Annotation + Slack (opzionale)
```

**Garanzie HA:**
- `concurrency.cancel-in-progress: false` → nessun run parallelo corrode l'ingest
- `needs: deploy` → l'invocazione parte solo se il deploy è riuscito
- `--retry 3 --retry-delay 10` → resilienza su errori di rete transitori
- `timeout-minutes: 15` su invoke → evita job bloccati infinitamente
