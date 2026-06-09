# Engine: Dependency Map — Cell and Sheet Dependency Analysis

**Purpose**: Map the complete dependency graph of a spreadsheet — which cells depend on which, which sheets read from which, and how data flows through the workbook.

## Core Concepts

### Dependency Types
1. **Same-sheet reference**: Formula in Sheet1 references another cell in Sheet1
2. **Cross-sheet reference**: Formula in Sheet1 references a cell in Sheet2
3. **External file reference**: Formula references a cell in another workbook file
4. **Named range reference**: Formula uses a named range (indirect reference)
5. **VBA-driven dependency**: Macro writes values that formulas depend on

### Dependency Direction
- **Precedent**: A cell that feeds INTO another cell's formula (upstream)
- **Dependent**: A cell that depends on another cell's value (downstream)

## Tool Commands

```bash
# Generate full data flow map with Mermaid diagram
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" dataflow <file> --pretty

# Trace a specific cell's dependencies
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" trace <file> "Sheet1!B10" --pretty
```

## Analysis Workflow

### Step 1: Sheet-Level Dependency Map

Start with the `dataflow` command to get the high-level picture:
- Which sheets read from which other sheets
- Sheet role classification (input, calculation, output, intermediate)
- Identify the data flow direction

### Step 2: Cell-Level Dependency Tracing

For critical cells (outputs, key calculations), use `trace` to get detailed dependencies:
- What cells feed into this calculation
- What cells depend on this calculation's result
- Are there cross-sheet dependencies

### Step 3: Build the Dependency Graph

For each sheet, construct a mental model of:
1. **Input cells** (no precedents, or only external data)
2. **Intermediate calculations** (precedents are input cells or other intermediates)
3. **Output cells** (no dependents, or only chart/report dependents)
4. **Circular references** (cells that ultimately reference themselves)

### Step 4: Identify Critical Paths

The critical path is the chain of dependencies from input to the most important output:
1. Identify the primary output cells (the whole reason the spreadsheet exists)
2. Trace backward from outputs to inputs
3. Mark every cell on this path as "critical" — errors here propagate to the final result
4. Assess the fragility of each link (hardcoded? no error handling? external reference?)

### Step 5: Detect Problem Patterns

| Pattern | Description | Risk |
|---------|-------------|------|
| **Long chain** | Output depends on 5+ levels of formulas | High fragility |
| **Fan-out** | One cell feeds many formulas | Single point of failure |
| **Fan-in** | Many cells feed one formula | Complex to debug |
| **Orphan** | Cell with formula but no dependents | Possibly unused |
| **Circular** | Cell references itself directly or indirectly | May be intentional (iteration) or error |
| **External link** | Reference to another workbook | Breaks when file moves |
| **Hidden dependency** | VBA writes values that formulas read | Invisible in formula view |

## Output Formats

### Mermaid Flow Diagram
The `dataflow` command generates a Mermaid diagram. Use it directly or enhance with:
- Node labels showing sheet roles
- Color coding: green (input), orange (calculation), blue (output), purple (intermediate)
- Annotations for external references

### Textual Dependency Chain
For critical paths, present as a chain:
```
[Input] Parameters!B3 (Discount Rate: 8%)
  → [Calc] Model!C10 (PV Factor = 1/(1+B3)^Year)
    → [Calc] Model!D10 (Present Value = Cashflow * C10)
      → [Output] Summary!B5 (Total NPV = SUM(D10:D20))
```
