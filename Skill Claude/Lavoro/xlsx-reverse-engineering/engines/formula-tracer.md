# Engine: Formula Tracer — Deep Formula Analysis

**Purpose**: Analyze, classify, and trace the logic of spreadsheet formulas. Go beyond "what formula is in this cell" to understand "what does this formula mean and how fragile is it."

## Formula Classification System

### By Function Type
| Category | Functions | Typical Business Meaning |
|----------|-----------|------------------------|
| **Aggregation** | SUM, AVERAGE, COUNT, MIN, MAX, SUMPRODUCT | Totals, averages, counts |
| **Lookup** | VLOOKUP, HLOOKUP, INDEX, MATCH, XLOOKUP | Data retrieval from reference tables |
| **Conditional** | IF, IFS, SWITCH, SUMIF, COUNTIF, AVERAGEIF | Business rules and filters |
| **Reference** | INDIRECT, OFFSET, ADDRESS | Dynamic cell references (high risk) |
| **Date/Time** | DATE, EDATE, EOMONTH, NETWORKDAYS | Date calculations, aging, schedules |
| **Text** | LEFT, RIGHT, MID, CONCAT, TEXTJOIN, SUBSTITUTE | Text manipulation, ID generation |
| **Math** | ROUND, CEILING, FLOOR, MOD, POWER | Precision control, cyclical calculations |
| **Financial** | NPV, IRR, PMT, FV, PV, RATE | Financial modeling |
| **Logical** | AND, OR, NOT, XOR | Compound conditions |
| **Information** | ISBLANK, ISERROR, ISTEXT, TYPE | Error checking, type validation |
| **Volatile** | NOW, TODAY, RAND, RANDBETWEEN | Change on every recalc (performance risk) |

### By Complexity Level
| Level | Criteria | Example |
|-------|----------|---------|
| **Simple** | Single function, 1-2 arguments | `=SUM(A1:A10)` |
| **Moderate** | Nested 2 levels, or multiple functions | `=IF(A1>0, VLOOKUP(A1,Table,2,0), 0)` |
| **Complex** | Nested 3+ levels, or 5+ functions | `=IFERROR(INDEX(Data,MATCH(1,(A1=Col1)*(B1=Col2),0)),"Not found")` |
| **Critical** | Mega-formulas, volatile functions, INDIRECT/OFFSET | `=SUMPRODUCT((INDIRECT("Sheet"&ROW()&"!A:A")>0)*1)` |

### By Risk Level
| Risk | Criteria | Mitigation |
|------|----------|-----------|
| **Fragile** | Hardcoded row/column numbers, no error handling | Add IFERROR, use named ranges |
| **Volatile** | Uses INDIRECT, OFFSET, NOW, TODAY, RAND | Replace with non-volatile alternatives |
| **Opaque** | Long nested formula, no documentation | Break into helper columns, add comments |
| **Incompatible** | Dynamic array functions, new functions | Use SUMPRODUCT instead of FILTER, INDEX/MATCH instead of XLOOKUP |
| **External** | References other workbooks | Consolidate or document dependency |

## Tool Commands

```bash
# Get formula inventory for a sheet
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" deconstruct <file> --sheet "Sheet1" --pretty

# Trace a specific formula's dependencies
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" trace <file> "Sheet1!B10" --pretty
```

## Analysis Workflow

### Step 1: Formula Inventory
Run deconstruct to get the full formula inventory per sheet. Focus on:
- Which formula types appear most frequently
- Which cells have the most complex formulas
- Where are cross-sheet references

### Step 2: Pattern Recognition
Identify common formula patterns and their business meaning:

| Pattern | Formula Example | Business Meaning |
|---------|----------------|-----------------|
| Simple sum | `=SUM(B2:B20)` | Adding up a column of values |
| Conditional sum | `=SUMIF(A:A,"Active",B:B)` | Sum values where condition is met |
| Lookup | `=VLOOKUP(A2,PriceList,2,0)` | Look up price from catalog |
| Index-Match | `=INDEX(Data,MATCH(A2,Keys,0),3)` | Flexible lookup (better than VLOOKUP) |
| Tiered calculation | `=IF(A1>1000,A1*0.1,IF(A1>500,A1*0.05,0))` | Tiered commission or discount |
| Growth rate | `=(B2-B1)/B1` | Period-over-period growth |
| Running total | `=SUM($B$2:B2)` | Cumulative sum |
| Age calculation | `=DATEDIF(A2,TODAY(),"Y")` | Age from birthdate |
| Debt service | `=PMT(rate,nper,-pv)` | Loan payment calculation |

### Step 3: Error Handling Audit
Check every formula for proper error handling:
- Divisions without IFERROR or IF(denom=0,...)
- VLOOKUP without IFERROR or IFNA
- INDEX/MATCH without IFERROR
- Date calculations that could produce #VALUE!
- References to potentially empty cells

### Step 4: Hardcoded Value Detection
Scan for "magic numbers" in formulas:
- Numeric constants that should be named ranges or input cells
- Text strings that represent categories or thresholds
- Cell references that should be named ranges

### Step 5: Volatile Function Impact
Identify all volatile functions and assess their impact:
- How many cells use them?
- How many dependents do those cells have?
- Is the volatility necessary? (e.g., TODAY for current date in a header is fine; INDIRECT for dynamic sheet references is risky)

### Step 6: Present Findings

Organize formula analysis results:
1. **Formula Distribution**: Pie chart of formula types by count
2. **Complexity Heatmap**: Which sheets/areas have the most complex formulas
3. **Risk Catalog**: List of formulas with fragility/opacity/volatility issues
4. **Business Logic Summary**: Plain-language description of what the formulas compute
5. **Improvement Recommendations**: Specific changes to reduce risk and improve readability
