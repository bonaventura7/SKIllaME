# EDF-X Pricing Agent Skill
## Version 3.1-HA | Parametric | Calculate Rates Per Row

---

## RULE ZERO
**Every single row requires: set Date → set Tenor → CLICK "Calculate Rates" → read value.**  
No shortcuts. No caching. Changing Date or Tenor without clicking Calculate Rates returns stale data from the previous row.

---

## PHASE 0 – COLLECT PARAMETERS (Ask the user before any action)

Ask the user for these exact inputs. Do NOT proceed until all are provided.

| # | Parameter | Example | Stored as |
|---|-----------|---------|-----------|
| 1 | **Rating** | `Baa3` | `RATING` |
| 2 | **Currency** | `EUR` | `CURRENCY` |
| 3 | **Reference Rate** | `European Government Bond` | `REF_RATE` |
| 4 | **Tenors (years)** | `3, 4, 5` | `TENORS` (list) |
| 5 | **Origination Dates** | `02/01/2025, 03/02/2025, ...` | `DATES_RAW` (list) |
| 6 | **Company ID** | `IT01457570065` | `COMPANY_ID` (default if blank) |

If the user says "same as before" or "continue", load the existing checkpoint JSON from the conversation context and skip to **Phase 5 (Resume)**.

---

## PHASE 1 – HOLIDAY CORRECTION (Pre-processing)

For every date in `DATES_RAW`, apply this rule:

> If the date falls on **Saturday**, **Sunday**, or an **Italian/TARGET2 holiday**, shift forward day-by-day until the first working day.

### Holiday Calendar (2025–2027)
```
2025: 01-01, 01-06, 04-18, 04-20, 04-21, 04-25, 05-01, 06-02, 08-15, 11-01, 12-08, 12-25, 12-26
2026: 01-01, 01-06, 04-03, 04-05, 04-06, 04-25, 05-01, 06-02, 08-15, 11-01, 12-08, 12-25, 12-26
2027: 01-01, 01-06, 03-26, 03-28, 03-29, 04-25, 05-01, 06-02, 08-15, 11-01, 12-08, 12-25, 12-26
```

Store corrected dates as `DATES_EFFECTIVE`.

---

## PHASE 2 – BUILD CHECKPOINT

Construct this JSON structure and keep it updated in the conversation context (or save to a text file / Google Sheets cell if possible):

```json
{
  "meta": {
    "version": "3.1-HA",
    "target_url": "https://edfx.moodysanalytics.com/company/{COMPANY_ID}/instruments/instrument-pricing",
    "total_rows": N,
    "last_processed_row_id": 0,
    "params": {
      "rating": "RATING",
      "currency": "CURRENCY",
      "ref_rate": "REF_RATE",
      "tenors": [3,4,5],
      "dates_count": 15
    }
  },
  "queue": [
    {
      "row_id": 1,
      "origination_date_requested": "02/01/2025",
      "origination_date_effective": "02/01/2025",
      "tenor_years": 3,
      "rating": "RATING",
      "currency": "CURRENCY",
      "ref_rate": "REF_RATE",
      "status": "pending",
      "credit_spread_bps": null,
      "attempts": 0,
      "calculate_rates_clicked": false
    }
  ]
}
```

Generate one queue item per `(date_effective × tenor)` combination.  
**Total rows = `len(DATES_EFFECTIVE) × len(TENORS)`**.

---

## PHASE 3 – EXECUTION LOOP (EDF-X)

**Load EDF-X once.** Keep the page open for the entire session.

For each row in `queue` where `status == "pending"` and `attempts < 3`:

### Step 3.1 – Set Date
- Click the Origination Date input field.
- Clear it (Ctrl+A, Delete).
- Type the `origination_date_effective` in format **DD/MM/YYYY**.
- **Fallback (date picker frozen):**
  - Press `F12` → open Console.
  - Paste and execute:
    ```javascript
    let d = document.querySelector('input[placeholder*="Date"], input[type="date"]');
    if(d){ d.value='DD/MM/YYYY'; d.dispatchEvent(new Event('input',{bubbles:true})); }
    ```
  - Press `F12` to close Console.

### Step 3.2 – Set Tenor
- Click the Tenor dropdown / `expand_more` button.
- Select the numeric value (e.g. `3`).
- **Fallback (dropdown stuck):**
  - Click the field → press `ArrowDown` N times → press `Enter`.
  - Or Console:
    ```javascript
    Array.from(document.querySelectorAll('li,option,[role="option"]')).find(el=>el.textContent.trim()==='3').click();
    ```

### Step 3.3 – Verify Static Fields (first row only)
- Confirm Rating, Currency, and Reference Rate match `RATING`, `CURRENCY`, `REF_RATE`.
- If wrong, correct them. If correct, do not touch again.

### Step 3.4 – CLICK "Calculate Rates" (MANDATORY)
- Locate and click the **"Calculate Rates"** button (or "Calculate", "Run", ▶ icon).
- **Wait up to 5 seconds** for results to load.
- **If button is greyed out / disabled:** wait 2 seconds, retry once.
- **If button is not visible:** scroll up/down the page to locate it.
- **If still missing:** search page text for "Calculate" and click the nearest interactive element.
- After clicking, set `calculate_rates_clicked = true` for this row.

### Step 3.5 – Extract Value
- Locate **"Median Credit Spread (bps)"** on the page.
- Read the numeric value next to it (e.g. `121.64`).
- **If value is `—`, `N/A`, `null`, `0.00`:**
  - Set `status = "failed"`, `credit_spread_bps = null`.
  - Log note: `"No data returned by EDF-X"`.
  - Proceed to next row.
- **If page shows "Date is a holiday" error:**
  - Add 1 day to the effective date, retry this row **once only**.

---

## PHASE 4 – SAVE & CHECKPOINT (after every single row)

1. **Write to spreadsheet** (Google Sheets / Excel):
   - Find or create the row matching `(date, tenor)`.
   - Write `credit_spread_bps` in the **"Median Credit Spread (bps)"** column.

2. **Update checkpoint JSON:**
   - `status` → `"done"` (or `"failed"`)
   - `credit_spread_bps` → extracted value
   - `calculate_rates_clicked` → `true`
   - `attempts` → `attempts + 1`
   - `last_processed_row_id` → current `row_id`

3. **Persist checkpoint.** Save the JSON text to a file, a dedicated Google Sheets cell, or paste it back into the conversation.  
   **This is the HA lifeline.** If the agent stops, this checkpoint allows cold restart.

---

## PHASE 5 – COLD RESUME

If restarting:
1. Load the last saved checkpoint JSON.
2. Read `last_processed_row_id`.
3. Find the first row in `queue` with `status == "pending"` **after** that ID.
4. Open EDF-X (if not already open).
5. Begin **Phase 3** at that row.
6. **Never re-process rows already marked `"done"`.**

---

## CIRCUIT BREAKER

| Scenario | Action |
|----------|--------|
| Page timeout >10s | Refresh once → wait 5s → retry same row |
| Same error 3× in a row | Pause 30s → continue |
| "Session expired" / Login required | **STOP.** Write `"LOGIN REQUIRED"` in spreadsheet. Save checkpoint. |
| Calculate Rates button permanently missing | Scroll page. If still missing, refresh once and retry. |
| Blocking popup / overlay | Press `ESC` or click `X`. If persists, refresh and retry same row. |

---

## WORKAROUND CHEAT SHEET

```javascript
// DATE PICKER BYPASS
let d = document.querySelector('input[placeholder*="Date"], input[type="date"]');
if(d){ d.value='DD/MM/YYYY'; d.dispatchEvent(new Event('input',{bubbles:true})); }

// TENOR DROPDOWN BYPASS
Array.from(document.querySelectorAll('li,option,[role="option"]'))
  .find(el=>el.textContent.trim()==='3').click();

// FORCE CLICK CALCULATE (if hidden by overlay)
document.querySelector('button:contains("Calculate")').click();
```

---

## EXAMPLE FULL FLOW (1 row)

**Row:** `row_id=1`, `date=02/01/2025`, `tenor=3`, `rating=Baa3`, `currency=EUR`

1. Checkpoint shows row 1 is `pending`.
2. EDF-X page is already open.
3. Click Date field → clear → type `02/01/2025`.
4. Click Tenor dropdown → select `3`.
5. Verify Rating=Baa3, Currency=EUR (first row only).
6. **Click "Calculate Rates".** Wait 4s.
7. Read value: `121.64`.
8. Write `121.64` to spreadsheet row 1, column F.
9. Update checkpoint: `status="done"`, `credit_spread_bps=121.64`, `calculate_rates_clicked=true`, `last_processed_row_id=1`.
10. Save checkpoint.
11. Advance to row 2 (`date=02/01/2025`, `tenor=4`).

---

## EFFICIENCY RULES

- Load EDF-X **once** per session.
- Between rows: change **only** Date, Tenor, and click Calculate Rates.
- Do NOT refresh the page between rows.
- Do NOT take unnecessary screenshots.
- Use `Ctrl+End` in spreadsheets to jump to the bottom.
- Skip any row already marked `"done"` in the checkpoint.

---

*End of Skill. Execute Phase 0 now.*
