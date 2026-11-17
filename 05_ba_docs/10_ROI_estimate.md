# 10. Impact estimate

Script: [`scripts/impact_estimate.py`](../scripts/impact_estimate.py). It uses only rates already seen in the data (SQL Q7, Q8, Q9) and two stated assumptions.

## Assumptions (only two fixes counted)

| Fix | Assumption |
| --- | --- |
| BR-03 Discharge planning | **Half** of the 3,011 discharge orders written after 15:00 move to 12:00-15:00 and get that band's extra-night rate |
| BR-02 Discharge file checklist | **Half** of discharge-stage queries are avoided |

## Inputs from the data

| Input | Value |
| --- | --- |
| Extra-night rate: orders after 15:00 vs 12:00-15:00 | 54.6% vs 14.5% |
| Extra hours when the insurer raises a discharge query | 12.0 h − 6.4 h = 5.6 h |
| Discharge-stage queries | 2,432 |
| Average length of stay | 4.3 days |
| Average bill | Rs 1.09 lakh |

## Result (per 6 months)

| Measure | Today | After the two fixes |
| --- | --- | --- |
| Extra bed-nights | 2,508 | about **1,904** (about **604 freed**) |
| More admissions the freed beds allow | - | about **140**, worth about **Rs 1.5 crore** in billing |
| Discharge queries | 2,432 | about **1,216** fewer, saving about **6,800 patient-hours** of waiting |
| Average discharge order to exit | 7.6 h | about **7.0 h** (query fix alone) |

## Notes

- The pre-auth checklist, live tracker, room-rent check and NHCX are not counted, so this is a cautious estimate.
- The "more admissions" figure assumes there is demand for the freed beds; check bed occupancy before using it in a business case.
- After launch, track: % pre-auth within 1 h, % final approval within 3 h, average order-to-exit hours, extra bed-nights, query rate by reason, and room-rent complaints.
