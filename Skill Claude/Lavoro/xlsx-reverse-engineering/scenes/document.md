# Scene: Document — Generate Comprehensive Documentation

**Goal**: Produce a complete, human-readable document that captures everything about the spreadsheet's architecture, logic, and risks.

## When to Use

- User says "document this spreadsheet", "create a spec for this file", "write up what this Excel does"
- Handoff documentation for a new team member
- Compliance or audit documentation requirements
- Pre-migration documentation

## Workflow

### Step 1: Gather All Data

Run all analysis commands to collect comprehensive information:

```bash
# Discovery
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" discover <file> --pretty

# Deconstruct (all sheets)
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" deconstruct <file> --pretty

# Data flow
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" dataflow <file> --pretty

# Hidden content
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" hidden <file> --pretty

# Forensic
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" audit-forensic <file> --pretty

# VBA (if applicable)
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" vba-extract <file> --pretty
```

### Step 2: Generate Markdown Documentation

Use the `document` command for a pre-formatted starting point:

```bash
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" document <file> --format md
```

### Step 3: Enrich with Business Logic Interpretation

The tool output captures *what* the spreadsheet contains. Your job is to add *why* — the business logic interpretation. For each sheet and formula area:

1. **State the observable facts** from tool output
2. **Add your interpretation** of what this means in business terms
3. **Flag uncertainties** where the purpose isn't clear

### Step 4: Structure the Documentation

Organize the documentation using this template:

```markdown
# Reverse Engineering Report: [Filename]

## Executive Summary
- What this spreadsheet does (1-2 sentences)
- Complexity rating and key risk areas
- Recommended audience (who should read this)

## File Metadata
- Author, creation date, last modified
- Application used
- File format details

## Architecture Overview
- Sheet inventory with roles
- Data flow diagram (Mermaid)
- Input → Processing → Output summary

## Detailed Sheet Analysis
### [Sheet Name] — [Role: Input/Calculation/Output/Lookup/Config]
- Purpose
- Layout description
- Key columns/ranges
- Formulas (with business meaning)
- Data validations
- Conditional formatting
- Named ranges used
- Protection status

## Named Ranges Catalog
| Name | Scope | Reference | Purpose |
|------|-------|-----------|---------|

## Formula Catalog
| Sheet | Cell | Formula | Business Meaning | Dependencies |
|-------|------|---------|-----------------|-------------|

## Data Validation Rules
| Sheet | Range | Type | Constraint | Business Rule |
|-------|-------|------|-----------|--------------|

## VBA Macros (if applicable)
- Module inventory
- Auto-executing macros
- Business logic summary
- Suspicious patterns

## Hidden Content
- Hidden sheets
- Very hidden sheets
- Hidden named ranges
- Hidden rows/columns

## Risk Assessment
- Fragility areas (hardcoded values, no error handling)
- Opacity areas (complex formulas, undocumented logic)
- Security concerns (external connections, VBA, protection)
- Compatibility issues (version-specific functions, external refs)

## Recommendations
- Critical fixes
- Documentation improvements
- Structure improvements
- Migration considerations
```

### Step 5: Deliver

Save the documentation to the user's requested location. If no location specified, save to `/home/z/my-project/download/` with a descriptive filename.

If the user wants a formal document file (PDF/DOCX), use the appropriate skill (docx or pdf) to convert the Markdown output into a polished document.
