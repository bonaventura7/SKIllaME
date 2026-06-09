# Scene: Audit Forensic — Security and Anomaly Analysis

**Goal**: Identify security risks, hidden content, anomalies, and potential malicious elements in a spreadsheet.

## When to Use

- User says "is this spreadsheet safe?", "find hidden content", "audit this file for risks", "check for malicious macros"
- Security review before opening an untrusted file
- Compliance audit
- Investigating suspicious spreadsheet behavior

## Workflow

### Step 1: Run Forensic Tools

```bash
# Forensic analysis
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" audit-forensic <file> --pretty

# OOXML low-level parse
python3 "$RE_SKILL_DIR/scripts/ooxml_parser.py" <file> --pretty

# Hidden content scan
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" hidden <file> --pretty

# VBA extraction (if applicable)
python3 "$RE_SKILL_DIR/scripts/reverse_engineer.py" vba-extract <file> --full-code --pretty
```

### Step 2: Analyze Security Findings

For each finding, assess:

#### Workbook-Level Security
- **Encryption**: Is the file encrypted? What algorithm?
- **Workbook protection**: Is structure locked? Is it trivially bypassable?
- **Digital signatures**: Is the file signed? Is the signature valid?

#### Sheet-Level Security
- **Protected sheets**: Which sheets? Password-protected or trivially removable?
- **Hidden content**: Hidden sheets, very hidden sheets, hidden rows/columns
- **White-on-white text**: Cells with white font on white background (stealth data)

#### External Attack Surface
- **External data connections**: What servers/databases does it connect to?
- **External file references**: What other files does it depend on?
- **Hyperlinks**: Are there hyperlinks to external URLs?

#### VBA Risk Assessment
- **Auto-executing macros**: Auto_Open, Workbook_Open, auto macros
- **Suspicious API calls**: CreateObject, Shell, WScript, Environ, Kill, etc.
- **File system access**: ChDir, ChDrive, MkDir, RmDir, FileCopy, etc.
- **Network access**: XMLHTTP, WinHttp, URLDownloadToFile
- **Process manipulation**: Shell, CreateProcess, WaitForSingleObject

#### Data Exfiltration Risk
- Formulas that send data externally (WEBSERVICE function)
- VBA that uploads data
- Connections that could leak data

### Step 3: Analyze Anomalies

#### Structural Anomalies
- **Extension mismatch**: .xlsx file containing VBA (should be .xlsm)
- **Excessive styles**: >500 cell styles (corruption risk)
- **Suspicious ZIP paths**: Path traversal or unusual characters in internal paths
- **Missing required parts**: No workbook.xml, no [Content_Types].xml

#### Content Anomalies
- **Self-referencing formulas**: Cells that reference themselves
- **Circular references**: Intentional or accidental?
- **Deprecated functions**: Functions removed in newer Excel versions
- **Inconsistent data types**: Numbers stored as text, dates as numbers

#### Version Anomalies
- **Legacy format indicators**: Features from older Excel versions
- **Compatibility issues**: Functions that don't work in all Excel versions

### Step 4: Produce Risk Report

Structure the forensic audit report:

```markdown
# Forensic Audit Report: [Filename]

## Risk Summary
- Overall risk level: [CRITICAL/HIGH/MEDIUM/LOW]
- High severity findings: [count]
- Medium severity findings: [count]
- Low severity findings: [count]

## Security Findings
### [SEVERITY] [Type]: [Description]
- Detail
- Evidence
- Recommendation

## Hidden Content
- Very hidden sheets: [list with purpose assessment]
- Hidden named ranges: [list with content description]
- Stealth text (white-on-white): [locations]

## Anomaly Findings
### [Type]: [Description]
- Detail
- Impact assessment

## VBA Analysis (if applicable)
- Module inventory with risk classification
- Auto-executing macros identified
- Suspicious pattern catalog
- Recommended actions

## Recommendations
1. [Critical items to address immediately]
2. [Important items to address soon]
3. [Nice-to-have improvements]
```

### Step 5: Severity Classification Guide

| Severity | Criteria | Example |
|----------|----------|---------|
| **CRITICAL** | Active exploit risk, data exfiltration capability | VBA with Shell + network access |
| **HIGH** | Significant security or data integrity risk | Very hidden sheets with critical logic, external connections to unknown servers |
| **MEDIUM** | Moderate risk, could be exploited with effort | Trivially removable sheet protection, extension mismatch |
| **LOW** | Minor issue, cosmetic or best-practice | Excessive styles, deprecated functions |
| **INFO** | Notable but not a risk | File metadata, application version |
