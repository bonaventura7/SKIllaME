/**
 * Edge Function: fetch-primary-news
 * Progetto: TP Box — Portale Transfer Pricing
 * Workflow: RSS/ATOM/HTML_WATCH → DRAFT (review umana obbligatoria)
 *
 * REGOLA D'ORO:
 *   ✅ Solo fonti primarie istituzionali (OCSE, AdE, MEF, HMRC, IRS, ATO, CBDT, EU)
 *   ❌ ZERO link a aggregator terzi (no regfollower, no taxsignals)
 *   ✅ Articolo originale in italiano scritto dall'agente
 *   ✅ Nessuna pubblicazione automatica — solo DRAFT
 *
 * Normativa: art.110 c.7 TUIR | D.Lgs.209/2023 | ATAD 2016/1164 | art.10-bis L.212/2000
 *
 * SICUREZZA:
 *   verify_jwt = false (config.toml) — invocata da GitHub Actions senza JWT
 *   Guard: X-Cron-Secret header confrontato con CRON_SECRET env var
 */

import { createClient } from 'jsr:@supabase/supabase-js@2';

const SUPABASE_URL          = Deno.env.get('SUPABASE_URL')!;
const SUPABASE_SERVICE_ROLE = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const OPENAI_API_KEY        = Deno.env.get('OPENAI_API_KEY')!;
const CRON_SECRET           = Deno.env.get('CRON_SECRET')!;

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE);

// ── Tipi ────────────────────────────────────────────────────────────────────

interface NewsSource {
  id: string;
  name: string;
  category: 'TP' | 'VAT' | 'P2' | 'AA';
  country: string;
  feed_url: string | null;
  watch_type: 'RSS' | 'ATOM' | 'HTML_WATCH';
  css_selector: string | null;
  fail_count: number;
}

interface RawItem {
  title: string;
  url: string;
  pubDate?: string;
  description?: string;
}

interface NormativoRef {
  tipo: string;
  numero: string;
  fonte: string;
  data?: string;
  url?: string;
}

interface RequestBody {
  triggered_by?: string;
  force_refresh?: boolean;
  dry_run?: boolean;
}

// ── Parser RSS/ATOM ──────────────────────────────────────────────────────────

async function fetchRss(source: NewsSource): Promise<RawItem[]> {
  const url = source.feed_url!;
  const res = await fetch(url, { headers: { 'User-Agent': 'TPBox-NewsAgent/1.0' } });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  const xml = await res.text();

  const items: RawItem[] = [];
  const itemRegex  = /<item[^>]*>([\s\S]*?)<\/item>/gi;
  const entryRegex = /<entry[^>]*>([\s\S]*?)<\/entry>/gi;

  const parseBlock = (block: string): RawItem | null => {
    const title = block.match(/<title[^>]*><!\[CDATA\[([\s\S]*?)\]\]>|<title[^>]*>([^<]*)<\/title>/i);
    const link  = block.match(/<link[^>]*href="([^"]+)"|<link[^>]*>([^<]+)<\/link>/i);
    const date  = block.match(/<pubDate[^>]*>([^<]+)<\/pubDate>|<updated[^>]*>([^<]+)<\/updated>/i);
    const desc  = block.match(/<description[^>]*><!\[CDATA\[([\s\S]*?)\]\]>|<description[^>]*>([^<]*)<\/description>/i);

    const t = title?.[1] || title?.[2];
    const l = link?.[1]  || link?.[2];
    if (!t || !l) return null;

    return {
      title:       t.trim(),
      url:         l.trim(),
      pubDate:     (date?.[1] || date?.[2])?.trim(),
      description: (desc?.[1] || desc?.[2])?.trim(),
    };
  };

  let m;
  while ((m = itemRegex.exec(xml))  !== null) { const i = parseBlock(m[1]); if (i) items.push(i); }
  while ((m = entryRegex.exec(xml)) !== null) { const i = parseBlock(m[1]); if (i) items.push(i); }

  return items.slice(0, 20); // max 20 per source per run
}

// ── HTML_WATCH ───────────────────────────────────────────────────────────────

async function fetchHtmlWatch(source: NewsSource): Promise<RawItem[]> {
  if (!source.css_selector) throw new Error('css_selector mancante per HTML_WATCH');

  const baseUrl = source.feed_url || 'https://www.agenziaentrate.gov.it';
  const res = await fetch(baseUrl, { headers: { 'User-Agent': 'TPBox-NewsAgent/1.0' } });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const html = await res.text();

  const items: RawItem[] = [];
  const linkRegex = /<a[^>]+href="([^"]+)"[^>]*>([^<]{10,200})<\/a>/gi;
  let m;
  while ((m = linkRegex.exec(html)) !== null) {
    const href = m[1];
    const text = m[2].trim();
    if (!href || !text) continue;
    const fullUrl = href.startsWith('http') ? href : `${new URL(baseUrl).origin}${href}`;
    items.push({ title: text, url: fullUrl });
  }

  return items.slice(0, 20);
}

// ── Deduplicazione ───────────────────────────────────────────────────────────

async function isDuplicate(url: string): Promise<boolean> {
  const hash = await sha256(url);
  const { data } = await supabase
    .from('news_items')
    .select('id')
    .eq('url_hash', hash)
    .maybeSingle();
  return !!data;
}

// Usa SHA-256 (supportato nativamente da Deno, MD5 non è disponibile in SubtleCrypto)
async function sha256(str: string): Promise<string> {
  const buf     = new TextEncoder().encode(str);
  const hashBuf = await crypto.subtle.digest('SHA-256', buf);
  return Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

// ── GPT: sommario in italiano ─────────────────────────────────────────────────

async function gptSummarize(item: RawItem, source: NewsSource): Promise<{
  summary: string;
  normative_references: NormativoRef[];
}> {
  const prompt = `Sei un esperto di fiscalità internazionale italiano.

Fonte istituzionale: ${source.name} (${source.country})
Categoria: ${source.category}
Titolo originale: ${item.title}
Descrizione: ${item.description || 'N/A'}
URL originale: ${item.url}

Scrivi:
1. Un sommario originale in italiano di max 200 parole. Non copiare il testo originale. Non citare siti aggregatori.
2. I riferimenti normativi applicabili in formato JSON array: [{"tipo":"articolo","numero":"110, comma 7","fonte":"TUIR","url":"https://www.normattiva.it/..."}]

Riferimenti normativi per categoria:
- TP: art.110 c.7 TUIR, Provvedimento AdE 21/11/2023, OECD TPG 2022 cap.I-IV
- P2: D.Lgs.209/2023, OECD GloBE Model Rules, Direttiva UE 2022/2523
- VAT: DPR 633/1972, Direttiva UE 2006/112/CE
- AA: art.10-bis L.212/2000, ATAD 2016/1164, BEPS Action 6

Rispondi SOLO con JSON:
{"summary": "...", "normative_references": [...]}`;

  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model:           'gpt-4o-mini',
      messages:        [{ role: 'user', content: prompt }],
      max_tokens:      800,
      temperature:     0.3,
      response_format: { type: 'json_object' },
    }),
  });

  if (!res.ok) throw new Error(`OpenAI error: ${res.status}`);
  const data    = await res.json();
  const content = data.choices?.[0]?.message?.content || '{}';
  return JSON.parse(content);
}

// ── Main handler ─────────────────────────────────────────────────────────────

Deno.serve(async (req: Request) => {

  // ─── GUARD: X-Cron-Secret ──────────────────────────────────────────────────
  // verify_jwt = false in config.toml: la funzione è invocata da GitHub Actions
  // senza JWT utente. Sicurezza garantita da X-Cron-Secret confrontato con
  // la variabile d'ambiente CRON_SECRET (impostata via: supabase secrets set)
  // ──────────────────────────────────────────────────────────────────────────
  const incomingSecret = req.headers.get('X-Cron-Secret');

  if (!CRON_SECRET || !incomingSecret || incomingSecret !== CRON_SECRET) {
    return new Response(
      JSON.stringify({ error: 'Unauthorized: invalid or missing cron secret' }),
      { status: 401, headers: { 'Content-Type': 'application/json' } }
    );
  }
  // ─── fine guard ────────────────────────────────────────────────────────────

  // Leggi parametri dal body
  let body: RequestBody = {};
  try {
    body = await req.json();
  } catch {
    // body opzionale — se assente usa defaults
  }

  const dryRun       = body.dry_run       === true;
  const forceRefresh = body.force_refresh === true;
  const triggeredBy  = body.triggered_by  || 'manual';

  const runResults: Record<string, unknown> = {};
  let totalFetched  = 0;
  let totalInserted = 0;
  let totalDuplicate = 0;

  // Fetch fonti abilitate
  const { data: sources, error: srcErr } = await supabase
    .from('news_sources')
    .select('*')
    .eq('enabled', true)
    .lt('fail_count', 3); // circuit breaker: salta fonti con 3+ errori

  if (srcErr || !sources) {
    return new Response(
      JSON.stringify({ error: 'Failed to load sources', detail: srcErr?.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  for (const source of sources as NewsSource[]) {
    try {
      const items = source.watch_type === 'HTML_WATCH'
        ? await fetchHtmlWatch(source)
        : await fetchRss(source);

      totalFetched += items.length;
      let inserted  = 0;
      let duplicate = 0;

      for (const item of items) {
        // Deduplicazione (salta se force_refresh=true)
        if (!forceRefresh && await isDuplicate(item.url)) {
          duplicate++;
          continue;
        }

        if (dryRun) {
          // Dry run: logga ma non scrive
          console.log(`[DRY RUN] Would insert: ${item.title}`);
          inserted++;
          continue;
        }

        // GPT summarize
        const { summary, normative_references } = await gptSummarize(item, source);

        // INSERT come DRAFT — mai automaticamente PUBLISHED
        const hash = await sha256(item.url);
        const { error: insertErr } = await supabase.from('news_items').insert({
          title:                item.title,
          summary,
          category:             source.category,
          country:              source.country,
          source_name:          source.name,
          source_url:           item.url,
          url_hash:             hash,
          pdf_url:              item.url.endsWith('.pdf') ? item.url : null,
          normative_references: normative_references,
          status:               'DRAFT',  // ← SEMPRE DRAFT — review umana obbligatoria
          pub_date:             item.pubDate ? new Date(item.pubDate).toISOString() : null,
        });

        if (!insertErr) inserted++;
        else console.error(`Insert error for ${item.url}:`, insertErr.message);
      }

      totalInserted  += inserted;
      totalDuplicate += duplicate;

      // Reset fail_count + aggiorna last_fetched_at (solo se non dry_run)
      if (!dryRun) {
        await supabase.from('news_sources').update({
          last_fetched_at: new Date().toISOString(),
          fail_count:      0,
          health_status:   'OK',
        }).eq('id', source.id);
      }

      runResults[source.name] = { ok: true, fetched: items.length, inserted, duplicate };

    } catch (err) {
      // Circuit breaker: incrementa fail_count
      if (!dryRun) {
        await supabase.from('news_sources').update({
          fail_count:    source.fail_count + 1,
          health_status: source.fail_count + 1 >= 3 ? 'ERROR' : 'WARN',
        }).eq('id', source.id);
      }

      runResults[source.name] = { ok: false, error: String(err) };
      console.error(`Source ${source.name} failed:`, err);
    }
  }

  return new Response(
    JSON.stringify({
      success:         true,
      dry_run:         dryRun,
      triggered_by:    triggeredBy,
      items_fetched:   totalFetched,
      items_inserted:  totalInserted,
      items_duplicate: totalDuplicate,
      sources:         runResults,
      timestamp:       new Date().toISOString(),
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
});
