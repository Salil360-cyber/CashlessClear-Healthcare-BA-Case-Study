# Build guide

Build the Excel, SQL and Power BI parts yourself, then compare your numbers with the **expected values** at each step.

## Part A: Excel (start from `01_data/claims_raw.csv`)

**A1. Open and save**
1. Open the CSV → File > Save As → `CashlessClear_Analysis.xlsx`.
2. Rename the sheet `Raw_Data`, make a copy named `Clean_Data` (right-click tab > Move or Copy > Create a copy). Work on `Clean_Data`.

**A2. Remove duplicates**: Data > Remove Duplicates > Select All → **180** removed, **12,000** rows left.

**A3. Fix `payer_type`** (column E)
1. Insert a helper column: `=PROPER(TRIM(E2))`, fill down.
2. Ctrl+H on the helper: Find `Psu`, Replace `PSU` (Match case) → Replace All.
3. Paste Special > Values over `payer_type`, delete the helper. Filter check: only 3 payer types. (**500** fixed.)

**A4. Fix `department`** (column C)
1. New sheet `Dept_Map`: A1 `Raw name`, B1 `Clean name`, then rows: Ortho → Orthopaedics, Cardio → Cardiology, Surgery → General Surgery, Gen Medicine → General Medicine, OBG → Maternity, Onco → Oncology.
2. Helper column in `Clean_Data`: `=IFERROR(VLOOKUP(C2,Dept_Map!$A:$B,2,FALSE),C2)` → if the name is in the map it is replaced, otherwise kept.
3. Paste as values over `department`, delete the helper. (**300** fixed.)

**A5. Check dates**: select columns I to Q (all `_at` columns) → Format Cells > Custom `yyyy-mm-dd hh:mm`. If any column stays left-aligned, it is text: Data > Text to Columns > Finish converts it.

**A6. Table + formula columns**: Ctrl+T, name the table `claims`. Add at the right:

| Column | Formula |
| --- | --- |
| preauth_hours | `=ROUND(([@preauth_decided_at]-[@preauth_requested_at])*24,2)` |
| preauth_within_1h | `=IF([@preauth_hours]<=1,"Yes","No")` |
| file_prep_hours | `=IF([@discharge_ordered_at]="","",ROUND(([@discharge_file_sent_at]-[@discharge_ordered_at])*24,2))` |
| insurer_approval_hours | `=IF([@discharge_ordered_at]="","",ROUND(([@final_approval_at]-[@discharge_file_sent_at])*24,2))` |
| final_within_3h | `=IF([@discharge_ordered_at]="","",IF([@insurer_approval_hours]<=3,"Yes","No"))` |
| order_to_exit_hours | `=IF([@discharge_ordered_at]="","",ROUND(([@patient_left_at]-[@discharge_ordered_at])*24,2))` |
| extra_night | `=IF([@discharge_ordered_at]="","",IF(INT([@patient_left_at])>INT([@discharge_ordered_at]),"Yes","No"))` |
| order_time_band | `=IF([@discharge_ordered_at]="","",IF(HOUR([@discharge_ordered_at])<12,"Before 12:00",IF(HOUR([@discharge_ordered_at])<15,"12:00-15:00","After 15:00")))` |

Why `*24`: Excel stores time in days, so (end − start) × 24 = hours. `INT` of a date-time gives just the date.

**A7. Summary sheet**

| KPI | Formula | Expected |
| --- | --- | --- |
| Settled cashless | `=COUNTIF(claims[claim_status],"Settled cashless")` | 11,565 |
| Pre-auth within 1 h | `=COUNTIF(claims[preauth_within_1h],"Yes")/12000` | 50.5% |
| Final within 3 h | `=COUNTIF(claims[final_within_3h],"Yes")/11565` | 66.8% |
| Avg order to exit | `=AVERAGE(claims[order_to_exit_hours])` | 7.59 |
| Avg hospital file prep | `=AVERAGE(claims[file_prep_hours])` | 2.85 |
| Extra nights | `=COUNTIF(claims[extra_night],"Yes")` | 2,508 |
| Deduction % | `=SUM(claims[deduction_amount])/SUM(claims[billed_amount])` | 7.7% |

**A8. Pivot tables** (Insert > PivotTable > table `claims` > new sheet `Analysis`)
1. Rows `payer_type`, `via_tpa`; Columns `final_within_3h`; Values Count; Show Values As % of Row Total. Expected Yes: PSU + TPA **48.2%**, standalone **80.6%**.
2. Rows `order_time_band`; Columns `extra_night`; % of Row Total. Expected Yes: before 12:00 **4.7%**, after 15:00 **54.6%**. Insert a column chart from it.
3. Add a column `has_preauth_query`: `=IF([@preauth_queries]>0,1,0)`. Pivot: Rows `admission_type`; Values Average of `has_preauth_query` (as %). Expected: Emergency **35.4%**, Planned **20.2%**.
4. Rows `discharge_queries`; Values Average of `order_to_exit_hours`. Expected: 0 → **6.40**, 1 → **12.03**.
5. Rows `deduction_reason`; Values Sum of `deduction_amount` and Sum of `billed_amount`; add a calculated field `= deduction_amount / billed_amount`. Expected: **5.5%** and **24.1%**.

## Part B: SQL (pgAdmin 4)

1. Create database `cashlessclear` → run `03_sql/01_schema.sql`.
2. Import `claims_clean.csv` into `claims` and `insurer_queries.csv` into `insurer_queries` (Header ON, NULL strings empty).
3. Expected counts: **12,000** and **6,581**.
4. Run each query in `03_analysis.sql` one at a time, compare with `results.md`, and write one line in your own words about what each answers.

## Part C: Power BI Desktop

Follow [`04_powerbi/DAX_measures.md`](04_powerbi/DAX_measures.md) (load, Power Query columns, relationship, measures), then build:

**Page 1: Insurance desk overview**: 4 cards (Claims, Pre-auth within 1h %, Final within 3h %, Extra Nights); bar of Avg File Prep / Avg Insurer Hours; bar of `payer_type` + `via_tpa` vs Final within 3h %; column of month vs Pre-auth within 1h %; column of `admission_type` vs Pre-auth Query %; slicers for hospital, department, payer type in one row.

**Page 2: Root cause**: column of `order_band` vs Extra Night %; column of `discharge_queries` vs Avg Exit Hours; column of `deduction_reason` vs Deduction %; two bars of `queries[query_reason]` vs Queries, one filtered to each `query_stage`.

Check the cards against the expected values, save as `CashlessClear_Dashboard.pbix` and add it to `04_powerbi/`.
