/**
 * News Repository — Supabase-or-Demo pattern
 *
 * Se NEXT_PUBLIC_SUPABASE_URL è definito → legge da Supabase (TP Box)
 * Altrimenti → fallback a DEMO_NEWS (sviluppo locale)
 *
 * Modello editoriale: RegFollower-style
 *   ✅ Fonte primaria istituzionale sempre citata
 *   ✅ Link PDF ufficiale quando disponibile
 *   ✅ Riferimenti normativi inline (TUIR, OCSE, Direttive UE)
 *   ✅ Solo articoli PUBLISHED esposti
 *   ✅ Filtri: categoria (TP|VAT|P2|AA) + paese
 */

import type { NewsFilters, NewsFeedResult, NewsItem, NewsCategory } from '../types/news';

// ── Demo data (fallback dev locale) ─────────────────────────────────────────
// 5 articoli realistici che coprono tutte e 4 le categorie

const DEMO_NEWS: NewsItem[] = [
  {
    id: 'demo-001',
    title: 'India: record storico di APA nel FY 2025-26 — 220 accordi firmati, prime BAPA con Francia e Svezia',
    summary:
      'Il Central Board of Direct Taxes (CBDT) indiano ha pubblicato il Rapporto Annuale APA FY 2025-26, documentando il massimo storico di 220 Advance Pricing Agreement firmati in un anno, di cui 84 bilaterali (BAPA). Il programma ha raggiunto 1.035 APA cumulativi. Significative le riforme introdotte dall\'Income Tax Act 2025 e dall\'Income Tax Rules 2026: fee standardizzata a INR 2 milioni, nuovi moduli (Forms 50-54), e safe harbor unificato al 15,5% per i servizi IT. Il periodo mediano di risoluzione è di 36 mesi per UAPA e 38 per BAPA. India e Giappone hanno ricevuto riconoscimento OCSE 2024 per la cooperazione MAP.',
    category: 'TP',
    country: 'IN',
    source_name: 'Income Tax Department India — Annual APA Report FY 2025-26',
    source_url: 'https://www.incometaxindia.gov.in/pages/international-taxation/advance-pricing-agreement.aspx',
    pdf_url: 'https://www.incometaxindia.gov.in/documents/d/guest/apa-report2025-26-2-pdf',
    normative_references: [
      { tipo: 'legge', numero: 'Income Tax Act 2025 — Section 168', fonte: 'CBDT India', url: 'https://www.incometaxindia.gov.in/' },
      { tipo: 'regola', numero: 'Income Tax Rules 2026 — Rules 103-120', fonte: 'CBDT India', url: 'https://www.incometaxindia.gov.in/' },
      { tipo: 'linee guida', numero: 'TPG 2022 Cap. I-IV', fonte: 'OCSE', url: 'https://www.oecd.org/tax/transfer-pricing/oecd-transfer-pricing-guidelines.htm' },
      { tipo: 'regola', numero: 'Rule 89 — Safe Harbor IT Services 15,5%', fonte: 'CBDT India', url: 'https://www.incometaxindia.gov.in/' },
    ],
    status: 'PUBLISHED',
    url_hash: 'cbdt-apa-report-2025-26',
    published_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 'demo-002',
    title: 'OCSE: aggiornamento Linee Guida Transfer Pricing 2025 — Capitolo I e VI su intangibili',
    summary:
      'L\'OCSE ha rilasciato un aggiornamento sostanziale alle Transfer Pricing Guidelines (TPG 2025) con modifiche al Capitolo I (principio di libera concorrenza) e al Capitolo VI (proprietà intellettuale e intangibili). Le nuove disposizioni rafforzano i requisiti documentali per operazioni infragruppo ad alto valore aggiunto e introducono chiarimenti metodologici sui comparabili geografici. Particolare attenzione è dedicata alle transazioni digitali e ai modelli di business dematerializzati, in linea con le conclusioni BEPS Action 8-10. Le modifiche sono rilevanti per i contribuenti italiani ai sensi dell\'art. 110, comma 7 TUIR e del Provvedimento AdE 21/11/2023.',
    category: 'TP',
    country: 'INT',
    source_name: 'OECD — Transfer Pricing Guidelines 2025',
    source_url: 'https://www.oecd.org/tax/transfer-pricing/oecd-transfer-pricing-guidelines.htm',
    pdf_url: 'https://www.oecd.org/tax/transfer-pricing/oecd-transfer-pricing-guidelines-for-multinational-enterprises-and-tax-administrations-20769717.htm',
    normative_references: [
      { tipo: 'articolo', numero: '110, comma 7', fonte: 'TUIR', url: 'https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.del.presidente.della.repubblica:1986-12-22;917' },
      { tipo: 'provvedimento', numero: '21/11/2023', fonte: 'Agenzia delle Entrate', url: 'https://www.agenziaentrate.gov.it/' },
      { tipo: 'linee guida', numero: 'BEPS Action 8-10', fonte: 'OCSE', url: 'https://www.oecd.org/tax/beps/' },
    ],
    status: 'PUBLISHED',
    url_hash: 'oecd-tpg-2025-update',
    published_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 'demo-003',
    title: 'Pillar Two: MEF pubblica circolare applicativa al D.Lgs. 209/2023 — IIR e UTPR per gruppi multinazionali',
    summary:
      'Il Ministero dell\'Economia e delle Finanze ha pubblicato una circolare esplicativa sull\'applicazione del D.Lgs. 209/2023, che recepisce la Direttiva UE 2022/2523 (Global Minimum Tax / Pillar Two). La circolare chiarisce il perimetro soggettivo — gruppi con ricavi consolidati ≥ 750 milioni EUR — e le modalità di calcolo dell\'Imposta Minima Integrativa (IIR), dell\'Imposta Minima Suppletiva (UTPR) e dell\'Imposta Minima Nazionale (QDMTT). Vengono altresì illustrate le regole di esclusione de minimis (ricavi < 10 milioni EUR e utile < 1 milione EUR per giurisdizione) e il trattamento delle entità a flusso diretto (flow-through entities).',
    category: 'P2',
    country: 'IT',
    source_name: 'MEF — Circolare D.Lgs. 209/2023 Pillar Two',
    source_url: 'https://www.mef.gov.it/en/focus/Global-Minimum-Tax/',
    pdf_url: 'https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2023-12-27;209',
    normative_references: [
      { tipo: 'decreto', numero: 'D.Lgs. 209/2023', fonte: 'MEF', url: 'https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2023-12-27;209' },
      { tipo: 'direttiva', numero: '2022/2523/UE', fonte: 'Commissione EU', url: 'https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32022L2523' },
      { tipo: 'regole', numero: 'GloBE Model Rules 2021', fonte: 'OCSE', url: 'https://www.oecd.org/tax/beps/tax-challenges-arising-from-the-digitalisation-of-the-economy-global-anti-base-erosion-model-rules-pillar-two.htm' },
    ],
    status: 'PUBLISHED',
    url_hash: 'mef-circolare-dlgs-209-2023-p2',
    published_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 'demo-004',
    title: 'UE: nuove regole IVA sull\'economia digitale — pacchetto VAT in the Digital Age (ViDA) in vigore',
    summary:
      'La Direttiva UE 2025/516 (VAT in the Digital Age — ViDA) è entrata in vigore introducendo l\'obbligo di fatturazione elettronica cross-border e il sistema di dichiarazione digitale in tempo reale per le operazioni B2B intra-UE. Le piattaforme digitali diventano responsabili della riscossione IVA per i servizi di trasporto e alloggio breve termine (deemed supplier). Il regime OSS (One Stop Shop) è esteso anche alle cessioni di beni B2C domestiche. Per l\'Italia, le modifiche si intersecano con il sistema SDI già esistente e richiederanno adeguamenti normativi al DPR 633/1972.',
    category: 'VAT',
    country: 'EU',
    source_name: 'Commissione Europea — VAT in the Digital Age (ViDA)',
    source_url: 'https://taxation-customs.ec.europa.eu/taxation/value-added-tax/vat-digital-age_en',
    pdf_url: 'https://eur-lex.europa.eu/legal-content/IT/TXT/PDF/?uri=CELEX:32025L0516',
    normative_references: [
      { tipo: 'direttiva', numero: '2025/516/UE — ViDA', fonte: 'Commissione UE', url: 'https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32025L0516' },
      { tipo: 'direttiva', numero: '2006/112/CE — Sistema comune IVA', fonte: 'Consiglio UE', url: 'https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32006L0112' },
      { tipo: 'decreto', numero: 'DPR 633/1972', fonte: 'Italia', url: 'https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.del.presidente.della.repubblica:1972-10-26;633' },
    ],
    status: 'PUBLISHED',
    url_hash: 'eu-vida-vat-digital-age-2025',
    published_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 'demo-005',
    title: 'AdE: Circolare 10/E/2025 — chiarimenti sull\'abuso del diritto ex art. 10-bis L. 212/2000 e operazioni infragruppo',
    summary:
      'L\'Agenzia delle Entrate ha pubblicato la Circolare 10/E del 15 marzo 2025 recante chiarimenti in materia di abuso del diritto tributario ai sensi dell\'art. 10-bis della Legge 212/2000 (Statuto del Contribuente), con specifico riferimento alle operazioni infragruppo e alle ristrutturazioni aziendali cross-border. La circolare precisa i criteri per valutare la sostanza economica delle operazioni e l\'assenza di vantaggi fiscali indebiti, anche alla luce della clausola anti-abuso generale prevista dall\'ATAD (Direttiva UE 2016/1164). Vengono forniti esempi pratici relativi a fusioni, scissioni e conferimenti di partecipazioni con elementi di internazionalità.',
    category: 'AA',
    country: 'IT',
    source_name: 'Agenzia delle Entrate — Circolare 10/E/2025',
    source_url: 'https://www.agenziaentrate.gov.it/portale/web/guest/normativa-e-prassi/circolari',
    pdf_url: 'https://www.agenziaentrate.gov.it/portale/documents/20143/233439/Circolare+10E+2025.pdf',
    normative_references: [
      { tipo: 'articolo', numero: '10-bis', fonte: 'L. 212/2000 — Statuto Contribuente', url: 'https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2000-07-27;212' },
      { tipo: 'direttiva', numero: '2016/1164/UE — ATAD', fonte: 'Consiglio UE', url: 'https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32016L1164' },
      { tipo: 'azione', numero: 'BEPS Action 6 — Abuso Trattati', fonte: 'OCSE', url: 'https://www.oecd.org/tax/beps/beps-actions/action6/' },
    ],
    status: 'PUBLISHED',
    url_hash: 'ade-circolare-10e-2025-abuso-diritto',
    published_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
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
    'apikey':          anonKey,
    'Authorization':   `Bearer ${anonKey}`,
    'Range':           `${from}-${to}`,
    'Range-Unit':      'items',
    'Prefer':          'count=exact',
  };

  const [itemsRes, metaRes] = await Promise.all([
    fetch(url, { headers }),
    fetch(`${supabaseUrl}/rest/v1/news_items?status=eq.PUBLISHED&select=country,category`, { headers }),
  ]);

  const items:    NewsItem[]                                  = itemsRes.ok ? await itemsRes.json() : [];
  const allItems: { country?: string; category: NewsCategory }[] = metaRes.ok  ? await metaRes.json()  : [];

  const total = parseInt(itemsRes.headers.get('Content-Range')?.split('/')[1] || '0', 10);

  const availableCountries   = [...new Set(allItems.map(i => i.country).filter(Boolean))]  as string[];
  const availableCategories  = [...new Set(allItems.map(i => i.category))]                  as NewsCategory[];

  return { items, total, availableCategories, availableCountries, page, limit, hasMore: to < total - 1 };
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

  // Calcola metadati disponibili dall'intero dataset (non filtrato)
  const allCountries   = [...new Set(DEMO_NEWS.map(i => i.country))]   as string[];
  const allCategories  = [...new Set(DEMO_NEWS.map(i => i.category))]  as NewsCategory[];

  return {
    items:               paged,
    total,
    availableCategories: allCategories,
    availableCountries:  allCountries,
    page,
    limit,
    hasMore:             start + limit < total,
  };
}
