---
name: firecrawl-search
version: 1.0
description: Wrapper per "firecrawl search" — integrazione e best practice per usare Firecrawl search per ricerca web via MCP/HTTP.
agents: [main_agent, search_agent]
triggers: [firecrawl, firecrawl search, search web, web crawl]
---

# Firecrawl Search

Missione

Fornire accesso strutturato e ricette operative per usare Firecrawl (search crawler) come fonte di conoscenza in pipeline agentiche. Include esempi di query, rate limiting, e post-processing dei risultati.

Quando Usarla

- Vuoi effettuare ricerche web mirate e integrare risultati in un agent workflow
- Hai bisogno di estrarre snippet, link, e metadati da pagine web in batch

Trigger Keywords

`firecrawl`, `firecrawl search`, `web search`, `crawl web`, `search crawl`

Processo Standard

1. Configura endpoint MCP o HTTP per Firecrawl
2. Esegui query con parametri (depth, filters, domains)
3. Normalizza risultati (title, url, snippet, date)
4. Indicizza o passa a un neural search / QA pipeline

Formato Output

JSON array di risultati con campi: url, title, snippet, content_preview, crawl_time, source

Workaround / Limitazioni

- Rispetta robots.txt e rate limits
- Pagina dinamiche potrebbero richiedere rendering (headless browser)
- Cleanup dei duplicati necessario per pipeline di retrieval

Source: Skill Claude/Scaricate/Skill/firecrawl search.md
