# Scene: Reconstruct — Clean Rebuild from Reverse-Engineered Spec

**Goal**: Using the complete understanding of the spreadsheet, create a clean, well-structured rebuild specification that eliminates technical debt and improves maintainability.

## When to Use

- User says "rebuild this cleanly", "start fresh with this model", "create a better version"
- The original spreadsheet has become unmaintainable
- Need to fix structural issues while preserving all functionality

## Important: This is Specification, Not Execution

This scene produces a **rebuild specification** — a detailed blueprint for creating a clean version. The actual rebuild should use the **xlsx skill** for spreadsheet recreation or appropriate development tools for other platforms.

## Workflow

### Step 1: Full Analysis

```bash
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" discover <file> --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" deconstruct <file> --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" dataflow <file> --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" hidden <file> --pretty
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" audit-forensic <file> --pretty
```

### Step 2: Identify Technical Debt

Catalog all issues in the original:

#### Structure Issues
- Sheets with mixed purposes (should be separated)
- Redundant calculations (same formula in multiple places)
- Missing named ranges for key constants
- Inconsistent naming conventions
- Unused sheets, ranges, or named ranges

#### Formula Issues
- Hardcoded values that should be input cells
- Overly complex nested formulas (should be broken into steps)
- Missing error handling (no IFERROR/IFNA)
- Volatile functions used unnecessarily (NOW, TODAY, RAND, OFFSET, INDIRECT)
- Incompatible functions (dynamic arrays when compatibility needed)

#### Layout Issues
- Data and calculations on the same sheet
- No clear input/output separation
- Formatting inconsistent across similar elements
- Merged cells causing reference problems

#### Risk Issues
- No data validation on input cells
- Unprotected formulas that could be accidentally overwritten
- External references that could break
- VBA macros that could be replaced with formulas

### Step 3: Design the Clean Architecture

#### Sheet Architecture
Design the new sheet layout following best practices:

| Sheet Type | Purpose | Naming Convention |
|-----------|---------|-------------------|
| **Inputs** | User-editable data entry | `inp_*` or `Inputs` |
| **Parameters** | Constants and assumptions | `param_*` or `Config` |
| **Lookup** | Reference data tables | `lkp_*` or `Ref_*` |
| **Calculations** | Formula processing | `calc_*` or `Calc_*` |
| **Outputs** | Results and reports | `out_*` or `Report` |
| **Dashboard** | Visual summary | `dash_*` or `Dashboard` |

#### Named Range Strategy
- All input cells should have named ranges
- Constants should be named ranges (not magic numbers in formulas)
- Naming convention: camelCase or snake_case (consistent!)
- Scope: Prefer workbook-level unless sheet-specific

#### Formula Architecture
- Use helper columns instead of mega-formulas
- Use IFERROR consistently for all divisions and lookups
- Prefer INDEX/MATCH over VLOOKUP (more flexible, less fragile)
- Use named ranges in formulas (not cell references when possible)
- Document complex formulas with cell comments

#### Protection Strategy
- Lock all formula cells
- Unlock only input cells
- Use sheet protection with a consistent password
- Consider hiding calculation sheets

### Step 4: Create the Rebuild Specification

```markdown
# Rebuild Specification: [Filename]

## Overview
- Purpose of the spreadsheet
- What the rebuild changes vs preserves
- Migration strategy (parallel run, cut-over, gradual)

## Architecture
### Sheet Inventory
| Sheet | Type | Purpose | Source Mapping |
|-------|------|---------|---------------|

### Data Flow
[Mermaid diagram of new architecture]

### Named Ranges
| Name | Scope | Reference | Purpose |
|------|-------|-----------|---------|

## Sheet-by-Sheet Specification
### [Sheet Name] — [Type]
- **Layout**: [Describe cell-by-cell or use a table]
- **Input cells**: [List with named ranges]
- **Formulas**: [List with named range references]
- **Data validations**: [List with rules]
- **Conditional formatting**: [List with rules]
- **Protection**: [What's locked/unlocked]
- **Source mapping**: [Where each element comes from in the original]

## Migration Checklist
- [ ] All functionality preserved or intentionally removed
- [ ] All formulas have error handling
- [ ] All inputs have data validation
- [ ] All constants are named ranges
- [ ] Consistent naming conventions
- [ ] Sheet protection applied
- [ ] No hardcoded values in formulas
- [ ] No merged cells in data areas
- [ ] Cross-sheet references minimized
- [ ] Tested against original for same outputs

## Differences from Original
| Original Issue | Rebuild Change |
|---------------|---------------|
```

### Step 5: Hand Off to Build Phase

Once the specification is complete and approved:
- Use the **xlsx skill** to build the new spreadsheet
- Or use **fullstack-dev** for a web application replacement
- The specification serves as the requirements document for the build
