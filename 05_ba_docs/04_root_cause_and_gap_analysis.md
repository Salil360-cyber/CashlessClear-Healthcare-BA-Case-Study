# 4. Root cause and gap analysis

## 5 Whys: why are patients kept an extra night?

1. **Why do patients stay an extra night?** Final approval and payment finish after 22:00, so the patient cannot leave until morning (2,508 cases).
2. **Why does it finish so late?** Discharge takes 7.6 hours from the doctor's order, and 3,011 orders are written after 15:00.
3. **Why does discharge take 7.6 hours?** The hospital takes 2.85 hours to build the file, the insurer 3.01 hours to approve it, and 21.0% of files get a query that adds about 5.6 hours.
4. **Why is the file slow and often incomplete?** It is started only after the discharge order, and the summary, itemised bill and invoices come from different teams with no checklist.
5. **Why is there no plan?** Discharges are not planned the day before, and nobody tracks the time each step takes.

**Root causes:** no discharge planning, no file checklist, no tracking of the 1-hour / 3-hour clocks.

## Fishbone (cause categories)

| Category | Causes found |
| --- | --- |
| Process | Discharge file started only after the order; orders written late in the day |
| People | Emergency admissions sent for pre-auth without all reports (35.4% query rate) |
| Technology | Reports not auto-attached from the hospital system; no checklist on the desk screen |
| Data / reporting | No view of claims nearing the 1-hour / 3-hour limits |
| External | Insurers working through a TPA approve more slowly (PSU + TPA: 48.2% within 3 h vs 80.6% for standalone health insurers) |
| Policy communication | Room-rent limits explained only at discharge |

## Gap analysis

| Area | AS-IS | TO-BE | Gap to close |
| --- | --- | --- | --- |
| Pre-auth request | Reports attached by hand, often missing | Checklist by department, reports auto-attached | BR-01 |
| Discharge file | Built after the order, sent incomplete | Drafted the evening before, checklist blocks incomplete files | BR-02 |
| Discharge timing | 26% of orders after 15:00 | Orders on the morning round | BR-03 |
| Monitoring | No live view | Tracker with 1 h / 3 h clocks, escalation, daily MIS | BR-04 |
| Patient costs | Deductions learnt at discharge | Room-rent check and estimate at admission | BR-05 |
| Payer performance | Not measured | Monthly payer / TPA scorecard | BR-06 |
| Claim exchange | Email and portals | NHCX connection | BR-07 |
