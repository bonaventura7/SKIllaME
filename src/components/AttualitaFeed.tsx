'use client';

/**
 * AttualitaFeed — Sezione Attualità TP Box
 * Modello editoriale: RegFollower-style
 *
 * Layout:
 *   [Sidebar filtri] | [Lista articoli card]
 *
 * Per ogni articolo:
 *   - Badge categoria (TP | VAT | P2 | AA) + flag paese
 *   - Titolo + sommario
 *   - Riferimenti normativi collassabili
 *   - 🔗 Link fonte originale + 📄 PDF scaricabile
 *   - Data pubblicazione
 *
 * Filtri:
 *   - Categoria (TP | VAT | P2 | AA | Tutti)
 *   - Paese (IT | EU | INT | US | UK | IN | Tutti)
 *   - Ricerca testuale
 *
 * Archivio/Biblioteca:
 *   - Sezione separata con tutte le fonti PDF organizzate per categoria
 */

import React, { useState, useEffect, useCallback } from 'react';
import type { NewsItem, NewsCategory, NewsFilters } from '../types/news';
import {
  CATEGORY_LABELS,
  CATEGORY_COLORS,
  COUNTRY_FLAGS,
  COUNTRY_NAMES,
} from '../types/news';
import { getPublishedNews } from '../lib/news.repository';

// ── Tipi locali ──────────────────────────────────────────────────────────────

type ViewMode = 'feed' | 'biblioteca';

// ── Componente Badge Categoria ───────────────────────────────────────────────

function CategoryBadge({ category }: { category: NewsCategory }) {
  const colors = CATEGORY_COLORS[category];
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
        colors.bg} ${colors.text} ${colors.border}`}
    >
      {CATEGORY_LABELS[category]}
    </span>
  );
}

// ── Componente Flag Paese ────────────────────────────────────────────────────

function CountryBadge({ country }: { country: string }) {
  const flag = COUNTRY_FLAGS[country] || '🌐';
  const name = COUNTRY_NAMES[country] || country;
  return (
    <span className="inline-flex items-center gap-1 text-xs text-gray-500 font-medium">
      <span>{flag}</span>
      <span>{name}</span>
    </span>
  );
}

// ── Componente Card Articolo (stile RegFollower) ─────────────────────────────

function NewsCard({ item }: { item: NewsItem }) {
  const [showRefs, setShowRefs] = useState(false);

  const publishedDate = item.published_at
    ? new Date(item.published_at).toLocaleDateString('it-IT', {
        day: '2-digit', month: 'long', year: 'numeric',
      })
    : null;

  return (
    <article className="bg-white border border-gray-100 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden">
      {/* Header card */}
      <div className="p-5 pb-3">
        {/* Badge riga */}
        <div className="flex items-center gap-2 mb-3 flex-wrap">
          <CategoryBadge category={item.category} />
          <CountryBadge country={item.country} />
          {publishedDate && (
            <span className="text-xs text-gray-400 ml-auto">{publishedDate}</span>
          )}
        </div>

        {/* Titolo */}
        <h2 className="text-base font-bold text-gray-900 leading-snug mb-2 hover:text-blue-700 transition-colors">
          <a href={item.source_url} target="_blank" rel="noopener noreferrer">
            {item.title}
          </a>
        </h2>

        {/* Fonte */}
        <p className="text-xs text-gray-500 mb-3 font-medium">
          Fonte: <span className="text-gray-700">{item.source_name}</span>
        </p>

        {/* Sommario — stile "RF Report" */}
        <div className="text-sm text-gray-700 leading-relaxed">
          <span className="font-semibold text-gray-900">RF Report</span>... {item.summary}
        </div>
      </div>

      {/* Footer card */}
      <div className="px-5 py-3 bg-gray-50 border-t border-gray-100 flex items-center gap-3 flex-wrap">
        {/* Link fonte originale */}
        <a
          href={item.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-700 hover:text-blue-900 transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          Leggi fonte originale
        </a>

        {/* PDF scaricabile — REGOLA D'ORO: sempre visibile se disponibile */}
        {item.pdf_url && (
          <a
            href={item.pdf_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-red-700 hover:text-red-900 transition-colors"
          >
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            📄 Scarica PDF ufficiale
          </a>
        )}

        {/* Toggle normativa */}
        {item.normative_references && item.normative_references.length > 0 && (
          <button
            onClick={() => setShowRefs(!showRefs)}
            className="inline-flex items-center gap-1 text-xs text-gray-500 hover:text-gray-800 transition-colors ml-auto"
          >
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            {showRefs ? 'Nascondi normativa' : `Normativa (${item.normative_references.length})`}
          </button>
        )}
      </div>

      {/* Normativa collassabile */}
      {showRefs && item.normative_references && (
        <div className="px-5 py-3 bg-blue-50 border-t border-blue-100">
          <p className="text-xs font-semibold text-blue-900 mb-2">Riferimenti normativi applicabili:</p>
          <ul className="space-y-1">
            {item.normative_references.map((ref, idx) => (
              <li key={idx} className="text-xs text-blue-800 flex items-start gap-1.5">
                <span className="text-blue-400 mt-0.5">▸</span>
                {ref.url ? (
                  <a href={ref.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
                    <span className="capitalize">{ref.tipo}</span> {ref.numero}{' '}
                    <span className="text-blue-500">({ref.fonte})</span>
                  </a>
                ) : (
                  <span>
                    <span className="capitalize">{ref.tipo}</span> {ref.numero}{' '}
                    <span className="text-blue-500">({ref.fonte})</span>
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </article>
  );
}

// ── Componente Biblioteca/Archivio ───────────────────────────────────────────

function BibliotecaView({ items }: { items: NewsItem[] }) {
  const categories: NewsCategory[] = ['TP', 'P2', 'VAT', 'AA'];
  const itemsWithPdf = items.filter(i => i.pdf_url);

  return (
    <div className="space-y-8">
      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <p className="text-sm text-amber-800">
          <strong>📚 Biblioteca Fonti Ufficiali</strong> — {itemsWithPdf.length} documenti primari disponibili.
          Tutte le fonti linkano direttamente ai siti istituzionali originali.
        </p>
      </div>

      {categories.map(cat => {
        const catItems = itemsWithPdf.filter(i => i.category === cat);
        if (catItems.length === 0) return null;
        const colors = CATEGORY_COLORS[cat];
        return (
          <section key={cat}>
            <div className={`flex items-center gap-2 mb-3 pb-2 border-b ${colors.border}`}>
              <CategoryBadge category={cat} />
              <span className="text-sm text-gray-500">{catItems.length} documenti</span>
            </div>
            <ul className="space-y-2">
              {catItems.map(item => (
                <li key={item.id} className="flex items-start gap-3 p-3 rounded-lg bg-white border border-gray-100 hover:border-gray-200 transition-colors">
                  <svg className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{item.title}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <CountryBadge country={item.country} />
                      <span className="text-xs text-gray-400">•</span>
                      <span className="text-xs text-gray-500">{item.source_name}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <a href={item.source_url} target="_blank" rel="noopener noreferrer"
                      className="text-xs text-blue-600 hover:text-blue-800 font-medium">Fonte</a>
                    {item.pdf_url && (
                      <a href={item.pdf_url} target="_blank" rel="noopener noreferrer"
                        className="text-xs text-red-600 hover:text-red-800 font-medium">PDF</a>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </div>
  );
}

// ── Componente principale AttualitaFeed ──────────────────────────────────────

export function AttualitaFeed() {
  const [items,               setItems]               = useState<NewsItem[]>([]);
  const [total,               setTotal]               = useState(0);
  const [availableCountries,  setAvailableCountries]  = useState<string[]>([]);
  const [loading,             setLoading]             = useState(true);
  const [error,               setError]               = useState<string | null>(null);
  const [viewMode,            setViewMode]            = useState<ViewMode>('feed');

  // Filtri attivi
  const [selectedCategory, setSelectedCategory] = useState<NewsCategory | ''>('');
  const [selectedCountry,  setSelectedCountry]  = useState<string>('');
  const [searchQuery,      setSearchQuery]      = useState<string>('');
  const [debouncedQuery,   setDebouncedQuery]   = useState<string>('');

  // Debounce ricerca
  useEffect(() => {
    const t = setTimeout(() => setDebouncedQuery(searchQuery), 400);
    return () => clearTimeout(t);
  }, [searchQuery]);

  const loadNews = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const filters: NewsFilters = {};
      if (selectedCategory) filters.category = selectedCategory as NewsCategory;
      if (selectedCountry)  filters.country  = selectedCountry;
      if (debouncedQuery)   filters.q        = debouncedQuery;

      const result = await getPublishedNews(filters);
      setItems(result.items);
      setTotal(result.total);
      setAvailableCountries(result.availableCountries);
    } catch (e) {
      setError('Impossibile caricare le notizie. Riprova tra qualche istante.');
      console.error('[AttualitaFeed] loadNews error:', e);
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, selectedCountry, debouncedQuery]);

  useEffect(() => { loadNews(); }, [loadNews]);

  const categories: NewsCategory[] = ['TP', 'P2', 'VAT', 'AA'];
  const activeFiltersCount = [selectedCategory, selectedCountry, debouncedQuery].filter(Boolean).length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header sezione */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Attualità Fiscale</h1>
              <p className="text-sm text-gray-500 mt-1">
                Aggiornamenti in italiano da fonti primarie istituzionali · {total} articoli
              </p>
            </div>
            {/* Toggle Feed / Biblioteca */}
            <div className="flex items-center bg-gray-100 rounded-lg p-1 gap-1">
              <button
                onClick={() => setViewMode('feed')}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  viewMode === 'feed'
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                📰 Feed
              </button>
              <button
                onClick={() => setViewMode('biblioteca')}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  viewMode === 'biblioteca'
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                📚 Biblioteca
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex gap-6 flex-col lg:flex-row">

          {/* ── Sidebar Filtri ── */}
          <aside className="w-full lg:w-64 flex-shrink-0">
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 sticky top-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-bold text-gray-900">Filtri</h2>
                {activeFiltersCount > 0 && (
                  <button
                    onClick={() => {
                      setSelectedCategory('');
                      setSelectedCountry('');
                      setSearchQuery('');
                    }}
                    className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Azzera ({activeFiltersCount})
                  </button>
                )}
              </div>

              {/* Ricerca */}
              <div className="mb-4">
                <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1.5 block">Ricerca</label>
                <input
                  type="text"
                  placeholder="Cerca articoli..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Filtro Categoria */}
              <div className="mb-4">
                <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2 block">Categoria</label>
                <div className="space-y-1">
                  <button
                    onClick={() => setSelectedCategory('')}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                      selectedCategory === ''
                        ? 'bg-gray-900 text-white font-medium'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    Tutte le categorie
                  </button>
                  {categories.map(cat => {
                    const colors = CATEGORY_COLORS[cat];
                    return (
                      <button
                        key={cat}
                        onClick={() => setSelectedCategory(selectedCategory === cat ? '' : cat)}
                        className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center gap-2 ${
                          selectedCategory === cat
                            ? `${colors.bg} ${colors.text} font-semibold border ${colors.border}`
                            : 'text-gray-600 hover:bg-gray-50'
                        }`}
                      >
                        {CATEGORY_LABELS[cat]}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Filtro Paese */}
              {availableCountries.length > 0 && (
                <div>
                  <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2 block">Paese</label>
                  <div className="space-y-1">
                    <button
                      onClick={() => setSelectedCountry('')}
                      className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                        selectedCountry === ''
                          ? 'bg-gray-900 text-white font-medium'
                          : 'text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      Tutti i paesi
                    </button>
                    {availableCountries.map(country => (
                      <button
                        key={country}
                        onClick={() => setSelectedCountry(selectedCountry === country ? '' : country)}
                        className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                          selectedCountry === country
                            ? 'bg-gray-900 text-white font-medium'
                            : 'text-gray-600 hover:bg-gray-50'
                        }`}
                      >
                        {COUNTRY_FLAGS[country] || '🌐'} {COUNTRY_NAMES[country] || country}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </aside>

          {/* ── Contenuto principale ── */}
          <main className="flex-1 min-w-0">

            {/* Stato: loading */}
            {loading && (
              <div className="space-y-4">
                {[1, 2, 3].map(n => (
                  <div key={n} className="bg-white rounded-xl border border-gray-100 p-5 animate-pulse">
                    <div className="flex gap-2 mb-3">
                      <div className="h-5 w-24 bg-gray-200 rounded-full" />
                      <div className="h-5 w-16 bg-gray-100 rounded-full" />
                    </div>
                    <div className="h-5 bg-gray-200 rounded mb-2 w-3/4" />
                    <div className="h-4 bg-gray-100 rounded mb-4 w-1/3" />
                    <div className="space-y-2">
                      <div className="h-3 bg-gray-100 rounded" />
                      <div className="h-3 bg-gray-100 rounded w-5/6" />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Stato: errore */}
            {!loading && error && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
                <p className="text-red-700 text-sm">{error}</p>
                <button
                  onClick={loadNews}
                  className="mt-3 text-sm text-red-600 hover:text-red-800 font-medium underline"
                >
                  Riprova
                </button>
              </div>
            )}

            {/* Stato: vuoto */}
            {!loading && !error && items.length === 0 && (
              <div className="bg-white border border-gray-100 rounded-xl p-12 text-center">
                <div className="text-4xl mb-3">📭</div>
                <h3 className="text-gray-900 font-semibold mb-1">Nessun articolo trovato</h3>
                <p className="text-gray-500 text-sm">
                  Prova a modificare i filtri o la ricerca.
                </p>
              </div>
            )}

            {/* Vista Feed */}
            {!loading && !error && items.length > 0 && viewMode === 'feed' && (
              <div className="space-y-4">
                {items.map(item => (
                  <NewsCard key={item.id} item={item} />
                ))}
              </div>
            )}

            {/* Vista Biblioteca */}
            {!loading && !error && viewMode === 'biblioteca' && (
              <BibliotecaView items={items} />
            )}
          </main>
        </div>
      </div>
    </div>
  );
}

export default AttualitaFeed;
