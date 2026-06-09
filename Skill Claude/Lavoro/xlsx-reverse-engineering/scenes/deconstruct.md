# Scene: Deconstruct — Deep Structural Analysis

**Goal**: Break down the spreadsheet into its constituent parts. Answer "How is it built?" with precision.

## When to Use

- User says "analyze the structure", "break down the formulas", "what are the data validations?", "how is this organized?"
- Second phase after discovery, when you need structural details
- Before documentation or migration work

## Workflow

### Step 1: Run Deconstruct Tool

```bash
# Analyze all sheets
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" deconstruct <file> --pretty

# Or focus on a specific sheet
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" deconstruct <file> --sheet "Sheet1" --pretty
```

### Step 2: Run Data Flow Analysis

```bash
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" dataflow <file> --pretty
```

### Step 3: Run Hidden Content Scan

```bash
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" hidden <file> --pretty
```

### Step 4: Analyze Each Sheet

For each sheet, produce a structured analysis:

#### Sheet Anatomy
- **Purpose**: What is this sheet for? (Input/Calculation/Output/Lookup/Config)
- **Layout**: Header row, data range, totals row, footer
- **Key Columns**: What each significant column represents
- **Data Types**: Numbers, dates, text, booleans
- **Special Features**: Merged cells, conditional formatting, data validation

#### Formula Analysis
For each formula type found:
- **Function**: Which Excel functions are used
- **Pattern**: What common pattern does this formula follow (lookup, aggregation, conditional, text manipulation)
- **Business Meaning**: What does this formula calculate in business terms
- **Dependencies**: What cells/sheets does it reference
- **Error Handling**: Does it use IFERROR, IFNA, or is it unprotected against division by zero

#### Named Range Analysis
For each named range:
- **Name**: Is it descriptive or cryptic?
- **Scope**: Workbook-level or sheet-level?
- **Reference**: What does it point to?
- **Usage**: Is it referenced in formulas? Which ones?

#### Data Validation Analysis
For each validation rule:
- **Range**: Which cells are validated
- **Type**: Dropdown list, number range, date range, custom formula
- **Business Rule**: What constraint does this enforce
- **Error Handling**: Is error messaging helpful or generic

#### Conditional Formatting Analysis
For each rule:
- **Range**: Which cells are formatted
- **Condition**: What triggers the formatting
- **Visual Effect**: What formatting is applied (color, icon, data bar)
- **Business Meaning**: Why does this condition matter

### Step 5: Identify the Data Model

Synthesize the structural analysis into a data model:

1. **Input Layer**: Which cells/sheets accept user input? What constraints exist?
2. **Processing Layer**: Which formulas perform calculations? What are the calculation chains?
3. **Output Layer**: Which cells/sheets present results? Charts? Reports?
4. **Reference Data**: Which sheets/ranges serve as lookup tables? Named ranges?
5. **Configuration**: Any hardcoded constants, parameter cells, or settings?

### Step 6: Present Results

The deconstruction output should be organized by sheet, with a cross-sheet summary at the end showing the overall architecture.

**Output Format Options**:
- **Structured text**: Organized by sheet with clear headings
- **JSON**: The raw tool output for programmatic use
- **Architecture diagram**: Using the Mermaid data flow output from the dataflow command

If the user has a specific question about a particular sheet or formula, focus on that area rather than producing the full deconstruction.
