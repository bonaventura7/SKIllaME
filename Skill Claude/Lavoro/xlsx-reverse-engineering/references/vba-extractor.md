# Engine: VBA Extractor — Macro Extraction and Documentation

**Purpose**: Extract, analyze, and document VBA macros from .xlsm files. Understand what the macros do, when they trigger, and what risks they present.

## When VBA is Present

The `discover` command detects VBA via the `vbaProject.bin` file in the OOXML archive. When VBA is detected, this engine provides the detailed analysis.

## Tool Commands

```bash
# Extract VBA module list with previews
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" vba-extract <file> --pretty

# Extract full VBA source code
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" vba-extract <file> --full-code --pretty
```

**Note**: Full VBA extraction requires the `oletools` Python package. If not installed, the tool will report limited information from the OOXML archive structure.

Install oletools: `pip install oletools`

## VBA Module Classification

### By Module Type
| Type | Extension | Description |
|------|-----------|-------------|
| **Standard Module** | .bas | General code modules |
| **Class Module** | .cls | Object-oriented code |
| **UserForm** | .frm | Dialog box definitions + code |
| **ThisWorkbook** | — | Workbook-level event handlers |
| **Sheet Module** | — | Worksheet-level event handlers |

### By Trigger Type
| Trigger | Event | Auto-Executes? |
|---------|-------|---------------|
| **Auto_Open** | Workbook opens | Yes |
| **Workbook_Open** | Workbook opens | Yes |
| **Auto_Close** | Workbook closes | Yes |
| **Workbook_BeforeClose** | Workbook closes | Yes |
| **Worksheet_Change** | Cell value changes | Yes (event) |
| **Worksheet_Activate** | Sheet becomes active | Yes (event) |
| **Button_Click** | User clicks button | No (user action) |
| **Menu/Toolbar** | User selects menu item | No (user action) |
| **Timer** | Application.OnTime | Semi-automatic |
| **Called by other macro** | Sub/function call | Depends on caller |

### By Risk Level
| Risk | Pattern | Examples |
|------|---------|---------|
| **Safe** | Data manipulation within workbook | Sorting, formatting, copying data between sheets |
| **Low** | File operations within expected scope | Saving backup, exporting to CSV |
| **Medium** | System interaction | Registry reads, environment variables, file system browsing |
| **High** | External execution | Shell commands, CreateObject for scripting, downloading files |
| **Critical** | Data exfiltration or system modification | Network calls with data, process creation, file deletion |

## Analysis Workflow

### Step 1: Module Inventory
List all VBA modules with:
- Module name and type
- Number of lines of code
- Auto-executing triggers present
- Suspicious patterns detected

### Step 2: Macro Purpose Identification
For each macro (Sub/Function), determine:
- **Name**: Is it descriptive or obfuscated?
- **Parameters**: What inputs does it accept?
- **Trigger**: How and when does it run?
- **Actions**: What does it do? (high-level)
- **Side effects**: What does it change outside the workbook?

### Step 3: Data Flow Through VBA
VBA creates invisible dependencies. Map:
- Which cells does VBA READ from?
- Which cells does VBA WRITE to?
- What external resources does VBA access?
- What events trigger VBA execution?

This is critical because VBA-written values appear as constants in formula analysis — you can't understand the full data flow without knowing VBA writes them.

### Step 4: Business Logic Extraction
Translate VBA code into business rules:
```
VBA: If Range("B5").Value > 10000 Then
       Range("C5").Value = "Premium"
     Else
       Range("C5").Value = "Standard"
     End If

Business Rule: Customers with revenue > $10,000 are classified as "Premium"
Target Implementation: UPDATE customers SET tier = CASE WHEN revenue > 10000 THEN 'Premium' ELSE 'Standard' END
```

### Step 5: VBA → Formula Replacement Assessment
Some VBA macros exist because the original author didn't know how to do it with formulas. Assess each macro:

| VBA Pattern | Formula Replacement | Feasibility |
|-------------|-------------------|-------------|
| Simple IF/THEN | IF() function | Easy |
| Lookup + transform | INDEX/MATCH or VLOOKUP | Easy |
| Loop over rows | SUMPRODUCT or array formula | Moderate |
| Sort data | SORT function (Excel 365) or manual | Moderate |
| Import data | Power Query or external connection | Moderate |
| Create charts | Chart objects | Hard (limited formula support) |
| Send email | No formula equivalent | Keep VBA or use external tool |
| File system ops | No formula equivalent | Keep VBA or use external tool |

### Step 6: Present VBA Documentation

```markdown
## VBA Macro Documentation

### Module: [ModuleName] ([Type])
- **Lines of code**: [count]
- **Auto-executes**: [Yes/No, which events]
- **Risk level**: [Safe/Low/Medium/High/Critical]

### Sub [MacroName]()
- **Purpose**: [Business description]
- **Trigger**: [How it runs]
- **Reads from**: [Cell references]
- **Writes to**: [Cell references]
- **External access**: [Files, URLs, APIs]
- **Business logic**:
  [Plain-language description of the logic]
- **Formula replacement**: [Possible? What formula?]
```
