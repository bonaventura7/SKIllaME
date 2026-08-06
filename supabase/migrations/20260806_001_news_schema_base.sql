-- ============================================================
-- MIGRATION 001: Schema base Attualità fiscale
-- Approccio B: 2 tabelle minimali + workflow editoriale
-- Progetto: TP Box | Data: 2026-08-06
-- ============================================================
-- Vedi: apply_migration su Supabase TP Box (igtthymjeujkgfpmgoqj)
-- Già applicata via MCP Supabase in data 2026-08-06
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE public.news_sources (
  id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  name            TEXT        NOT NULL UNIQUE,
  category        TEXT        NOT NULL CHECK (category IN ('TP','VAT','P2','AA')),
  country         TEXT,
  feed_url        TEXT,
  watch_type      TEXT        NOT NULL DEFAULT 'RSS' CHECK (watch_type IN ('RSS','ATOM','HTML_WATCH')),
  css_selector    TEXT,
  enabled         BOOLEAN     NOT NULL DEFAULT true,
  last_fetched_at TIMESTAMPTZ,
  health_status   TEXT        DEFAULT 'OK' CHECK (health_status IN ('OK','WARN','ERROR','DISABLED')),
  fail_count      INTEGER     NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.news_items (
  id                   UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  title                TEXT        NOT NULL,
  summary              TEXT        NOT NULL,
  content_markdown     TEXT,
  category             TEXT        NOT NULL CHECK (category IN ('TP','VAT','P2','AA')),
  country              TEXT,
  source_name          TEXT        NOT NULL REFERENCES public.news_sources(name) ON UPDATE CASCADE,
  source_url           TEXT        NOT NULL,
  pdf_url              TEXT,
  pdf_local_path       TEXT,
  normative_references JSONB       NOT NULL DEFAULT '[]'::jsonb,
  status               TEXT        NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT','IN_REVIEW','PUBLISHED','ARCHIVED')),
  url_hash             TEXT        GENERATED ALWAYS AS (md5(source_url)) STORED,
  reviewed_by          TEXT,
  published_at         TIMESTAMPTZ,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_news_items_status       ON public.news_items(status);
CREATE INDEX idx_news_items_category_pub ON public.news_items(category) WHERE status = 'PUBLISHED';
CREATE INDEX idx_news_items_country_pub  ON public.news_items(country)  WHERE status = 'PUBLISHED';
CREATE INDEX idx_news_items_published_at ON public.news_items(published_at DESC) WHERE status = 'PUBLISHED';
CREATE UNIQUE INDEX idx_news_items_url_hash ON public.news_items(url_hash);
CREATE INDEX idx_news_items_normrefs     ON public.news_items USING GIN (normative_references);

CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$;

CREATE TRIGGER trg_news_items_updated_at
  BEFORE UPDATE ON public.news_items
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE OR REPLACE FUNCTION public.enforce_published_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.status = 'PUBLISHED' AND NEW.published_at IS NULL THEN
    NEW.published_at = NOW();
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_news_items_published_at
  BEFORE INSERT OR UPDATE ON public.news_items
  FOR EACH ROW EXECUTE FUNCTION public.enforce_published_at();

ALTER TABLE public.news_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.news_items   ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public_read_published"       ON public.news_items   FOR SELECT USING (status = 'PUBLISHED');
CREATE POLICY "service_role_full"           ON public.news_items   FOR ALL USING (auth.role() = 'service_role') WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "authenticated_full"         ON public.news_items   FOR ALL USING (auth.role() = 'authenticated') WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "sources_public_read"         ON public.news_sources FOR SELECT USING (enabled = true);
CREATE POLICY "sources_service_role_full"   ON public.news_sources FOR ALL USING (auth.role() = 'service_role') WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "sources_authenticated_full" ON public.news_sources FOR ALL USING (auth.role() = 'authenticated') WITH CHECK (auth.role() = 'authenticated');
