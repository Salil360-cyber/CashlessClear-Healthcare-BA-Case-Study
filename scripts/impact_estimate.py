"""TO-BE impact estimate for CashlessClear (6 months). Uses only rates already seen in the data (SQL Q7, Q8, Q9)."""
import pandas as pd
cols = pd.read_csv("01_data/claims_clean.csv", nrows=1).columns
A = pd.read_csv("01_data/claims_clean.csv", parse_dates=[c for c in cols if c.endswith("_at")])
S = A[A.claim_status == "Settled cashless"].copy()
S["exit_h"] = (S.patient_left_at - S.discharge_ordered_at).dt.total_seconds() / 3600
S["extra_night"] = S.patient_left_at.dt.date > S.discharge_ordered_at.dt.date
hr = S.discharge_ordered_at.dt.hour
late, mid = S[hr >= 15], S[(hr >= 12) & (hr < 15)]
SHIFT = 0.5           # assumption: discharge planning on morning rounds moves half of after-15:00 orders to 12:00-15:00
QUERY_AVOIDED = 0.5   # assumption: discharge-file checklist prevents half of discharge-stage queries
nights_saved = SHIFT * len(late) * (late.extra_night.mean() - mid.extra_night.mean())
q = S[S.discharge_queries > 0]
hours_per_query = q.exit_h.mean() - S[S.discharge_queries == 0].exit_h.mean()
queries_avoided = QUERY_AVOIDED * len(q)
los = (S.discharge_ordered_at.dt.normalize() - S.admitted_at.dt.normalize()).dt.days.mean()
extra_adm = nights_saved / los
print(f"After-15:00 orders: {len(late):,} at {late.extra_night.mean():.1%} extra night; 12:00-15:00 rate {mid.extra_night.mean():.1%}")
print(f"Bed-nights freed: {nights_saved:,.0f} of {S.extra_night.sum():,} today")
print(f"Avg length of stay {los:.1f} days -> about {extra_adm:,.0f} more admissions possible; avg bill Rs {S.billed_amount.mean():,.0f} -> Rs {extra_adm*S.billed_amount.mean()/1e7:.2f} crore")
print(f"Discharge queries avoided: {queries_avoided:,.0f}; each adds {hours_per_query:.1f} h -> {queries_avoided*hours_per_query:,.0f} patient-hours saved")
new_exit = (S.exit_h.sum() - queries_avoided * hours_per_query) / len(S)
print(f"Avg order-to-exit: {S.exit_h.mean():.2f} h -> {new_exit:.2f} h (query fix only)")
