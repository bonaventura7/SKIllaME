---
name: mcp-notion-server
version: 1.0
description: Wrapper per integrare Notion via MCP — istruzioni di deploy, mapping delle API e casi d'uso. (Archivare pacchetto zip incluso)
agents: [connector_agent, sync_agent]
triggers: [mcp notion, notion mcp, notion connector, mcp-notion]
---

# MCP Notion Server

Missione

Fornire una guida rapida per usare il server MCP per sincronizzare e interrogare contenuti Notion da pipeline AI. Il codice sorgente è incluso come archivio (mcp-notion-server-main.zip) nella cartella Scaricate; vedi _archive/community per il pacchetto.

Quando Usarla

- Vuoi indicizzare pagine Notion e offrire retrieval semantico
- Hai bisogno di sincronizzazione bidirezionale fra Notion e il tuo datastore

Trigger Keywords

`mcp-notion`, `notion mcp`, `notion connector`, `notion sync`

Processo Standard

1. Estrarre il pacchetto e configurare credentials Notion
2. Avviare endpoint MCP e testare health checks
3. Mappare proprietà Notion a document schema per embedding
4. Programmare sync incrementale

Workaround / Limitazioni

- Verifica limiti API Notion e limiti di rate
- Gestire paginazione e proprietà personalizzate

Source (archive): Skill Claude/Scaricate/Skill/mcp-notion-server-main.zip
