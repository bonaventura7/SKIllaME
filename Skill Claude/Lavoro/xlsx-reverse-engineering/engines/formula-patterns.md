# Reference: Common Formula Patterns and Business Meaning

## Purpose

When reverse engineering a spreadsheet, recognizing common formula patterns helps quickly understand business logic without analyzing each formula individually. This reference maps formula patterns to their typical business meanings.

## Aggregation Patterns

| Pattern | Formula | Business Meaning |
|---------|---------|-----------------|
| Simple sum | `=SUM(range)` | Total of values |
| Conditional sum | `=SUMIF(criteria_range, criteria, sum_range)` | Total where condition is met |
| Multi-condition sum | `=SUMPRODUCT((cond1)*(cond2)*(values))` | Total where multiple conditions met |
| Running total | `=SUM($A$1:A1)` | Cumulative running balance |
| Weighted average | `=SUMPRODUCT(weights,values)/SUM(weights)` | Weighted mean calculation |
| Count distinct | `=SUMPRODUCT(1/COUNTIF(range,range))` | Count unique values |

## Lookup Patterns

| Pattern | Formula | Business Meaning |
|---------|---------|-----------------|
| Exact match lookup | `=VLOOKUP(key, table, col, 0)` | Find exact record by key |
| Approximate match | `=VLOOKUP(key, table, col, 1)` | Tax bracket, tiered pricing |
| Two-column lookup | `=INDEX(result_col, MATCH(key, key_col, 0))` | Flexible retrieval |
| Two-key lookup | `=INDEX(Data, MATCH(1,(key1=Col1)*(key2=Col2),0))` | Composite key lookup (CSE) |
| Left lookup | `=INDEX(return_col, MATCH(key, lookup_col, 0))` | Lookup to the left (VLOOKUP can't) |

## Conditional Logic Patterns

| Pattern | Formula | Business Meaning |
|---------|---------|-----------------|
| Binary decision | `=IF(condition, value_if_true, value_if_false)` | Yes/No, Pass/Fail |
| Tiered classification | `=IF(A1>1000,"High",IF(A1>500,"Med","Low"))` | Risk tier, customer segment |
| Multi-case | `=IFS(cond1,val1, cond2,val2, TRUE,default)` | Multiple categories |
| Error guard | `=IFERROR(formula, fallback)` | Graceful error handling |
| Null guard | `=IF(A1="","",formula)` | Skip empty cells |

## Date/Time Patterns

| Pattern | Formula | Business Meaning |
|---------|---------|-----------------|
| Age calculation | `=DATEDIF(birth,TODAY(),"Y")` | Person's age |
| Days between | `=end_date - start_date` | Duration, aging |
| Business days | `=NETWORKDAYS(start, end, holidays)` | Working days between dates |
| End of month | `=EOMONTH(date, 0)` | Month-end closing date |
| Quarterly date | `=DATE(YEAR(A1),CEILING(MONTH(A1),3)+1,0)` | Quarter-end date |
| Year fraction | `=YEARFRAC(start, end)` | Time proportion for interest |

## Financial Patterns

| Pattern | Formula | Business Meaning |
|---------|---------|-----------------|
| Loan payment | `=PMT(rate, nper, -pv)` | Monthly payment amount |
| Present value | `=PV(rate, nper, -pmt)` | Current value of future cash flows |
| Net present value | `=NPV(rate, cashflows) + initial_investment` | Investment evaluation |
| Internal rate of return | `=IRR(cashflows)` | Break-even discount rate |
| Depreciation | `=SLN(cost, salvage, life)` | Straight-line depreciation |
| Compound growth | `=(end/start)^(1/periods)-1` | CAGR calculation |

## Text Manipulation Patterns

| Pattern | Formula | Business Meaning |
|---------|---------|-----------------|
| Extract prefix | `=LEFT(A1, FIND("-",A1)-1)` | Parse product code |
| Concatenate name | `=A1 & " " & B1` | Full name from first + last |
| Format number | `=TEXT(A1, "#,##0.00")` | Display formatting |
| Clean whitespace | `=TRIM(CLEAN(A1))` | Data cleansing |
| Substitute | `=SUBSTITUTE(A1, "old", "new")` | String replacement |

## Warning Pattern: Red Flags

| Pattern | Formula | Why It's Risky |
|---------|---------|----------------|
| Volatile reference | `=INDIRECT("Sheet"&A1&"!B2")` | Breaks if sheet renamed, slow recalc |
| Offset range | `=SUM(OFFSET(A1,0,0,B1,1))` | Volatile, hard to debug, fragile |
| Circular with iteration | `=A1+1` (self-referencing) | Requires iteration enabled, fragile |
| Hardcoded array | `={1,2,3;4,5,6}` | CSE formula, hard to edit |
| Deep nesting | `=IF(IF(IF(...)))` 5+ levels | Nearly impossible to understand |
| Magic number | `=A1*0.0875` | What is 0.0875? Tax rate? Use named range |

## Naming Convention Recommendations

When reconstructing, translate formula patterns into readable named ranges:

| Original | Reconstructed |
|----------|--------------|
| `=B5*0.0875` | `=Revenue * TaxRate` |
| `=VLOOKUP(A2,Sheet3!A:D,3,0)` | `=VLOOKUP(ProductCode, PriceList, UnitPrice, 0)` |
| `=IF(C10>100000,"A",IF(C10>50000,"B","C"))` | `=IF(Revenue>TierAThreshold, "A", IF(Revenue>TierBThreshold, "B", "C"))` |
