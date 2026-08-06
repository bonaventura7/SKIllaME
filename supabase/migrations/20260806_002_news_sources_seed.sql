-- ============================================================
-- MIGRATION 002: Seed whitelist fonti primarie istituzionali
-- REGOLA D'ORO: solo fonti primarie, ZERO aggregator terzi
-- Già applicata via MCP Supabase in data 2026-08-06
-- ============================================================

INSERT INTO public.news_sources (name, category, country, feed_url, watch_type, css_selector, enabled) VALUES
  ('OECD Tax News',                    'TP',  'INT', 'https://www.oecd.org/tax/news/rss.xml',                                                    'RSS',        NULL, true),
  ('OECD BEPS Transfer Pricing',       'TP',  'INT', 'https://www.oecd.org/tax/transfer-pricing/rss.xml',                                        'RSS',        NULL, true),
  ('Agenzia Entrate - Provvedimenti TP','TP',  'IT',  NULL,                                                                                        'HTML_WATCH', '.provvedimenti-list > li > a', true),
  ('Kluwer International Tax Blog',    'TP',  'INT', 'https://kluwertaxblog.com/feed/',                                                           'RSS',        NULL, true),
  ('OECD Inclusive Framework BEPS',    'P2',  'INT', 'https://www.oecd.org/tax/beps/rss.xml',                                                    'RSS',        NULL, true),
  ('European Commission TAXUD',        'P2',  'EU',  'https://ec.europa.eu/taxation_customs/news/rss_en',                                        'RSS',        NULL, true),
  ('MEF - D.Lgs. 209/2023 Pillar Two', 'P2',  'IT',  NULL,                                                                                        'HTML_WATCH', '.comunicati-list a', true),
  ('HMRC UK - Pillar Two Guidance',    'P2',  'UK',  'https://www.gov.uk/government/organisations/hm-revenue-customs/announcements.atom',         'ATOM',       NULL, true),
  ('Government of Canada - GMT',       'P2',  'CA',  'https://www.canada.ca/en/news/tag/international-tax.rss',                                  'RSS',        NULL, true),
  ('European Commission VAT Updates',  'VAT', 'EU',  'https://ec.europa.eu/taxation_customs/vat-gst-news/rss_en',                               'RSS',        NULL, true),
  ('Agenzia Entrate - Circolari IVA',  'VAT', 'IT',  NULL,                                                                                        'HTML_WATCH', '.circolari-list > li > a', true),
  ('HMRC UK - VAT Notices',            'VAT', 'UK',  'https://www.gov.uk/topic/vat/announcements.atom',                                          'ATOM',       NULL, true),
  ('ATO Australia - GST Updates',      'VAT', 'AU',  'https://www.ato.gov.au/rss/news.xml',                                                      'RSS',        NULL, true),
  ('OECD BEPS Action Plans',           'AA',  'INT', 'https://www.oecd.org/tax/beps/rss.xml',                                                    'RSS',        NULL, true),
  ('EU Code of Conduct Group',         'AA',  'EU',  NULL,                                                                                        'HTML_WATCH', '.code-of-conduct a', true),
  ('Agenzia Entrate - Interpelli',     'AA',  'IT',  NULL,                                                                                        'HTML_WATCH', '.interpelli-list > li > a', true),
  ('IRS - Anti-abuse Guidance',        'AA',  'US',  'https://www.irs.gov/newsroom/news.rss',                                                    'RSS',        NULL, true),
  ('CBDT India - TP Circulars',        'TP',  'IN',  NULL,                                                                                        'HTML_WATCH', '.circular-list a', true)
ON CONFLICT (name) DO NOTHING;
