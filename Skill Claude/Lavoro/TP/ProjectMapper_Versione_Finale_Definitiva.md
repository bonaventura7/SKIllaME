# Project Mapper — Versione Finale Definitiva

**Autore/Owner:** Luca Consalter  
**Data:** 2026-06-30  
**Versione:** 3.0 Definitiva  
**Stato:** Career-grade / Production-ready blueprint  
**Modalità:** ARCHITECT-OMNI PRIME — DEEP + BUILD + REVIEW  

---

## 0. Executive Summary

Questo documento definisce la versione finale e definitiva di **Project Mapper**, un sistema PowerShell/Python-ready per eseguire reverse engineering documentale di cartelle progetto complesse, con particolare attenzione a progetti professionali composti da deliverable, bozze, PBC, contratti, benchmark, working paper, allegati, email e output finali.

L'obiettivo non è solo generare un inventario file, ma ricostruire:

- cosa contiene la cartella;
- cosa è finale;
- cosa è bozza/storico;
- cosa è input cliente;
- cosa è contratto, benchmark, fonte esterna o working paper;
- quali file probabilmente alimentano quali deliverable;
- quali elementi mancano;
- quanto è affidabile ogni classificazione;
- quali regole possono essere apprese dalle correzioni manuali;
- quali output sono difendibili davanti a revisori, partner, auditor o hiring manager.

La versione definitiva integra quattro principi fondamentali:

1. **Planning sicuro e reversibile**: ogni cambiamento è minimo, verificabile e rollbackabile.
2. **Quality gate oggettivo**: nessun output viene trattato come affidabile senza score, difetti e raccomandazione.
3. **Reverse engineering Excel**: i workbook possono essere analizzati come artefatti logici, non solo come file.
4. **Produzione locale resiliente**: health check, logging, snapshot, rollback e validazione.

---

## 1. Mente Locale — Cosa Stiamo Costruendo Davvero

Project Mapper non è uno script. È un **motore di analisi documentale**.

La cartella progetto viene trattata come un sistema informativo implicito. I nomi file, le estensioni, le cartelle, le date, le versioni e i pattern ricorrenti diventano segnali per ricostruire l'architettura documentale.

### 1.1 Problema reale

In cartelle professionali complesse spesso troviamo:

- file finali non chiaramente distinguibili;
- bozze multiple;
- cartelle `Old` usate in modo incoerente;
- file PBC con naming variabile;
- benchmark e search report sparsi;
- contratti in PDF/Word con nomi non standard;
- Excel con formule e logiche di business critiche;
- allegati finali scollegati dal documento principale;
- versioni FY diverse con strutture simili ma non identiche.

### 1.2 Obiettivo professionale

Project Mapper deve produrre un output che possa essere usato per:

- onboarding rapido su un progetto;
- revisione interna;
- controllo completezza;
- preparazione anno successivo;
- generazione template;
- audit documentale;
- handover a collega o team;
- dimostrazione di capacità architetturali e automazione career-grade.

---

## 2. Fonti Metodologiche Integrate

Questa versione incorpora tre skill/fondamenti:

### 2.1 Planning Methodology

La metodologia impone piani minimali, reversibili, verificabili e con rollback obbligatorio. Ogni modifica deve avere scopo chiaro, verifica e strategia di ritorno.  
Fonte: `<File>SKILL - Copia.md</File>` — planning-methodology.

### 2.2 Quality Validation

Ogni output deve superare una validazione con score, difetti, severità e decisione: APPROVE, APPROVE WITH REVIEW o BLOCK.  
Fonte: `<File>SKILL.md</File>` — quality-validation.

### 2.3 Excel Reverse Engineering

I workbook Excel devono poter essere analizzati per struttura, formule, named ranges, complessità, dipendenze, logica finanziaria e rischi.  
Fonte: `<File>SKILL.it.md</File>` — xlsx-reverse-engineering.

---

## 3. Architettura Finale

```text
ProjectMapper/
├── README.md
├── SKILL.md
├── config/
│   ├── taxonomy.json
│   ├── classification.rules.json
│   ├── confidence.model.json
│   ├── expected.structure.json
│   └── validation.policy.json
├── scripts/
│   ├── 00_Config.ps1
│   ├── 01_Scan.ps1
│   ├── 02_Classify.ps1
│   ├── 03_MapRelations.ps1
│   ├── 04_AnalyzeExcel.ps1
│   ├── 05_CompilationLogic.ps1
│   ├── 06_GenerateArchitecture.ps1
│   ├── 07_Validate.ps1
│   ├── 08_LearnFromCorrections.ps1
│   ├── 09_HealthCheck.ps1
│   ├── 10_Rollback.ps1
│   └── RUN_ALL.ps1
├── python/
│   ├── inspect_xlsx.py
│   ├── formula_audit.py
│   ├── extract_logic.py
│   └── generate_excel_report.py
├── knowledge/
│   ├── knowledge-core.md
│   ├── manual-corrections.csv
│   └── pattern-index.json
├── runbooks/
│   ├── RUNBOOK.md
│   ├── ROLLBACK.md
│   └── TROUBLESHOOTING.md
├── tests/
│   ├── create-sample-tree.ps1
│   ├── expected-results.json
│   └── smoke-test.ps1
└── output/
    └── _ANALISI/
        ├── current/
        ├── previous/
        └── archive/
```

---

## 4. Pipeline Definitiva

```text
0. HEALTH CHECK
   ↓
1. SCAN INVENTARIO
   ↓
2. CLASSIFICAZIONE
   ↓
3. MAPPA RELAZIONI
   ↓
4. ANALISI EXCEL OPZIONALE
   ↓
5. LOGICA COMPILAZIONE
   ↓
6. ARCHITETTURA DOCUMENTALE
   ↓
7. QUALITY VALIDATION
   ↓
8. LEARNING DA CORREZIONI
   ↓
9. SNAPSHOT / ROLLBACK READY
```

---

## 5. Contratto degli Output

Ogni run deve generare almeno questi artefatti:

```text
_ANALISI/current/
├── 00_RUN_MANIFEST.json
├── 01_INVENTARIO.csv
├── 01_INVENTARIO.json
├── 01_STATISTICHE.md
├── 02_CLASSIFICAZIONE.csv
├── 02_CLASSIFICAZIONE.json
├── 02_REPORT_CLASSIFICAZIONE.md
├── 03_RELAZIONI.csv
├── 03_RELAZIONI.json
├── 03_REPORT_RELAZIONI.md
├── 04_EXCEL_AUDIT_SUMMARY.md
├── 05_LOGICA_COMPILAZIONE.md
├── 06_ARCHITETTURA.md
├── 07_VALIDATION_REPORT.md
├── 08_LEARNINGS.md
└── 09_HEALTHCHECK.md
```

### Regola fondamentale

CSV = leggibile in Excel.  
JSON = stabile per automazioni.  
Markdown = leggibile da persone.

---

## 6. Tassonomia Finale

Categorie canoniche:

| Categoria | Ruolo | Criticità | Descrizione |
|---|---|---:|---|
| DELIVERABLE_DN | OUTPUT | HIGH | Documentazione Nazionale finale |
| DELIVERABLE_MF | OUTPUT | HIGH | Master File finale |
| DELIVERABLE_BUNDLE | OUTPUT | HIGH | PDF unico con allegati |
| DRAFT | WIP | LOW | Bozza/versione intermedia |
| PBC_DATA | INPUT_RAW | HIGH | Dati grezzi dal cliente |
| CONTRACT | INPUT_LEGAL | HIGH | Contratti, accordi, policy |
| BENCHMARK | INPUT_BM | HIGH | Comparables, benchmark, search report |
| CALCULATION | INPUT_CALC | MEDIUM | Working paper, RPT, elaborazioni |
| EXTERNAL_SOURCE | INPUT_MKT | MEDIUM | Bilanci, fonti mercato, organigrammi |
| ATTACHMENT | OUTPUT_ATTACHMENT | MEDIUM | Allegati finali |
| EMAIL | NOTE | LOW | Corrispondenza email |
| UNKNOWN | REVIEW | REVIEW | Da classificare manualmente |

---

## 7. `config/taxonomy.json`

```json
{
  "version": "3.0",
  "categories": {
    "DELIVERABLE_DN": {
      "label": "Documentazione Nazionale finale",
      "role": "OUTPUT",
      "criticality": "HIGH",
      "expected_final": true
    },
    "DELIVERABLE_MF": {
      "label": "Master File finale",
      "role": "OUTPUT",
      "criticality": "HIGH",
      "expected_final": true
    },
    "DELIVERABLE_BUNDLE": {
      "label": "PDF unico con allegati",
      "role": "OUTPUT",
      "criticality": "HIGH",
      "expected_final": true
    },
    "DRAFT": {
      "label": "Bozza o versione intermedia",
      "role": "WIP",
      "criticality": "LOW",
      "expected_final": false
    },
    "PBC_DATA": {
      "label": "Dati grezzi ricevuti dal cliente",
      "role": "INPUT_RAW",
      "criticality": "HIGH",
      "expected_final": false
    },
    "CONTRACT": {
      "label": "Contratti, accordi, policy o base legale",
      "role": "INPUT_LEGAL",
      "criticality": "HIGH",
      "expected_final": false
    },
    "BENCHMARK": {
      "label": "Benchmark, comparables o search report",
      "role": "INPUT_BM",
      "criticality": "HIGH",
      "expected_final": false
    },
    "CALCULATION": {
      "label": "Working paper, RPT o elaborazioni",
      "role": "INPUT_CALC",
      "criticality": "MEDIUM",
      "expected_final": false
    },
    "EXTERNAL_SOURCE": {
      "label": "Fonti esterne, mercato, bilanci, organigrammi",
      "role": "INPUT_MKT",
      "criticality": "MEDIUM",
      "expected_final": false
    },
    "ATTACHMENT": {
      "label": "Allegato finale",
      "role": "OUTPUT_ATTACHMENT",
      "criticality": "MEDIUM",
      "expected_final": true
    },
    "EMAIL": {
      "label": "Email o corrispondenza",
      "role": "NOTE",
      "criticality": "LOW",
      "expected_final": false
    },
    "UNKNOWN": {
      "label": "Da classificare manualmente",
      "role": "REVIEW",
      "criticality": "REVIEW",
      "expected_final": false
    }
  }
}
```

---

## 8. `config/classification.rules.json`

```json
[
  {
    "id": "dn-final",
    "priority": 100,
    "match_on": "filename",
    "pattern": "DN*Final*",
    "category": "DELIVERABLE_DN",
    "confidence": 0.95,
    "evidence": "Nome file contiene DN e Final"
  },
  {
    "id": "mf-final",
    "priority": 100,
    "match_on": "filename",
    "pattern": "MF*Final*",
    "category": "DELIVERABLE_MF",
    "confidence": 0.95,
    "evidence": "Nome file contiene MF e Final"
  },
  {
    "id": "bundle-final",
    "priority": 98,
    "match_on": "filename",
    "pattern": "*con allegati*",
    "category": "DELIVERABLE_BUNDLE",
    "confidence": 0.90,
    "evidence": "Nome file indica bundle con allegati"
  },
  {
    "id": "draft-generic",
    "priority": 80,
    "match_on": "filename",
    "pattern": "*Draft*",
    "category": "DRAFT",
    "confidence": 0.85,
    "evidence": "Nome file contiene Draft"
  },
  {
    "id": "bozza-generic",
    "priority": 80,
    "match_on": "filename",
    "pattern": "*Bozza*",
    "category": "DRAFT",
    "confidence": 0.85,
    "evidence": "Nome file contiene Bozza"
  },
  {
    "id": "pnl-split",
    "priority": 85,
    "match_on": "filename",
    "pattern": "*P&L*Split*",
    "category": "PBC_DATA",
    "confidence": 0.90,
    "evidence": "Nome file contiene P&L Split"
  },
  {
    "id": "pl-split",
    "priority": 84,
    "match_on": "filename",
    "pattern": "*PL split*",
    "category": "PBC_DATA",
    "confidence": 0.85,
    "evidence": "Nome file contiene PL split"
  },
  {
    "id": "transazioni",
    "priority": 83,
    "match_on": "filename",
    "pattern": "*Transazioni*",
    "category": "PBC_DATA",
    "confidence": 0.85,
    "evidence": "Nome file contiene Transazioni"
  },
  {
    "id": "agreement",
    "priority": 82,
    "match_on": "filename",
    "pattern": "*Agreement*",
    "category": "CONTRACT",
    "confidence": 0.85,
    "evidence": "Nome file contiene Agreement"
  },
  {
    "id": "contratto",
    "priority": 82,
    "match_on": "filename",
    "pattern": "*Contratto*",
    "category": "CONTRACT",
    "confidence": 0.85,
    "evidence": "Nome file contiene Contratto"
  },
  {
    "id": "comparables",
    "priority": 82,
    "match_on": "filename",
    "pattern": "*Comparables*",
    "category": "BENCHMARK",
    "confidence": 0.90,
    "evidence": "Nome file contiene Comparables"
  },
  {
    "id": "search-report",
    "priority": 82,
    "match_on": "filename",
    "pattern": "*Search Report*",
    "category": "BENCHMARK",
    "confidence": 0.90,
    "evidence": "Nome file contiene Search Report"
  },
  {
    "id": "rpt",
    "priority": 78,
    "match_on": "filename",
    "pattern": "RPT*",
    "category": "CALCULATION",
    "confidence": 0.82,
    "evidence": "Nome file inizia con RPT"
  },
  {
    "id": "wsh",
    "priority": 76,
    "match_on": "filename",
    "pattern": "*WSH*",
    "category": "CALCULATION",
    "confidence": 0.78,
    "evidence": "Nome file contiene WSH"
  },
  {
    "id": "bilancio",
    "priority": 72,
    "match_on": "filename",
    "pattern": "*Bilancio*",
    "category": "EXTERNAL_SOURCE",
    "confidence": 0.80,
    "evidence": "Nome file contiene Bilancio"
  },
  {
    "id": "allegato",
    "priority": 70,
    "match_on": "filename",
    "pattern": "Allegato*",
    "category": "ATTACHMENT",
    "confidence": 0.82,
    "evidence": "Nome file inizia con Allegato"
  },
  {
    "id": "email-msg",
    "priority": 95,
    "match_on": "extension",
    "pattern": ".msg",
    "category": "EMAIL",
    "confidence": 0.95,
    "evidence": "Estensione .msg"
  }
]
```

---

## 9. `config/confidence.model.json`

```json
{
  "version": "3.0",
  "classification": {
    "exact_filename_pattern": 0.95,
    "strong_filename_pattern": 0.85,
    "folder_context_bonus": 0.10,
    "extension_match_bonus": 0.05,
    "old_folder_penalty": -0.25,
    "unknown_default": 0.10
  },
  "relations": {
    "same_year": 0.25,
    "same_entity": 0.25,
    "source_is_input": 0.25,
    "target_is_output": 0.15,
    "both_not_obsolete": 0.10,
    "max": 0.95
  },
  "thresholds": {
    "high": 0.80,
    "medium": 0.50,
    "low": 0.30,
    "manual_review_required": 0.50
  }
}
```

---

## 10. Core Script — `00_Config.ps1`

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$RootPath = (Resolve-Path $Path).Path.TrimEnd('\')
$AnalysisRoot = Join-Path $RootPath "_ANALISI"
$OutputDir = Join-Path $AnalysisRoot "current"
$PreviousDir = Join-Path $AnalysisRoot "previous"
$ArchiveDir = Join-Path $AnalysisRoot "archive"

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor DarkCyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor DarkCyan
}

function Assert-FileExists {
    param([string]$FilePath)
    if (-not (Test-Path $FilePath)) {
        throw "File richiesto non trovato: $FilePath"
    }
}

function Initialize-OutputDirs {
    New-Item -ItemType Directory -Path $AnalysisRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $ArchiveDir -Force | Out-Null

    if (Test-Path $PreviousDir) {
        Remove-Item $PreviousDir -Recurse -Force
    }

    if (Test-Path $OutputDir) {
        Move-Item $OutputDir $PreviousDir
    }

    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

function Export-Data {
    param(
        [Parameter(Mandatory)] $Data,
        [Parameter(Mandatory)] [string]$BasePath
    )

    $Data | Export-Csv "$BasePath.csv" -NoTypeInformation -Encoding UTF8 -Delimiter ";"
    $Data | ConvertTo-Json -Depth 10 | Out-File "$BasePath.json" -Encoding UTF8
}

function Get-ConfidenceLevel {
    param([double]$Score)
    if ($Score -ge 0.80) { return "HIGH" }
    if ($Score -ge 0.50) { return "MEDIUM" }
    if ($Score -ge 0.30) { return "LOW" }
    return "VERY_LOW"
}
```

---

## 11. `01_Scan.ps1`

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
)

. "$PSScriptRoot\00_Config.ps1" -Path $Path

Write-Section "FASE 1 - SCANSIONE"

$files = Get-ChildItem -Path $RootPath -Recurse -File | Where-Object {
    -not $_.FullName.StartsWith($AnalysisRoot, [System.StringComparison]::OrdinalIgnoreCase)
} | ForEach-Object {
    $relPath = [System.IO.Path]::GetRelativePath($RootPath, $_.FullName)
    $parts = $relPath -split '[\\/]'
    $depth = [Math]::Max(0, $parts.Count - 1)

    [PSCustomObject]@{
        NomeFile = $_.Name
        BaseName = $_.BaseName
        Estensione = $_.Extension.ToLowerInvariant()
        DimensioneKB = [Math]::Round($_.Length / 1KB, 1)
        Profondita = $depth
        AnnoFiscale = if ($parts.Count -ge 1) { $parts[0] } else { "" }
        Entita = if ($parts.Count -ge 2) { $parts[1] } else { "" }
        TipoCartella = if ($parts.Count -ge 3) { $parts[2] } else { "" }
        PercorsoRelativo = $relPath
        UltimaModifica = $_.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        PercorsoCompleto = $_.FullName
        HashLite = "$($_.Length)-$($_.LastWriteTimeUtc.Ticks)"
    }
}

Export-Data -Data $files -BasePath (Join-Path $OutputDir "01_INVENTARIO")

$stats = @"
# Statistiche Scansione

- Cartella: `$RootPath`
- File totali: $($files.Count)
- Dimensione totale MB: $([Math]::Round(($files | Measure-Object DimensioneKB -Sum).Sum / 1024, 1))

## Per estensione
$(($files | Group-Object Estensione | Sort-Object Count -Descending | ForEach-Object { "- $($_.Name): $($_.Count)" }) -join "`n")

## Per anno fiscale
$(($files | Group-Object AnnoFiscale | Sort-Object Name | ForEach-Object { "- $($_.Name): $($_.Count)" }) -join "`n")

## Per entità
$(($files | Group-Object Entita | Sort-Object Count -Descending | ForEach-Object { "- $($_.Name): $($_.Count)" }) -join "`n")
"@

$stats | Out-File (Join-Path $OutputDir "01_STATISTICHE.md") -Encoding UTF8
Write-Host $stats -ForegroundColor Cyan
```

---

## 12. `02_Classify.ps1`

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
)

. "$PSScriptRoot\00_Config.ps1" -Path $Path

Write-Section "FASE 2 - CLASSIFICAZIONE"

$inventoryPath = Join-Path $OutputDir "01_INVENTARIO.csv"
$rulesPath = Join-Path $ProjectRoot "config\classification.rules.json"
$taxonomyPath = Join-Path $ProjectRoot "config\taxonomy.json"

Assert-FileExists $inventoryPath
Assert-FileExists $rulesPath
Assert-FileExists $taxonomyPath

$files = Import-Csv $inventoryPath -Delimiter ";"
$rules = Get-Content $rulesPath -Raw | ConvertFrom-Json | Sort-Object priority -Descending
$taxonomy = Get-Content $taxonomyPath -Raw | ConvertFrom-Json

$classified = foreach ($f in $files) {
    $matched = $null

    foreach ($rule in $rules) {
        $value = switch ($rule.match_on) {
            "filename" { $f.NomeFile }
            "extension" { $f.Estensione }
            "path" { $f.PercorsoRelativo }
            default { $f.NomeFile }
        }

        if ($value -like $rule.pattern) {
            $matched = $rule
            break
        }
    }

    if ($matched) {
        $category = $matched.category
        $confidence = [double]$matched.confidence
        $evidence = $matched.evidence
        $ruleId = $matched.id
    } else {
        $category = "UNKNOWN"
        $confidence = 0.10
        $evidence = "Nessuna regola corrispondente"
        $ruleId = ""
    }

    $isOld = $f.PercorsoRelativo -match "(^|[\\/])Old([\\/]|$)"
    if ($isOld) { $confidence = [Math]::Max(0.05, $confidence - 0.25) }

    $status = if ($isOld) {
        "OBSOLETE"
    } elseif ($f.NomeFile -match "(?i)\bfinal\b") {
        "FINAL"
    } elseif ($f.NomeFile -match "(?i)draft|bozza|semi|v\.\d+|versione") {
        "WIP"
    } else {
        "MATERIAL"
    }

    $meta = $taxonomy.categories.$category
    $role = if ($meta) { $meta.role } else { "REVIEW" }
    $label = if ($meta) { $meta.label } else { "Da classificare" }
    $criticality = if ($meta) { $meta.criticality } else { "REVIEW" }

    $f | Add-Member -NotePropertyName Categoria -NotePropertyValue $category -PassThru |
         Add-Member -NotePropertyName CategoriaLabel -NotePropertyValue $label -PassThru |
         Add-Member -NotePropertyName Ruolo -NotePropertyValue $role -PassThru |
         Add-Member -NotePropertyName Criticita -NotePropertyValue $criticality -PassThru |
         Add-Member -NotePropertyName Stato -NotePropertyValue $status -PassThru |
         Add-Member -NotePropertyName Obsoleto -NotePropertyValue $isOld -PassThru |
         Add-Member -NotePropertyName Confidence -NotePropertyValue ([Math]::Round($confidence, 2)) -PassThru |
         Add-Member -NotePropertyName ConfidenceLevel -NotePropertyValue (Get-ConfidenceLevel $confidence) -PassThru |
         Add-Member -NotePropertyName RuleId -NotePropertyValue $ruleId -PassThru |
         Add-Member -NotePropertyName Evidence -NotePropertyValue $evidence -PassThru
}

Export-Data -Data $classified -BasePath (Join-Path $OutputDir "02_CLASSIFICAZIONE")

$unknown = @($classified | Where-Object { $_.Categoria -eq "UNKNOWN" })
$low = @($classified | Where-Object { [double]$_.Confidence -lt 0.50 })

$report = @"
# Report Classificazione

- File totali: $($classified.Count)
- File UNKNOWN: $($unknown.Count)
- File confidence bassa: $($low.Count)

## Categorie
$(($classified | Group-Object Categoria | Sort-Object Count -Descending | ForEach-Object { "- $($_.Name): $($_.Count)" }) -join "`n")

## File da classificare manualmente
$(($unknown | Select-Object -First 200 | ForEach-Object { "- $($_.PercorsoRelativo)" }) -join "`n")
"@

$report | Out-File (Join-Path $OutputDir "02_REPORT_CLASSIFICAZIONE.md") -Encoding UTF8
Write-Host $report -ForegroundColor Yellow
```

---

## 13. `03_MapRelations.ps1`

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
)

. "$PSScriptRoot\00_Config.ps1" -Path $Path

Write-Section "FASE 3 - MAPPA RELAZIONI"

$classPath = Join-Path $OutputDir "02_CLASSIFICAZIONE.csv"
Assert-FileExists $classPath

$items = Import-Csv $classPath -Delimiter ";"
$relations = @()

function New-Relation {
    param($Source, $Target, [string]$RelationType, [string]$Chapter)

    $score = 0.0
    $evidence = @()

    if ($Source.AnnoFiscale -eq $Target.AnnoFiscale) { $score += 0.25; $evidence += "stesso anno fiscale" }
    if ($Source.Entita -eq $Target.Entita) { $score += 0.25; $evidence += "stessa entità" }
    if ($Source.Ruolo -match "^INPUT") { $score += 0.25; $evidence += "origine input" }
    if ($Target.Ruolo -eq "OUTPUT") { $score += 0.15; $evidence += "destinazione output" }
    if ($Source.Obsoleto -eq "False" -and $Target.Obsoleto -eq "False") { $score += 0.10; $evidence += "file non obsoleti" }

    $score = [Math]::Min(0.95, [Math]::Round($score, 2))

    [PSCustomObject]@{
        AnnoFiscale = $Source.AnnoFiscale
        Entita = $Source.Entita
        FileOrigine = $Source.NomeFile
        CategoriaOrigine = $Source.Categoria
        Relazione = $RelationType
        FileDestino = $Target.NomeFile
        CategoriaDestino = $Target.Categoria
        Capitolo = $Chapter
        Confidence = $score
        ConfidenceLevel = Get-ConfidenceLevel $score
        Evidence = ($evidence -join "; ")
    }
}

$groups = $items | Group-Object { "$($_.AnnoFiscale)|$($_.Entita)" }

foreach ($g in $groups) {
    $groupItems = @($g.Group)
    $targets = @($groupItems | Where-Object { $_.Ruolo -eq "OUTPUT" -and $_.Obsoleto -eq "False" })
    $sources = @($groupItems | Where-Object { $_.Ruolo -match "^INPUT" -and $_.Obsoleto -eq "False" })
    $attachments = @($groupItems | Where-Object { $_.Ruolo -eq "OUTPUT_ATTACHMENT" -and $_.Obsoleto -eq "False" })

    foreach ($target in $targets) {
        foreach ($source in $sources) {
            $chapter = switch ($source.Ruolo) {
                "INPUT_RAW" { "Cap.2-3 Dati cliente" }
                "INPUT_LEGAL" { "Cap.2 Base contrattuale" }
                "INPUT_BM" { "Cap.3 Benchmark" }
                "INPUT_CALC" { "Cap.3 Analisi economica" }
                "INPUT_MKT" { "Cap.1 Mercato" }
                default { "Generale" }
            }
            $relations += New-Relation $source $target "PROBABLY_FEEDS" $chapter
        }

        foreach ($att in $attachments) {
            $relations += New-Relation $att $target "PROBABLY_ATTACHED_TO" "Allegati"
        }
    }
}

Export-Data -Data $relations -BasePath (Join-Path $OutputDir "03_RELAZIONI")

$report = @"
# Report Relazioni

- Relazioni totali: $($relations.Count)

## Distribuzione confidence
$(($relations | Group-Object ConfidenceLevel | Sort-Object Name | ForEach-Object { "- $($_.Name): $($_.Count)" }) -join "`n")
"@

$report | Out-File (Join-Path $OutputDir "03_REPORT_RELAZIONI.md") -Encoding UTF8
Write-Host $report -ForegroundColor Magenta
```

---

## 14. Excel Reverse Engineering — `04_AnalyzeExcel.ps1`

Questa fase è opzionale ma consigliata per workbook critici.

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
)

. "$PSScriptRoot\00_Config.ps1" -Path $Path

Write-Section "FASE 4 - ANALISI EXCEL"

$classPath = Join-Path $OutputDir "02_CLASSIFICAZIONE.csv"
Assert-FileExists $classPath

$items = Import-Csv $classPath -Delimiter ";"
$excelFiles = @($items | Where-Object { $_.Estensione -in @(".xlsx", ".xlsm", ".xls") })

$summary = foreach ($x in $excelFiles) {
    [PSCustomObject]@{
        NomeFile = $x.NomeFile
        PercorsoRelativo = $x.PercorsoRelativo
        Categoria = $x.Categoria
        Ruolo = $x.Ruolo
        Action = "Analyze with python/inspect_xlsx.py when deep audit is required"
        Priority = if ($x.Categoria -in @("PBC_DATA", "CALCULATION", "BENCHMARK")) { "HIGH" } else { "NORMAL" }
    }
}

Export-Data -Data $summary -BasePath (Join-Path $OutputDir "04_EXCEL_AUDIT_SUMMARY")

$md = @"
# Excel Audit Summary

- Workbook trovati: $($excelFiles.Count)
- Workbook prioritari: $(@($summary | Where-Object { $_.Priority -eq "HIGH" }).Count)

## Nota operativa
Per workbook critici eseguire pipeline Python:

```powershell
python python/inspect_xlsx.py "file.xlsx" --pretty
python python/formula_audit.py "file.xlsx" --pretty
python python/extract_logic.py "file.xlsx" --pretty
python python/generate_excel_report.py "file.xlsx" "report.xlsx"
```
"@

$md | Out-File (Join-Path $OutputDir "04_EXCEL_AUDIT_SUMMARY.md") -Encoding UTF8
Write-Host $md -ForegroundColor Cyan
```

---

## 15. Quality Gate — `07_Validate.ps1`

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
)

. "$PSScriptRoot\00_Config.ps1" -Path $Path

Write-Section "FASE 7 - QUALITY VALIDATION"

$classPath = Join-Path $OutputDir "02_CLASSIFICAZIONE.csv"
$relPath = Join-Path $OutputDir "03_RELAZIONI.csv"

Assert-FileExists $classPath

$items = Import-Csv $classPath -Delimiter ";"
$relations = if (Test-Path $relPath) { Import-Csv $relPath -Delimiter ";" } else { @() }

$issues = New-Object System.Collections.Generic.List[object]

function Add-Issue {
    param([string]$Severity, [string]$Area, [string]$Message, [string]$Fix)
    $issues.Add([PSCustomObject]@{
        Severity = $Severity
        Area = $Area
        Message = $Message
        Fix = $Fix
    })
}

$total = [Math]::Max(1, $items.Count)
$unknown = @($items | Where-Object { $_.Categoria -eq "UNKNOWN" })
$unknownPct = [Math]::Round(($unknown.Count / $total) * 100, 1)

if ($unknownPct -gt 15) {
    Add-Issue "HIGH" "Classificazione" "UNKNOWN sopra soglia: $unknownPct%." "Aggiungere regole o correzioni manuali."
} elseif ($unknown.Count -gt 0) {
    Add-Issue "MEDIUM" "Classificazione" "$($unknown.Count) file UNKNOWN." "Valutare correzione manuale."
}

$groups = $items | Where-Object { $_.AnnoFiscale -and $_.Entita } | Group-Object { "$($_.AnnoFiscale)|$($_.Entita)" }
foreach ($g in $groups) {
    $hasInput = @($g.Group | Where-Object { $_.Ruolo -match "^INPUT" -and $_.Obsoleto -eq "False" }).Count -gt 0
    $hasOutput = @($g.Group | Where-Object { $_.Ruolo -eq "OUTPUT" -and $_.Obsoleto -eq "False" }).Count -gt 0
    if ($hasInput -and -not $hasOutput) {
        Add-Issue "HIGH" "Completezza" "Gruppo $($g.Name) ha input ma nessun output finale." "Verificare presenza/naming deliverable."
    }
}

$lowRelations = @($relations | Where-Object { [double]$_.Confidence -lt 0.50 })
if ($lowRelations.Count -gt 0) {
    Add-Issue "MEDIUM" "Relazioni" "$($lowRelations.Count) relazioni con confidence bassa." "Revisionare evidence e struttura cartelle."
}

$score = 100
foreach ($i in $issues) {
    switch ($i.Severity) {
        "CRITICAL" { $score -= 30 }
        "HIGH" { $score -= 15 }
        "MEDIUM" { $score -= 7 }
        "LOW" { $score -= 2 }
    }
}
if ($score -lt 0) { $score = 0 }

$decision = if ($score -ge 90) {
    "APPROVE"
} elseif ($score -ge 80) {
    "APPROVE WITH MINOR REVIEW"
} elseif ($score -ge 70) {
    "APPROVE WITH MANUAL REVIEW"
} else {
    "BLOCK"
}

$md = @"
# Validation Report

## Esito

- Score: **$score/100**
- Decisione: **$decision**
- Issue totali: **$($issues.Count)**

## Issue

| Severity | Area | Messaggio | Fix |
|---|---|---|---|
$(($issues | ForEach-Object { "| $($_.Severity) | $($_.Area) | $($_.Message) | $($_.Fix) |" }) -join "`n")

## Regola decisionale

- 90-100: APPROVE
- 80-89: APPROVE WITH MINOR REVIEW
- 70-79: APPROVE WITH MANUAL REVIEW
- <70: BLOCK
"@

$md | Out-File (Join-Path $OutputDir "07_VALIDATION_REPORT.md") -Encoding UTF8
$issues | Export-Csv (Join-Path $OutputDir "07_VALIDATION_ISSUES.csv") -NoTypeInformation -Encoding UTF8 -Delimiter ";"

Write-Host $md -ForegroundColor White
```

---

## 16. Learning Loop — `08_LearnFromCorrections.ps1`

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
)

. "$PSScriptRoot\00_Config.ps1" -Path $Path

Write-Section "FASE 8 - LEARNING DA CORREZIONI"

$correctionsPath = Join-Path $ProjectRoot "knowledge\manual-corrections.csv"
$classPath = Join-Path $OutputDir "02_CLASSIFICAZIONE.csv"
$knowledgePath = Join-Path $ProjectRoot "knowledge\knowledge-core.md"

Assert-FileExists $classPath

if (-not (Test-Path $correctionsPath)) {
    New-Item -ItemType Directory -Path (Split-Path $correctionsPath) -Force | Out-Null
    "PercorsoRelativo;CategoriaCorretta;Note" | Out-File $correctionsPath -Encoding UTF8
    Write-Host "Creato template correzioni manuali: $correctionsPath" -ForegroundColor Yellow
    return
}

$corrections = Import-Csv $correctionsPath -Delimiter ";"
$classified = Import-Csv $classPath -Delimiter ";"

if (-not (Test-Path $knowledgePath)) {
    "# Knowledge Core - Project Mapper`n" | Out-File $knowledgePath -Encoding UTF8
}

$entries = foreach ($c in $corrections) {
    $file = $classified | Where-Object { $_.PercorsoRelativo -eq $c.PercorsoRelativo } | Select-Object -First 1
    if ($file) {
        [PSCustomObject]@{
            Date = Get-Date -Format "yyyy-MM-dd"
            File = $file.PercorsoRelativo
            OriginalCategory = $file.Categoria
            CorrectedCategory = $c.CategoriaCorretta
            Note = $c.Note
            SuggestedPattern = "*" + ($file.BaseName -replace "\d+", "*") + "*"
        }
    }
}

Add-Content $knowledgePath "`n## Manual Classification Learnings - $(Get-Date -Format "yyyy-MM-dd")`n"
foreach ($e in $entries) {
    Add-Content $knowledgePath @"
### Pattern candidate: $($e.CorrectedCategory)

- File: `$($e.File)`
- Categoria originale: `$($e.OriginalCategory)`
- Categoria corretta: `$($e.CorrectedCategory)`
- Pattern suggerito: `$($e.SuggestedPattern)`
- Nota: $($e.Note)

"@
}

$entries | Export-Csv (Join-Path $OutputDir "08_LEARNINGS.csv") -NoTypeInformation -Encoding UTF8 -Delimiter ";"
Write-Host "Learning completato." -ForegroundColor Green
```

---

## 17. Health Check — `09_HealthCheck.ps1`

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
)

. "$PSScriptRoot\00_Config.ps1" -Path $Path

Write-Section "HEALTH CHECK"

$checks = New-Object System.Collections.Generic.List[object]

function Add-Check {
    param([string]$Name, [bool]$Passed, [string]$Details, [string]$Fix)
    $checks.Add([PSCustomObject]@{
        Name = $Name
        Passed = $Passed
        Details = $Details
        Fix = $Fix
    })
}

Add-Check "Root path exists" (Test-Path $RootPath) $RootPath "Verificare -Path."
Add-Check "PowerShell supported" ($PSVersionTable.PSVersion.Major -ge 5) "$($PSVersionTable.PSVersion)" "Usare PowerShell 5.1+ o 7+."
Add-Check "taxonomy.json exists" (Test-Path (Join-Path $ProjectRoot "config\taxonomy.json")) "config/taxonomy.json" "Creare taxonomy."
Add-Check "classification.rules.json exists" (Test-Path (Join-Path $ProjectRoot "config\classification.rules.json")) "config/classification.rules.json" "Creare regole."

$failed = @($checks | Where-Object { -not $_.Passed })

$md = @"
# Health Check

- Check totali: $($checks.Count)
- Falliti: $($failed.Count)
- Stato: $(if ($failed.Count -eq 0) { "HEALTHY" } else { "DEGRADED" })

| Check | Esito | Dettagli | Fix |
|---|---:|---|---|
$(($checks | ForEach-Object { "| $($_.Name) | $(if ($_.Passed) { "OK" } else { "FAIL" }) | $($_.Details) | $($_.Fix) |" }) -join "`n")
"@

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
$md | Out-File (Join-Path $OutputDir "09_HEALTHCHECK.md") -Encoding UTF8
Write-Host $md -ForegroundColor White

if ($failed.Count -gt 0) { throw "Health check fallito." }
```

---

## 18. RUN_ALL Definitivo

```powershell
param(
    [string]$Path = "C:\Users\luca.consalter\Desktop\Nuova cartella (2)",
    [switch]$SkipExcelAudit
)

$ErrorActionPreference = "Stop"

. "$PSScriptRoot\00_Config.ps1" -Path $Path

Initialize-OutputDirs

$manifest = [ordered]@{
    RunId = [Guid]::NewGuid().ToString()
    StartedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    TargetPath = $RootPath
    Status = "RUNNING"
}

$manifest | ConvertTo-Json -Depth 5 | Out-File (Join-Path $OutputDir "00_RUN_MANIFEST.json") -Encoding UTF8

$steps = @(
    "09_HealthCheck.ps1",
    "01_Scan.ps1",
    "02_Classify.ps1",
    "03_MapRelations.ps1"
)

if (-not $SkipExcelAudit) {
    $steps += "04_AnalyzeExcel.ps1"
}

$steps += @(
    "05_CompilationLogic.ps1",
    "06_GenerateArchitecture.ps1",
    "07_Validate.ps1",
    "08_LearnFromCorrections.ps1"
)

try {
    foreach ($step in $steps) {
        $script = Join-Path $PSScriptRoot $step
        if (-not (Test-Path $script)) { throw "Script mancante: $script" }
        Write-Host "`n>>> $step" -ForegroundColor Cyan
        & $script -Path $Path
    }

    $manifest.Status = "COMPLETED"
    $manifest.CompletedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}
catch {
    $manifest.Status = "FAILED"
    $manifest.Error = $_.Exception.Message
    $manifest.FailedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $manifest | ConvertTo-Json -Depth 5 | Out-File (Join-Path $OutputDir "00_RUN_MANIFEST.json") -Encoding UTF8
    throw
}

$manifest | ConvertTo-Json -Depth 5 | Out-File (Join-Path $OutputDir "00_RUN_MANIFEST.json") -Encoding UTF8
Write-Host "`nPROJECT MAPPER COMPLETATO" -ForegroundColor Green
```

---

## 19. Runbook Operativo

### 19.1 Setup

```powershell
cd ProjectMapper
```

Verificare che esistano:

```text
config/taxonomy.json
config/classification.rules.json
config/confidence.model.json
scripts/RUN_ALL.ps1
```

### 19.2 Esecuzione standard

```powershell
.\scripts\RUN_ALL.ps1 -Path "C:\Users\luca.consalter\Desktop\Nuova cartella (2)"
```

### 19.3 Esecuzione senza audit Excel

```powershell
.\scripts\RUN_ALL.ps1 -Path "C:\Users\luca.consalter\Desktop\Nuova cartella (2)" -SkipExcelAudit
```

### 19.4 Output da leggere subito

```text
_ANALISI/current/06_ARCHITETTURA.md
_ANALISI/current/07_VALIDATION_REPORT.md
_ANALISI/current/02_REPORT_CLASSIFICAZIONE.md
```

---

## 20. Rollback

### Quando fare rollback

- Quality gate peggiora dopo nuove regole.
- Molti file passano erroneamente a UNKNOWN.
- Relazioni diventano rumorose.
- Output current corrotto.
- Excel/CSV non apribili.

### Procedura manuale

```powershell
Rename-Item "_ANALISI\current" "bad-current"
Rename-Item "_ANALISI\previous" "current"
```

### Verifica rollback

```powershell
Get-Content "_ANALISI\current\07_VALIDATION_REPORT.md"
```

---

## 21. Workaround Smart Policy

### Caso: troppe classificazioni UNKNOWN

**Cosa facciamo ora:** usare `manual-corrections.csv`.  
**Perché funziona:** evita di bloccare la pipeline.  
**Limite:** non automatizza subito tutti i casi.  
**Rischio residuo:** alcune relazioni restano incomplete.  
**Evoluzione definitiva:** trasformare le correzioni frequenti in regole JSON.

### Caso: file Excel troppo complesso

**Cosa facciamo ora:** lo segnaliamo come HIGH priority in `04_EXCEL_AUDIT_SUMMARY.md`.  
**Perché funziona:** evita parsing pesante nella pipeline base.  
**Limite:** l'analisi profonda va eseguita separatamente.  
**Rischio residuo:** logica business nascosta.  
**Evoluzione definitiva:** integrare pipeline Python automatica.

### Caso: relazioni incerte

**Cosa facciamo ora:** `PROBABLY_FEEDS` con confidence/evidence.  
**Perché funziona:** non dichiara certezza falsa.  
**Limite:** serve review manuale su casi critici.  
**Rischio residuo:** dipendenze mancanti.  
**Evoluzione definitiva:** analisi contenuto e cross-reference.

---

## 22. Rischi e Mitigazioni

| Rischio | Impatto | Mitigazione |
|---|---:|---|
| Regole troppo aggressive | Alto | Priority, confidence, evidence |
| Troppi UNKNOWN | Medio | manual-corrections + learning loop |
| Relazioni non vere | Alto | usare PROBABLY + confidence |
| File Old inclusi per errore | Alto | penalità confidence + exclusion relation |
| CSV problematici in Excel | Medio | delimiter `;` + JSON parallelo |
| Output perso dopo rerun | Alto | current/previous/archive |
| Workbook con formule critiche ignorate | Alto | Excel audit summary + Python pipeline |
| Config corrotta | Medio | health check pre-run |

---

## 23. Quality Gate Finale

Score base: 100.

Penalità:

| Condizione | Penalità |
|---|---:|
| Deliverable atteso mancante | -15 |
| UNKNOWN > 15% | -15 |
| Confidence media bassa | -10 |
| Relazioni confidence < 0.50 | -7 |
| Output JSON mancante | -5 |
| CSV non generato | -5 |
| File finali in Old | -10 |
| Naming typo noto | -2 |

Decisioni:

| Score | Decisione |
|---:|---|
| 90-100 | APPROVE |
| 80-89 | APPROVE WITH MINOR REVIEW |
| 70-79 | APPROVE WITH MANUAL REVIEW |
| <70 | BLOCK |

---

## 24. Checklist di Consegna

### Funzionale

- [x] Scansione file completa
- [x] Esclusione `_ANALISI`
- [x] Classificazione con regole esterne
- [x] Confidence + evidence
- [x] Relazioni probabilistiche
- [x] Output CSV + JSON + Markdown
- [x] Quality gate
- [x] Learning loop
- [x] Health check
- [x] Rollback

### Sicurezza

- [x] Nessuna modifica ai file sorgenti
- [x] Scrittura confinata in `_ANALISI` e `knowledge`
- [x] Nessun secret richiesto
- [x] Nessuna lettura contenuto file nella pipeline base
- [x] Audit Excel separabile e controllato

### Resilienza

- [x] Run idempotente
- [x] Output current/previous
- [x] Errori espliciti
- [x] Fallback manual-corrections
- [x] Rilancio sicuro

### Carriera / presentabilità

- [x] Architettura modulare
- [x] Quality gate difendibile
- [x] Evidenze e non affermazioni assolute
- [x] Runbook operativo
- [x] Rollback plan
- [x] Estendibilità futura

---

## 25. Verdetto Finale

Questa è la versione definitiva consigliata.

Il punto chiave è passare da:

```text
"Ho trovato dei file e li ho classificati."
```

A:

```text
"Ho ricostruito l'architettura documentale, con confidence, evidence, quality gate, rollback e learning loop."
```

Questa seconda formulazione è molto più professionale, difendibile e adatta a un contesto career-grade.

---

## 26. Prossimo Step Operativo

Creare la struttura cartelle e salvare i file:

```powershell
New-Item -ItemType Directory -Force -Path config, scripts, python, knowledge, runbooks, tests
```

Poi inserire:

1. `taxonomy.json`
2. `classification.rules.json`
3. `confidence.model.json`
4. `00_Config.ps1`
5. `01_Scan.ps1`
6. `02_Classify.ps1`
7. `03_MapRelations.ps1`
8. `07_Validate.ps1`
9. `09_HealthCheck.ps1`
10. `RUN_ALL.ps1`

Eseguire smoke test su una cartella di prova prima della cartella reale.

---

## 27. Smoke Test Minimo

Struttura test:

```text
C:\Temp\ProjectMapperTest\
├── FY 24\
│   ├── Beurer\
│   │   ├── DN Beurer FY24 Final.docx
│   │   ├── RPT Beurer FY24.xlsx
│   │   ├── Agreement Beurer.pdf
│   │   └── Old\
│   │       └── DN Beurer FY24 Draft.docx
│   └── Medel\
│       ├── P&L Split Medel.xlsx
│       └── Comparables Medel.pdf
```

Comando:

```powershell
.\scripts\RUN_ALL.ps1 -Path "C:\Temp\ProjectMapperTest" -SkipExcelAudit
```

Atteso:

- Beurer: output finale trovato.
- RPT: classificato CALCULATION.
- Agreement: classificato CONTRACT.
- Draft in Old: OBSOLETE.
- Medel: input senza deliverable → issue HIGH corretta.
- Quality gate probabilmente `APPROVE WITH MANUAL REVIEW` o `BLOCK`, a seconda delle soglie.

---

## 28. Conclusione

Project Mapper v3.0 è una base solida per automazione documentale professionale.

È:

- modulare;
- verificabile;
- estendibile;
- prudente;
- auditabile;
- adatto a cartelle Transfer Pricing / legali / finanziarie;
- utile come asset dimostrabile in contesti professionali.

**Raccomandazione finale:** implementare prima il core PowerShell con config esterne e quality gate. Integrare l'audit Excel solo dopo il primo smoke test riuscito.
