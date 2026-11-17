"""Generate CashlessClear synthetic data. Narmada Hospitals and all insurers are fictional.
One row per cashless admission + one row per insurer query."""
import numpy as np, pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(5)
N = 12000
H = lambda h: timedelta(hours=float(h))

def desk(t, start=8, end=22):
    """Hospital insurance/billing desk works 08:00-22:00 every day."""
    if t.hour < start:
        return t.replace(hour=start, minute=0)
    if t.hour >= end:
        return (t + timedelta(days=1)).replace(hour=start, minute=0)
    return t

DEPT = {"Cardiology": (5, 160000), "Orthopaedics": (4, 140000), "General Surgery": (4, 95000),
        "General Medicine": (4, 55000), "Maternity": (3, 70000), "Oncology": (6, 180000)}
PAYER = {"Standalone Health Insurer": (.40, 0.0), "Private General Insurer": (.32, .5), "PSU General Insurer": (.28, 1.0)}
PRE_Q = ["Investigation reports missing", "Doctor's notes / treatment plan unclear", "Policy / KYC copy missing", "Past medical history asked"]
DIS_Q = ["Discharge summary incomplete", "Itemised bill breakup missing", "Implant / pharmacy invoice missing", "Final investigation reports missing"]
rows, queries = [], []
qid = 0
for i in range(1, N + 1):
    cid = f"CL{i:05d}"
    hosp = rng.choice(["Nagpur", "Pune", "Nashik"], p=[.40, .35, .25])
    dept = rng.choice(list(DEPT), p=[.16, .15, .18, .24, .15, .12])
    adm = rng.choice(["Planned", "Emergency"], p=[.45, .55])
    payer = rng.choice(list(PAYER), p=[v[0] for v in PAYER.values()])
    tpa = "Yes" if rng.random() < PAYER[payer][1] else "No"
    pol = rng.choice(["Retail", "Group"], p=[.65, .35])
    room = rng.choice(["General Ward", "Twin Sharing", "Single Room"], p=[.30, .40, .30])
    admit = datetime(2026, 1, 1) + timedelta(days=int(rng.integers(0, 181)),
                                            hours=int(rng.choice(range(24), p=np.array([2,1,1,1,1,1,2,3,5,7,8,8,7,6,6,6,6,5,5,5,4,4,3,3]) / 100)),
                                            minutes=int(rng.integers(0, 60)))
    # ---- pre-authorisation ----
    req = desk(admit + H(rng.gamma(2, .35 if adm == "Planned" else 1.4)))
    base = {"Standalone Health Insurer": .45, "Private General Insurer": .55, "PSU General Insurer": .6}[payer] * (1.7 if tpa == "Yes" else 1)
    p_q = .20 + (.15 if adm == "Emergency" else 0)
    t = req + H(rng.gamma(2, base / 2 * 1.2))
    pre_q = 0
    while pre_q < 2 and rng.random() < (p_q if pre_q == 0 else .2):
        qid += 1; pre_q += 1
        reason = rng.choice(PRE_Q, p=[.38, .27, .20, .15])
        back = desk(t + H(rng.gamma(2, 1.6)))                         # hospital replies
        queries.append([f"Q{qid:05d}", cid, "Pre-authorisation", reason, t, back])
        t = back + H(rng.gamma(2, base / 2))
    denied = rng.random() < .035
    pre_dec = t
    if denied:
        rows.append([cid, hosp, dept, adm, payer, tpa, pol, room, admit, req, pre_dec, "Denied", pre_q,
                     None, None, None, None, 0, None, None, None, "", "Converted to reimbursement"]); continue
    # ---- stay & discharge ----
    los = max(1, int(round(rng.gamma(3, DEPT[dept][0] / 3))))
    order = (admit + timedelta(days=los)).replace(hour=int(rng.choice(range(9, 21), p=np.array([6,12,15,16,14,11,9,7,4,3,2,1]) / 100)),
                                                  minute=int(rng.integers(0, 60)))
    summary_missing = rng.random() < .28
    prep = rng.gamma(2, .9) + (rng.gamma(2, 1.0) if summary_missing else 0) + (.8 if order.hour >= 17 else 0)
    sent = desk(order + H(prep))
    fbase = {"Standalone Health Insurer": 1.3, "Private General Insurer": 1.6, "PSU General Insurer": 1.8}[payer] * (1.6 if tpa == "Yes" else 1)
    t = sent + H(rng.gamma(2, fbase / 2))
    dis_q = 0
    p_dq = .18 + (.12 if summary_missing else 0)
    if rng.random() < p_dq:
        qid += 1; dis_q = 1
        reason = rng.choice(DIS_Q, p=[.34, .30, .20, .16])
        back = desk(t + H(rng.gamma(2, .9)))
        queries.append([f"Q{qid:05d}", cid, "Final discharge", reason, t, back])
        t = back + H(rng.gamma(2, fbase / 3))
    approval = t
    pay = approval + H(rng.gamma(2, .25))
    if pay.hour >= 22:                                   # too late to leave: stays the night
        exit_ = (pay + timedelta(days=1)).replace(hour=9, minute=30)
    elif pay.hour < 8:
        exit_ = pay.replace(hour=9, minute=30)
    else:
        exit_ = pay
    billed = int(round(rng.gamma(4, DEPT[dept][1] / 4) / 100) * 100)
    nonpay = rng.uniform(.03, .08)
    capped = pol == "Retail" and room == "Single Room" and rng.random() < .6
    ded = billed * (nonpay + (rng.uniform(.12, .25) if capped else 0))
    ded_reason = "Room rent capping + non-payable items" if capped else "Non-payable items"
    rows.append([cid, hosp, dept, adm, payer, tpa, pol, room, admit, req, pre_dec, "Approved", pre_q,
                 order, sent, approval, exit_, dis_q, billed, int(round(ded / 100) * 100), billed - int(round(ded / 100) * 100), ded_reason, "Settled cashless"])

C = ["claim_id", "hospital", "department", "admission_type", "payer_type", "via_tpa", "policy_type", "room_category",
     "admitted_at", "preauth_requested_at", "preauth_decided_at", "preauth_outcome", "preauth_queries",
     "discharge_ordered_at", "discharge_file_sent_at", "final_approval_at", "patient_left_at", "discharge_queries",
     "billed_amount", "deduction_amount", "approved_amount", "deduction_reason", "claim_status"]
A = pd.DataFrame(rows, columns=C)
Q = pd.DataFrame(queries, columns=["query_id", "claim_id", "query_stage", "query_reason", "raised_at", "answered_at"])
for c in [c for c in C if c.endswith("_at")]:
    A[c] = pd.to_datetime(A[c]).dt.strftime("%Y-%m-%d %H:%M")
for c in ["raised_at", "answered_at"]:
    Q[c] = Q[c].dt.strftime("%Y-%m-%d %H:%M")
for c in ["billed_amount", "deduction_amount", "approved_amount"]:
    A[c] = A[c].astype("Int64")
A.to_csv("01_data/claims_clean.csv", index=False)
Q.to_csv("01_data/insurer_queries.csv", index=False)

# raw file with deliberate issues
R = A.copy().astype(object)
idx = rng.choice(len(R), 500, replace=False)
R.loc[idx, "payer_type"] = [rng.choice([p.upper(), p.lower(), " " + p]) for p in A.payer_type.iloc[idx]]
idx = rng.choice(len(R), 300, replace=False)
R.loc[idx, "department"] = [{"Orthopaedics": "Ortho", "General Medicine": "Gen Medicine", "General Surgery": "Surgery",
                             "Cardiology": "Cardio", "Maternity": "OBG", "Oncology": "Onco"}[d] for d in A.department.iloc[idx]]
dups = R.sample(180, random_state=3)
R = pd.concat([R, dups]).sample(frac=1, random_state=9).reset_index(drop=True)
R.to_csv("01_data/claims_raw.csv", index=False)
print(len(R), len(A), len(Q))
