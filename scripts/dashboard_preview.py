"""Static preview of the 2-page Power BI design, drawn from the same CSVs (numbers match SQL)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
cols = pd.read_csv("01_data/claims_clean.csv", nrows=1).columns
A = pd.read_csv("01_data/claims_clean.csv", parse_dates=[c for c in cols if c.endswith("_at")])
Q = pd.read_csv("01_data/insurer_queries.csv")
S = A[A.claim_status == "Settled cashless"].copy()
h = lambda d, a, b: (d[b] - d[a]).dt.total_seconds() / 3600
A["pre_h"] = h(A, "preauth_requested_at", "preauth_decided_at")
for c, (x, y) in {"prep": ("discharge_ordered_at", "discharge_file_sent_at"), "ins": ("discharge_file_sent_at", "final_approval_at"),
                  "pay": ("final_approval_at", "patient_left_at"), "exit": ("discharge_ordered_at", "patient_left_at")}.items():
    S[c] = h(S, x, y)
S["night"] = S.patient_left_at.dt.date > S.discharge_ordered_at.dt.date
INK, MUTED, GRID, BAR, KEY, BG = "#1b1f24", "#5b6470", "#e6e8eb", "#9db4d6", "#1f4e9a", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False})

def card(ax, label, value):
    ax.axis("off"); ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color="#f3f5f8"))
    ax.text(.06, .62, value, fontsize=22, weight="bold", color=INK, transform=ax.transAxes)
    ax.text(.06, .22, label, fontsize=10, color=MUTED, transform=ax.transAxes)

def hbar(ax, labels, vals, title, fmt, key=()):
    y = np.arange(len(vals)); ax.barh(y, vals, color=[KEY if i in key else BAR for i in range(len(vals))], height=.6)
    ax.set_yticks(y, labels); ax.invert_yaxis()
    for i, v in enumerate(vals):
        ax.text(v, i, " " + fmt.format(v), va="center", color=INK, fontsize=9)
    ax.set_title(title, loc="left", color=INK, fontsize=11, weight="bold"); ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)
    ax.set_xlim(0, max(vals) * 1.22)

def vbar(ax, labels, vals, title, fmt, key=()):
    x = np.arange(len(vals)); ax.bar(x, vals, color=[KEY if i in key else BAR for i in range(len(vals))], width=.6)
    ax.set_xticks(x, labels)
    for i, v in enumerate(vals):
        ax.text(i, v, fmt.format(v), ha="center", va="bottom", color=INK, fontsize=9)
    ax.set_title(title, loc="left", color=INK, fontsize=11, weight="bold"); ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)
    ax.set_ylim(0, max(vals) * 1.2)

def page(title):
    fig = plt.figure(figsize=(16, 9), facecolor=BG)
    fig.text(.03, .955, title, fontsize=18, weight="bold", color=INK)
    fig.text(.03, .925, "CashlessClear · Narmada Hospitals (fictional) · cashless admissions Jan-Jun 2026 · targets: pre-auth 1 h, final approval 3 h (IRDAI)",
             fontsize=10, color=MUTED)
    return fig

fig = page("Insurance desk: IRDAI timelines & discharge")
for i, (l, v) in enumerate([("Cashless claims", f"{len(A):,}"), ("Pre-auth within 1 hour", f"{(A.pre_h<=1).mean():.1%}"),
                            ("Final approval within 3 hours", f"{(S.ins<=3).mean():.1%}"), ("Patients kept an extra night", f"{S.night.sum():,}")]):
    card(fig.add_axes([.03 + i * .24, .76, .22, .12]), l, v)
parts = pd.Series({"Hospital file prep": S.prep.mean(), "Insurer approval": S.ins.mean(), "Payment & exit": S.pay.mean()})
hbar(fig.add_axes([.14, .42, .33, .26]), parts.index, parts.values.round(2), f"Discharge order to exit: {S.exit.mean():.1f} h on average", "{:.2f} h", key=(0,))
grp = S.groupby(["payer_type", "via_tpa"]).ins.apply(lambda x: (x <= 3).mean() * 100).sort_values()
lab = [f"{p.replace(' Insurer','')}{' + TPA' if t=='Yes' else ''}" for p, t in grp.index]
hbar(fig.add_axes([.66, .42, .30, .26]), lab, grp.values.round(1), "% final approval within 3 h, by payer", "{:.1f}%", key=(0,))
mo = A.groupby(A.admitted_at.dt.month).pre_h.apply(lambda x: (x <= 1).mean() * 100); mo.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
vbar(fig.add_axes([.05, .07, .42, .24]), mo.index, mo.values.round(1), "% pre-auth decided within 1 hour, by month", "{:.1f}%")
adm = A.groupby("admission_type").preauth_queries.apply(lambda x: (x > 0).mean() * 100)
vbar(fig.add_axes([.55, .07, .42, .24]), adm.index, adm.values.round(1), "% of pre-auths with an insurer query", "{:.1f}%", key=(0,))
fig.savefig("04_powerbi/screenshots/page1_desk_overview.png", dpi=100); plt.close(fig)

fig = page("Root cause: queries, late discharge orders, deductions")
b = pd.Series(np.select([S.discharge_ordered_at.dt.hour < 12, S.discharge_ordered_at.dt.hour < 15], ["Before 12:00", "12:00-15:00"], "After 15:00"), index=S.index)
nb = S.night.groupby(b).mean().reindex(["Before 12:00", "12:00-15:00", "After 15:00"]) * 100
vbar(fig.add_axes([.05, .55, .40, .30]), nb.index, nb.values.round(1), "% of patients kept an extra night, by discharge order time", "{:.1f}%", key=(2,))
dq = S.groupby("discharge_queries").exit.mean(); dq.index = ["No query", "Insurer query"]
vbar(fig.add_axes([.55, .55, .18, .30]), dq.index, dq.values.round(2), "Order-to-exit hours", "{:.1f} h", key=(1,))
dd = S.groupby("deduction_reason").apply(lambda d: d.deduction_amount.sum() / d.billed_amount.sum() * 100)
dd.index = ["Non-payable only", "Room-rent capped"]
vbar(fig.add_axes([.79, .55, .18, .30]), dd.index, dd.values.round(1), "Deduction % of bill", "{:.1f}%", key=(1,))
pq = Q[Q.query_stage == "Pre-authorisation"].query_reason.value_counts()
hbar(fig.add_axes([.20, .08, .27, .32]), pq.index, pq.values, "Pre-authorisation query reasons", "{:,}", key=(0,))
fq = Q[Q.query_stage == "Final discharge"].query_reason.value_counts()
hbar(fig.add_axes([.70, .08, .26, .32]), fq.index, fq.values, "Final discharge query reasons", "{:,}", key=(0,))
fig.savefig("04_powerbi/screenshots/page2_root_cause.png", dpi=100); plt.close(fig)
print("ok")
