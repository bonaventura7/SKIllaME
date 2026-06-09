# Scene: Migrate — Plan Migration to Another System

**Goal**: Analyze the spreadsheet and produce a migration specification for porting its logic to a database, web application, Python script, or other system.

## When to Use

- User says "migrate this Excel to a database", "convert this to Python", "port this spreadsheet to an app"
- Moving from spreadsheet-based processes to proper software systems
- Replacing a spreadsheet with a web dashboard or API

## Workflow

### Step 1: Full Analysis

Run all analysis tools to understand the complete spreadsheet:

```bash
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" discover <file> --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" deconstruct <file> --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" dataflow <file> --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" hidden <file> --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" vba-extract <file> --full-code --pretty
```

### Step 2: Identify Migration Target

Clarify with the user what system they're migrating to:

| Target | Key Considerations |
|--------|-------------------|
| **SQL Database** | Tables, relationships, constraints, stored procedures |
| **Python Application** | Data structures, calculation pipeline, input/output |
| **Web Application** | User interface, API endpoints, data persistence |
| **BI Tool** (Power BI, Tableau) | Data model, measures, visualizations |
| **NoSQL Database** | Document structure, nested data, denormalization |
| **Airtable/Smartsheet** | Table structure, linked records, views |

### Step 3: Map Spreadsheet to Target Architecture

#### Input Layer Mapping
For each input area in the spreadsheet:
- **Source**: Sheet, range, data validation rules
- **Target equivalent**: Database table + columns, API endpoint, UI form
- **Constraints**: Map data validation to target constraints (NOT NULL, CHECK, foreign keys)
- **Default values**: Capture any defaults or initial values

#### Processing Layer Mapping
For each calculation area:
- **Formula chain**: Order of operations, dependencies
- **Target equivalent**: SQL views, Python functions, API logic, stored procedures
- **Edge cases**: Error handling (IFERROR → try/except, null handling)
- **Named ranges**: Map to constants, configuration, or enum values

#### Output Layer Mapping
For each output area:
- **Source**: Sheet, range, chart
- **Target equivalent**: API response, dashboard widget, report template
- **Formatting**: Conditional formatting → CSS classes, UI state rules

#### Reference Data Mapping
For lookup tables and reference data:
- **Source**: Sheet, range, named range
- **Target equivalent**: Reference table, enum, configuration collection
- **Change frequency**: Static (hardcode OK) vs dynamic (needs admin UI)

#### VBA Logic Mapping
For each VBA macro:
- **Trigger**: When does it run? (Auto_Open, button click, worksheet event)
- **Logic**: What does it do? (data transformation, validation, import/export)
- **Target equivalent**: API endpoint, background job, event handler, middleware

### Step 4: Produce Migration Specification

```markdown
# Migration Specification: [Filename] → [Target System]

## Overview
- Source file description
- Target system description
- Migration complexity: [Simple/Moderate/Complex]
- Estimated effort: [days/weeks]

## Data Model
### Tables/Collections
| Table | Source Sheet | Columns | Key |
|-------|-------------|---------|-----|

### Relationships
| From Table | To Table | Type | Source Reference |
|-----------|---------|------|-----------------|

## Business Logic Mapping
### [Logic Name]
- **Source**: Sheet!Range, formula
- **Target**: [implementation approach]
- **Edge cases**: Division by zero, missing data, type mismatches
- **Test cases**: Input → Expected output

## Data Validation Mapping
| Source Rule | Target Constraint |
|-------------|------------------|

## VBA Migration
| Macro | Trigger | Logic Summary | Target Implementation |
|-------|---------|--------------|---------------------|

## Migration Checklist
- [ ] All input areas mapped
- [ ] All formulas converted
- [ ] Error handling replicated
- [ ] Data validations enforced
- [ ] Conditional formatting logic preserved
- [ ] Named ranges accounted for
- [ ] VBA macros migrated or documented as manual steps
- [ ] Hidden content reviewed for necessity
- [ ] Test data prepared
- [ ] Acceptance criteria defined

## Risks
- Formulas too complex for target system
- VBA logic with no direct equivalent
- External connections requiring network access
- User acceptance of new interface
```

### Step 5: Estimate Complexity

Use this scoring to estimate migration effort:

| Factor | Weight | Score (1-5) |
|--------|--------|-------------|
| Sheet count | 1 | |
| Formula count | 2 | |
| Cross-sheet references | 2 | |
| VBA complexity | 3 | |
| External connections | 2 | |
| Data validations | 1 | |
| Named ranges | 1 | |

Total score 5-10: Simple migration (days)
Total score 11-20: Moderate migration (weeks)
Total score 21+: Complex migration (months)
