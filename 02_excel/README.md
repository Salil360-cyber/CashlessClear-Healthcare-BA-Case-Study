# 02_excel

`CashlessClear_Analysis.xlsx`: every number on Summary and Analysis is a formula on `Clean_Data`.

| Sheet | What it shows |
| --- | --- |
| About | Sheet guide and the IRDAI targets used |
| Cleaning_Log | 180 duplicates removed, 500 payer values fixed, 300 department names mapped |
| Dept_Map | Lookup table for short department names (used with VLOOKUP) |
| Clean_Data | 12,000 claims as an Excel Table (`claims`) + 8 formula columns: hours between timestamps, 1 h / 3 h checks, extra night (`INT` of dates), order time band (`HOUR` + nested `IF`) |
| Summary | Claim outcome and KPIs (COUNTIF, AVERAGE, SUM) |
| Analysis | Payer & TPA, order time vs extra night (with chart), pre-auth queries by admission type, discharge queries, deductions (COUNTIFS, AVERAGEIFS, SUMIFS) |

Key results: **50.5%** of pre-auths decided within 1 hour; **66.8%** of final approvals within 3 hours; **7.59 h** from discharge order to exit; **2,508** patients kept an extra night. Excel and SQL results match.
