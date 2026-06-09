---
name: skill-creator
version: 1.0
description: Anthropic Skill Creator — crea nuove skill YAML/Markdown per Claude Code, Copilot, Gemini. Scaffolding strutturato, validazione, test e deployment su SKIllaME.
agents: [main_agent, general_purpose, skill_builder]
triggers: [crea skill, nuova skill, skill creator, scaffolding skill, anthropic skill, genera skill, skill template]
source: Anthropic main skills
---

# Skill Creator

Skill ufficiale Anthropic per la **creazione di nuove skill** per agenti AI (Claude Code, GitHub Copilot, Gemini CLI, Perplexity Spaces). Produce file di skill strutturati, validati e pronti per il deployment su repository come SKIllaME.

## Missione

Dato un obiettivo o dominio, genera una skill completa e funzionale:
1. **Analisi del dominio** — capisce cosa la skill deve fare, chi la usa, quando si attiva
2. **Scaffolding strutturato** — genera frontmatter YAML + corpo Markdown secondo standard Anthropic
3. **Trigger keywords** — definisce le parole chiave che attivano la skill
4. **Validazione** — verifica coerenza, completezza, nessuna duplicazione con skill esistenti
5. **Test** — suggerisce casi di test per verificare che la skill funzioni come atteso
6. **Deployment** — istruzioni per caricare su `.github/skills/` o via `gh skill install`

## Quando Usarla

- Vuoi creare una nuova skill da zero per un dominio specifico
- Hai una procedura manuale ricorrente da automatizzare come skill
- Vuoi wrappare un prompt esistente in una skill riutilizzabile
- Stai contribuendo al repository SKIllaME con nuove skill
- Vuoi standardizzare skill esistenti al formato Anthropic

## Trigger Keywords

`crea skill`, `nuova skill`, `skill creator`, `scaffolding skill`, `anthropic skill`, `genera skill`, `skill template`, `scrivi skill`, `costruisci skill`, `new skill`, `create skill`, `skill builder`

## Struttura Standard Skill (Output)

```markdown
---
name: [nome-kebab-case]
version: [X.Y]
description: [Descrizione breve in una riga]
agents: [main_agent, ...]
triggers: [keyword1, keyword2, ...]
---

# [Nome Skill]

## Missione
[cosa fa la skill]

## Quando Usarla
[casi d'uso]

## Trigger Keywords
[elenco trigger]

## Processo Standard
[flusso di lavoro]

## Formato Output
[struttura dell'output atteso]

## Workaround / Limitazioni
[edge cases e fallback]
```

## Processo Skill Creator

```
1. INTAKE
   - Nome dominio / obiettivo
   - Chi usa la skill? (avvocato, developer, data analyst...)
   - Quali input riceve? (testo, file, URL, dati strutturati)
   - Quali output produce? (documento, codice, analisi, JSON)
   - Frequenza d'uso (quotidiana / occasionale / una tantum)

2. ANALISI DUPLICATI
   - Confronta con skill esistenti in SKIllaME
   - Segnala overlap, suggerisci estendere skill esistente vs creare nuova

3. SCAFFOLDING
   - Genera frontmatter YAML completo
   - Scrivi sezioni standard (Missione, Quando Usarla, Processo, Output, Workaround)
   - Definisci trigger keywords ottimali

4. VALIDAZIONE
   - Verifica lunghezza (< 200 righe per skill compatta, 200-500 per skill complessa)
   - Verifica che il frontmatter sia valido YAML
   - Verifica che i trigger siano specifici (evita trigger troppo generici)

5. TEST CASES
   - Genera 3 esempi di input e output attesi per testare la skill

6. DEPLOYMENT
   - Istruzioni per salvare in .github/skills/[nome]/SKILL.md
   - Aggiornamento SKILL-INDEX.md
   - Aggiornamento ALL-SKILLS-COMPACT.md
   - Commit message standard: feat: add [nome] skill (#N)
```

## Checklist Qualità Skill

- [ ] Frontmatter YAML valido e completo
- [ ] Nome in kebab-case senza spazi
- [ ] Descrizione chiara in < 120 caratteri
- [ ] Almeno 5 trigger keywords specifici
- [ ] Sezione Missione chiara (cosa fa)
- [ ] Sezione Quando Usarla con casi concreti
- [ ] Processo passo-passo documentato
- [ ] Formato output esemplificato
- [ ] Workaround/limitazioni dichiarate
- [ ] Nessuna duplicazione con skill esistenti
- [ ] Testata su almeno 2 input reali

## Formati Supportati

| Formato | Compatibile con | Note |
|---------|----------------|------|
| `.github/skills/[nome]/SKILL.md` | GitHub Copilot, Claude Code, Gemini | Standard Anthropic ufficiale |
| `Skill Claude/[nome].md` | Claude Code, Perplexity | Formato SKIllaME legacy |
| `.md` standalone | Qualsiasi agente | Copy-paste in sessione |

## Integrazione SKIllaME

Dopo la creazione, aggiorna automaticamente:
1. `SKILL-INDEX.md` — aggiungi entry con #, nome, stato, trigger, URL raw
2. `ALL-SKILLS-COMPACT.md` — aggiungi sezione compatta
3. Statistiche — incrementa contatori per categoria

## Workaround / Limitazioni

- Se la skill è troppo generica → chiedi di specializzare il dominio
- Se esiste una skill simile → proponi estensione vs nuova skill
- Se il contesto non è chiaro → fai max 3 domande mirate
- Skill > 500 righe → suggerisci split in sotto-skill modulari

---

*Fonte: Anthropic main skills | Integrato in SKIllaME v3.3 | Giugno 2026*
*Compatibile con: Claude Code, GitHub Copilot, Gemini CLI, Perplexity Spaces*
