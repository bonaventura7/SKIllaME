/**
 * Tipi per il sistema di notizie TP Box
 * Modello editoriale: RegFollower-style
 * Categorie: TP | VAT | P2 | AA
 * Filtri: categoria + paese
 */

export type NewsCategory = 'TP' | 'VAT' | 'P2' | 'AA';
export type NewsStatus   = 'DRAFT' | 'IN_REVIEW' | 'PUBLISHED';

export interface NormativoRef {
  tipo:   string;  // 'articolo' | 'direttiva' | 'legge' | 'circolare'
  numero: string;
  fonte:  string;
  data?:  string;
  url?:   string;
}

export interface NewsItem {
  id:                    string;
  title:                 string;
  summary:               string;
  body?:                 string;          // corpo articolo completo (markdown)
  category:              NewsCategory;
  country:               string;          // ISO 2 o 'INT'
  source_name:           string;
  source_url:            string;          // URL articolo originale
  pdf_url?:              string;          // link diretto PDF ufficiale
  url_hash:              string;
  normative_references?: NormativoRef[];
  status:                NewsStatus;
  published_at?:         string;
  pub_date?:             string;
  created_at:            string;
  updated_at:            string;
}

export interface NewsFilters {
  category?: NewsCategory;
  country?:  string;
  q?:        string;
  from?:     string;
  to?:       string;
  page?:     number;
  limit?:    number;
}

export interface NewsFeedResult {
  items:               NewsItem[];
  total:               number;
  availableCategories: NewsCategory[];
  availableCountries:  string[];
  page:                number;
  limit:               number;
  hasMore:             boolean;
}

// ── Mappe UI ────────────────────────────────────────────────────────────────

export const CATEGORY_LABELS: Record<NewsCategory, string> = {
  TP:  'Transfer Pricing',
  VAT: 'IVA / VAT',
  P2:  'Pillar Two',
  AA:  'Anti Avoidance',
};

export const CATEGORY_COLORS: Record<NewsCategory, { bg: string; text: string; border: string }> = {
  TP:  { bg: 'bg-blue-50',   text: 'text-blue-800',   border: 'border-blue-200'  },
  VAT: { bg: 'bg-amber-50',  text: 'text-amber-800',  border: 'border-amber-200' },
  P2:  { bg: 'bg-purple-50', text: 'text-purple-800', border: 'border-purple-200'},
  AA:  { bg: 'bg-red-50',    text: 'text-red-800',    border: 'border-red-200'   },
};

export const COUNTRY_FLAGS: Record<string, string> = {
  IT:  '🇮🇹',
  EU:  '🇪🇺',
  INT: '🌐',
  US:  '🇺🇸',
  UK:  '🇬🇧',
  IN:  '🇮🇳',
  DE:  '🇩🇪',
  FR:  '🇫🇷',
  JP:  '🇯🇵',
  AU:  '🇦🇺',
};

export const COUNTRY_NAMES: Record<string, string> = {
  IT:  'Italia',
  EU:  'Unione Europea',
  INT: 'Internazionale',
  US:  'Stati Uniti',
  UK:  'Regno Unito',
  IN:  'India',
  DE:  'Germania',
  FR:  'Francia',
  JP:  'Giappone',
  AU:  'Australia',
};
