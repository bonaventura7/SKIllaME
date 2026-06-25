---
name: exa-mcp-neural-search
version: 1.0
description: Neural search wrapper per usare Exa MCP server come retriever per contenuti web, codice, aziende, persone.
agents: [main_agent, retrieval_agent]
triggers: [exa mcp, exa mcp search, neural search, exa neural]
---

# Exa MCP Neural Search

Missione

Illustrare come collegare un MCP Exa server per fornire ricerca semantica su sorgenti web, codice e directory aziendali. Contiene esempi di embedding, schema di indicizzazione e query di scoring.

Quando Usarla

- Hai grandi set di documenti web o codice da interrogare semanticamente
- Vuoi un retriever a bassa latenza integrato in agent pipeline

Trigger Keywords

`exa mcp`, `neural search`, `semantic search`, `exa search`

Processo Standard

1. Preprocess: estrai testo, metadata, chunking
2. Calcola embeddings e carica nel server Exa
3. Usa query semantiche per recuperare top-K risultati
4. Rerank con segnali basati su domain-specific heuristics

Formato Output

Top-K risultati con score, passage, source_uri, embedding_vector (opzionale)

Workaround / Limitazioni

- Gestire aggiornamenti incrementali dei corpus
- Attenzione a costi di embedding per dataset molto grandi

Source: Skill Claude/Scaricate/Skill/Neural search for web content, code, companies, and people via the Exa MCP server.md
