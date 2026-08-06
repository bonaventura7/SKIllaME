/**
 * News Repository — Supabase-or-Demo pattern
 *
 * Se NEXT_PUBLIC_SUPABASE_URL è definito → legge da Supabase (TP Box)
 * Altrimenti → fallback a DEMO_NEWS (sviluppo locale)
 *
 * IMPORTANTE: questo repository espone solo articoli PUBLISHED.
 * La gestione DRAFT/IN_REVIEW avviene tramite Supabase Dashboard o admin panel.
 */

import type { NewsFilters, NewsFeedResult, NewsItem, NewsCategory } from '../types/news';

// ── Demo data (fallback dev locale) ─────────────────────────────────────────

const DEMO_NEWS: NewsItem[] = [
  {
    id: 'demo-001',
    title: 'OCSE pubblica aggiornamento alle Linee Guida Transfer Pricing 2025',
    summary: 'L'OCSE ha rilasciato un aggiornamento significativo alle Linee Guida sui prezzi di trasferimento (TPG), con modifiche al capitolo I relativo al principio di libera concorrenza e al capitolo VI sulla proprietà intellettuale. Le nuove disposizioni rafforzano i requisiti documentali per le operazioni infragruppo ad alto valore e introducono chiarimenti sui comparabili geografici.',
    category: 'TP',
    country: 'INT',
    source_name: 'OECD Tax News',
    source_url: 'https://www.oecd.org/tax/transfer-pricing/',
    normative_references: [
      { tipo: 'articolo', numero: '110, comma 7', fonte: 'TUIR', url: 'https://www.normattiva.it/' },
      { tipo: 'legge', numero: 'TPG 2022 Cap. I-IV', fonte: 'OECD', url: 'https://www.oecd.org/tax/transfer-pricing/oecd-transfer-pricing-guidelines.htm' },
    ],
    status: 'PUBLISHED',
    url_hash: 'demo001hash',
    published_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 'demo-002',
    title: 'Pillar Two: MEF pubblica chiarimenti applicativi al D.Lgs. 209/2023',
    summary: 'Il Ministero dell'Economia e delle Finanze ha pubblicato una circolare esplicativa in merito all'applicazione del D.Lgs. 209/2023 che recepisce la Direttiva UE 2022/2523 (Pillar Two / GloBE). Il documento chiarisce il perimetro soggettivo delle imprese rientranti nella Global Minimum Tax italiana e le modalità di calcolo dell'Imposta Minima Integrativa (IIR) e dell'Imposta Minima Suppletiva (UTPR).',
    category: 'P2',
    country: 'IT',
    source_name: 'MEF - D.Lgs. 209/2023 Pillar Two',
    source_url: 'https://www.mef.gov.it/',
    normative_references: [
      { tipo: 'legge', numero: 'D.Lgs. 209/2023', fonte: 'MEF', url: 'https://www.normattiva.it/' },
      { tipo: 'direttiva', numero: '2022/2523/UE', fonte: 'EU', url: 'https://eur-lex.europa.eu/' },
    ],
    status: 'PUBLISHED',
    url_hash: 'demo002hash',
    published_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

// ── Repository principale ────────────────────────────────────────────────────

export async function getPublishedNews(filters: NewsFilters = {}): Promise<NewsFeedResult> {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
    || (typeof window !== 'undefined' && (window as Record<string, unknown>).__SUPABASE_URL as string)
    || null;

  if (supabaseUrl) {
    return getFromSupabase(filters, supabaseUrl);
  }

  return getFromDemo(filters);
}

// ── Supabase path ────────────────────────────────────────────────────────────

async function getFromSupabase(filters: NewsFilters, supabaseUrl: string): Promise<NewsFeedResult> {
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
  const page    = filters.page  || 1;
  const limit   = filters.limit || 20;
  const from    = (page - 1) * limit;
  const to      = from + limit - 1;

  let url = `${supabaseUrl}/rest/v1/news_items?status=eq.PUBLISHED&order=published_at.desc`;
  if (filters.category) url += `&category=eq.${filters.category}`;
  if (filters.country)  url += `&country=eq.${filters.country}`;
  if (filters.from)     url += `&published_at=gte.${filters.from}`;
  if (filters.to)       url += `&published_at=lte.${filters.to}`;
  if (filters.q)        url += `&title=ilike.*${encodeURIComponent(filters.q)}*`;

  const headers = {
    'apikey': anonKey,
    'Authorization': `Bearer ${anonKey}`,
    'Range': `${from}-${to}`,
    'Range-Unit': 'items',
    'Prefer': 'count=exact',
  };

  const [itemsRes, countRes] = await Promise.all([
    fetch(url, { headers }),
    fetch(`${supabaseUrl}/rest/v1/news_items?status=eq.PUBLISHED&select=country,category`, { headers }),
  ]);

  const items: NewsItem[] = itemsRes.ok ? await itemsRes.json() : [];
  const allItems: { country?: string; category: NewsCategory }[] = countRes.ok ? await countRes.json() : [];

  const total = parseInt(itemsRes.headers.get('Content-Range')?.split('/')[1] || '0', 10);

  const availableCountries = [...new Set(allItems.map(i => i.country).filter(Boolean))] as string[];
  const availableCategories = [...new Set(allItems.map(i => i.category))] as NewsCategory[];

  return {
    items,
    total,
    availableCategories,
    availableCountries,
    page,
    limit,
    hasMore: to < total - 1,
  };
}

// ── Demo path ────────────────────────────────────────────────────────────────

async function getFromDemo(filters: NewsFilters): Promise<NewsFeedResult> {
  let items = [...DEMO_NEWS];

  if (filters.category) items = items.filter(i => i.category === filters.category);
  if (filters.country)  items = items.filter(i => i.country  === filters.country);
  if (filters.q) {
    const q = filters.q.toLowerCase();
    items = items.filter(i =>
      i.title.toLowerCase().includes(q) ||
      i.summary.toLowerCase().includes(q)
    );
  }

  const page  = filters.page  || 1;
  const limit = filters.limit || 20;
  const total = items.length;
  const start = (page - 1) * limit;
  const paged = items.slice(start, start + limit);

  return {
    items: paged,
    total,
    availableCategories: ['TP', 'P2', 'VAT', 'AA'],
    availableCountries:  ['IT', 'INT', 'EU', 'US', 'UK'],
    page,
    limit,
    hasMore: start + limit < total,
  };
}
