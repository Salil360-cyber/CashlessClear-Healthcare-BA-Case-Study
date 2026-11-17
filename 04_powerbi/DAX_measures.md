# Power BI build: model, Power Query steps and DAX measures

## 1. Load

Get Data > Text/CSV: `claims_clean.csv` → table `claims`; `insurer_queries.csv` → table `queries`.
In Power Query set all `_at` columns to Date/Time and amounts to Whole Number.

## 2. Power Query: add hour columns to `claims` (Add Column > Custom Column)

| New column | Formula | Type |
| --- | --- | --- |
| preauth_hours | `Duration.TotalHours([preauth_decided_at] - [preauth_requested_at])` | Decimal |
| file_prep_hours | `if [discharge_ordered_at] = null then null else Duration.TotalHours([discharge_file_sent_at] - [discharge_ordered_at])` | Decimal |
| insurer_hours | `if [discharge_ordered_at] = null then null else Duration.TotalHours([final_approval_at] - [discharge_file_sent_at])` | Decimal |
| exit_hours | `if [discharge_ordered_at] = null then null else Duration.TotalHours([patient_left_at] - [discharge_ordered_at])` | Decimal |
| extra_night | `if [discharge_ordered_at] = null then null else if Date.From([patient_left_at]) > Date.From([discharge_ordered_at]) then "Yes" else "No"` | Text |
| order_band | `if [discharge_ordered_at] = null then null else if Time.Hour([discharge_ordered_at]) < 12 then "Before 12:00" else if Time.Hour([discharge_ordered_at]) < 15 then "12:00-15:00" else "After 15:00"` | Text |

## 3. Relationship

`claims[claim_id]` 1 → * `queries[claim_id]`

## 4. Measures

```
Claims = COUNTROWS(claims)

Settled = CALCULATE([Claims], claims[claim_status] = "Settled cashless")

Pre-auth within 1h % = DIVIDE(CALCULATE([Claims], claims[preauth_hours] <= 1), [Claims])

Final within 3h % = DIVIDE(CALCULATE([Settled], claims[insurer_hours] <= 3), [Settled])

Avg Exit Hours = AVERAGE(claims[exit_hours])

Avg File Prep Hours = AVERAGE(claims[file_prep_hours])

Avg Insurer Hours = AVERAGE(claims[insurer_hours])

Extra Nights = CALCULATE([Claims], claims[extra_night] = "Yes")

Extra Night % = DIVIDE([Extra Nights], [Settled])

Pre-auth Query % = DIVIDE(CALCULATE([Claims], claims[preauth_queries] > 0), [Claims])

Deduction % = DIVIDE(SUM(claims[deduction_amount]), SUM(claims[billed_amount]))

Queries = COUNTROWS(queries)
```

Sort `order_band`: add a column `band_order` (1, 2, 3) and use Column tools > Sort by column.

## 5. Expected values

| Measure | Value |
| --- | --- |
| Claims | 12,000 |
| Pre-auth within 1h % | 50.5% |
| Final within 3h % | 66.8% |
| Avg Exit Hours | 7.59 |
| Avg File Prep Hours | 2.85 |
| Extra Nights | 2,508 |
| Deduction % | 7.7% |
| Queries | 6,581 |

These match `03_sql/results.md` and the Excel workbook.
