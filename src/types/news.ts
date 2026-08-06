/**
 * Types: Attualità Fiscale — TP Box
 * Sincronizzati con schema Supabase (news_sources, news_items)
 */

export type NewsCategory = 'TP' | 'VAT' | 'P2' | 'AA';

export type NewsStatus = 'DRAFT' | 'IN_REVIEW' | 'PUBLISHED' | 'ARCHIVED';

export type WatchType = 'RSS' | 'ATOM' | 'HTML_WATCH';

export type HealthStatus = 'OK' | 'WARN' | 'ERROR' | 'DISABLED';

export interface NormativoReference {
  tipo: 'articolo' | 'comma' | 'legge' | 'direttiva' | 'regolamento' | 'provvedimento';
  numero: string;
  fonte: string;
  data?: string;
  url?: string;
}

export interface NewsSource {
  id: string;
  name: string;
  category: NewsCategory;
  country: string;
  feed_url: string | null;
  watch_type: WatchType;
  css_selector: string | null;
  enabled: boolean;
  last_fetched_at: string | null;
  health_status: HealthStatus;
  fail_count: number;
  created_at: string;
}

export interface NewsItem {
  id: string;
  title: string;
  summary: string;
  content_markdown?: string;
  category: NewsCategory;
  country?: string;
  source_name: string;
  source_url: string;
  pdf_url?: string;
  pdf_local_path?: string;
  normative_references: NormativoReference[];
  status: NewsStatus;
  url_hash: string;
  reviewed_by?: string;
  published_at?: string;
  created_at: string;
  updated_at: string;
}

/** Filtri per il feed pubblico */
export interface NewsFilters {
  category?: NewsCategory;
  country?: string;        // ISO 3166-1 alpha-2
  from?: string;           // ISO date YYYY-MM-DD
  to?: string;
  q?: string;              // full-text search
  page?: number;
  limit?: number;
}

/** Risultato paginato */
export interface NewsFeedResult {
  items: NewsItem[];
  total: number;
  availableCategories: NewsCategory[];
  availableCountries: string[];
  page: number;
  limit: number;
  hasMore: boolean;
}

/** Label leggibili per UI */
export const CATEGORY_LABELS: Record<NewsCategory, string> = {
  TP:  'Transfer Pricing',
  VAT: 'IVA / VAT',
  P2:  'Pillar Two / GloBE',
  AA:  'Anti-Avoidance',
};

export const CATEGORY_COLORS: Record<NewsCategory, string> = {
  TP:  'blue',
  VAT: 'green',
  P2:  'purple',
  AA:  'orange',
};

export const COUNTRY_LABELS: Record<string, string> = {
  IT:  'Italia',
  EU:  'Unione Europea',
  US:  'Stati Uniti',
  UK:  'Regno Unito',
  CA:  'Canada',
  AU:  'Australia',
  IN:  'India',
  INT: 'Internazionale',
  DE:  'Germania',
  FR:  'Francia',
};
