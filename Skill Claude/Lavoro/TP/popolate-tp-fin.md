---
name: "populate-analisi-tp-fin"
description: "Populates the Excel Analisi sheet from Screening Results while preserving formulas. Invoke when user requests automated Analisi population or mapping rules."
---

# Populate Analisi

## Scopo
Automatizzare il popolamento del foglio "Analisi" partendo dal foglio "Results/Risultati" generato dallo screening, preservando le formule esistenti e mappando correttamente le colonne.

## Quando attivare
Attiva questa skill quando l'utente chiede di:
- Popolare automaticamente il foglio "Analisi"
- Mappare colonne tra "Results" e "Analisi"
- Preservare formule e gestire controlli di coerenza

## Procedura operativa
1. Validare presenza fogli e intestazioni
2. Identificare riga header e mappare le colonne per pattern
3. Allineare righe per Bond ISIN
4. Popolare solo le colonne di input e sintesi
5. Preservare le formule nelle colonne calcolate
6. Eseguire controlli di coerenza (mismatch, colonne vuote, formati)

## Regole di compilazione
- Non sovrascrivere formule nel foglio "Analisi"
- Convertire "n.a." in celle vuote
- Normalizzare i valori percentuali in numeri
- Evidenziare i flag NACE per review manuale

---

## Mapping colonne Bond Results → Analisi Long (OBBLIGATORIO)

Le seguenti colonne devono essere sempre popolate da Bond Results usando il Bond ISIN come chiave di join:

| Colonna Analisi Long | Indice AL (0-based) | Fonte Bond Results | Indice BR (0-based) |
|---|---|---|---|
| Final Coupon Date | 22 | Final Coupon Date | 32 |
| Price Date | 23 | Price Date | 33 |
| Coupon Type (col 41) | 41 | Coupon Type | 23 |
| Valuta (col 42) | 42 | Bond Currency | 20 |

> ⚠️ **Final Coupon Date e Price Date sono obbligatorie**: devono essere sempre popolate. Se un ISIN non ha corrispondenza in Bond Results, segnalarlo nel log finale.

---

## Formattazione date — REGOLA OBBLIGATORIA

Tutte le date provenienti da Bond Results o da qualsiasi fonte xlsb **devono** essere scritte come oggetti `datetime` Python con `number_format = 'DD/MM/YYYY'` (es. `05/06/2115`).

> ❌ Non scrivere mai stringhe ISO come `2025-03-31T00:00:00.000Z` nelle celle.  
> ❌ Non scrivere interi serial Excel senza number_format corretto.  
> ✅ Scrivere sempre oggetti `datetime` con `cell.number_format = 'DD/MM/YYYY'`

### Funzione parse_date (usare SEMPRE per qualsiasi valore data)

```python
from datetime import datetime, timedelta

def parse_date(val):
    """Converte ISO string o serial Excel in oggetto datetime."""
    if val is None:
        return None
    if isinstance(val, str) and 'T' in val:
        try:
            return datetime.strptime(val[:10], '%Y-%m-%d')
        except ValueError:
            return None
    if isinstance(val, (int, float)) and val > 30000:
        base = datetime(1899, 12, 30)
        return base + timedelta(days=int(val))
    if isinstance(val, datetime):
        return val
    return None
```

### Scrittura corretta nella cella openpyxl

```python
dt = parse_date(raw_value)
if dt:
    cell.value = dt                    # oggetto datetime, non stringa!
    cell.number_format = 'DD/MM/YYYY'
```

### Rilevamento automatico colonne data
Applicare `parse_date` + `number_format = 'DD/MM/YYYY'` a **tutte** le colonne il cui header contiene "date" (case-insensitive):

```python
DATE_COLS = set()
for i, h in enumerate(header_row):
    if h and 'date' in str(h).lower():
        DATE_COLS.add(i)
```

---

## Script di popolazione (template)

```python
from pyxlsb import open_workbook
from datetime import datetime, timedelta
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment

def parse_date(val):
    if val is None:
        return None
    if isinstance(val, str) and 'T' in val:
        try:
            return datetime.strptime(val[:10], '%Y-%m-%d')
        except ValueError:
            return None
    if isinstance(val, (int, float)) and val > 30000:
        return datetime(1899, 12, 30) + timedelta(days=int(val))
    if isinstance(val, datetime):
        return val
    return None

def read_sheet(path, sheet_name):
    rows = []
    with open_workbook(path) as wb:
        with wb.get_sheet(sheet_name) as sheet:
            for row in sheet.rows():
                rows.append([c.v for c in row])
    return rows

# Leggi i fogli
rows_br = read_sheet(INPUT_FILE, 'Bond Results')
rows_al = read_sheet(INPUT_FILE, 'Analisi Long')

# Lookup Bond Results per ISIN
br_lookup = {row[0]: row for row in rows_br[1:] if row and row[0]}

# Rileva colonne data dall'header (riga 3, 0-based)
HEADER_IDX = 3
header = rows_al[HEADER_IDX]
DATE_COLS = {i for i, h in enumerate(header) if h and 'date' in str(h).lower()}
# Aggiungi sempre esplicitamente le colonne critiche
DATE_COLS.update({22, 23})  # Final Coupon Date, Price Date

# Popola in memoria
for r_idx, row in enumerate(rows_al):
    if r_idx <= HEADER_IDX or not row or row[0] is None:
        continue
    isin = row[1] if len(row) > 1 else None
    if not isin or isin not in br_lookup:
        continue
    br = br_lookup[isin]
    while len(row) <= 51:
        row.append(None)

    if row[22] is None:
        row[22] = parse_date(br[32] if len(br) > 32 else None)  # Final Coupon Date
    if row[23] is None:
        row[23] = parse_date(br[33] if len(br) > 33 else None)  # Price Date
    if row[41] is None:
        row[41] = br[23] if len(br) > 23 else None  # Coupon Type
    if row[42] is None:
        row[42] = br[20] if len(br) > 20 else None  # Valuta

    # Converti tutte le date esistenti
    for col_i in DATE_COLS:
        if col_i < len(row) and row[col_i] is not None and not isinstance(row[col_i], datetime):
            row[col_i] = parse_date(row[col_i])

# Scrivi in openpyxl
wb_out = openpyxl.Workbook()
ws = wb_out.active
ws.title = 'Analisi Long'

for r_idx, row in enumerate(rows_al):
    for c_idx, val in enumerate(row):
        if val is None:
            continue
        cell = ws.cell(row=r_idx + 1, column=c_idx + 1)
        cell.value = val
        if c_idx in DATE_COLS and isinstance(val, datetime):
            cell.number_format = 'DD/MM/YYYY'

wb_out.save(OUTPUT_FILE)
```

---

## Verifica finale obbligatoria
Dopo il salvataggio, verificare sempre:

```python
wb_v = openpyxl.load_workbook(OUTPUT_FILE)
ws_v = wb_v.active
total = sum(1 for r in range(5, ws_v.max_row+1) if ws_v.cell(row=r, column=1).value)
for col_name, col_idx in [('Final Coupon Date', 23), ('Price Date', 24), ('Coupon Type', 42), ('Valuta', 43)]:
    filled = sum(1 for r in range(5, ws_v.max_row+1) if ws_v.cell(row=r, column=1).value and ws_v.cell(row=r, column=col_idx).value)
    print(f"{col_name}: {filled}/{total}")
```

## Fase 4: Gestione errori e bug check
- ISIN in Analisi Long non trovato in Bond Results → segnalare nel log
- Formato numerico non coerente (testo vs numero)
- Date scritte come stringhe ISO o interi → usare sempre parse_date

## Output atteso
- File `_Analisi_Long_Popolato.xlsx` con dati inseriti e date in formato `DD/MM/YYYY`
- Riepilogo colonne popolate e ISIN non matchati stampato a console
