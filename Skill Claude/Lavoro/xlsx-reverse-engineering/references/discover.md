# Scene: Discover — Quick Surface Scan

**Goal**: Get a rapid overview of an unknown spreadsheet. Answer "What am I looking at?" in under 30 seconds.

## When to Use

- User says "what's in this file?", "give me an overview", "what does this spreadsheet contain?"
- First step before any deeper analysis
- Triaging multiple files to prioritize deep analysis

## Workflow

### Step 1: Run Discovery Tool

```bash
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" discover <file> --pretty
```

### Step 2: Run OOXML Parser for Supplementary Data

```bash
python3 "$RE_SKILL_DIR/scripts/ooxml_parser.py" <file> --pretty --section workbook
```

### Step 3: Interpret the Results

Based on the discovery output, provide the user with a human-readable summary covering:

1. **File Identity**: What is this file? When was it created? By whom?
2. **Structure Overview**: How many sheets? What are they called? Any hidden?
3. **Complexity Assessment**: Is this simple (a few formulas) or complex (hundreds of formulas, VBA, connections)?
4. **Key Findings**: Anything notable — VBA macros, external connections, very hidden sheets, large size
5. **Recommended Next Steps**: Should they go deeper? Which scene to use next?

### Step 4: Classify the Spreadsheet Type

Based on the discovery data, classify the spreadsheet into one of these archetypes:

| Archetype | Indicators | Typical Risk |
|-----------|-----------|-------------|
| **Data Entry Form** | Few formulas, data validations, protected sheets | Low |
| **Calculator/Tool** | Many formulas, few input cells, clear I/O | Medium |
| **Financial Model** | VLOOKUP/INDEX-MATCH-heavy, multiple scenarios, cross-sheet refs | High |
| **Report/Dashboard** | Charts, pivot tables, external data connections | Medium |
| **Database Replacement** | Large data ranges, sorting/filtering, no formulas | Low-Medium |
| **Legacy System Export** | Old dates, inconsistent formatting, hard-coded values | High |
| **Multi-User Tracker** | Shared workbook, protection, comments | Medium |
| **VBA Application** | xlsm, extensive macros, userforms | High |

This classification helps the user understand what they're dealing with and guides which scene to use next.

### Step 5: Present Results

Format the output based on user's communication style:
- **Brief** (default): 5-10 bullet points + classification + recommendation
- **Detailed**: Full structured summary with all discovery data

If the user just asked a quick question, answer it directly without the full workflow.
