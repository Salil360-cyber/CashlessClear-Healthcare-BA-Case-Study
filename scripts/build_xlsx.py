import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

F = "Arial"
cols = pd.read_csv("01_data/claims_clean.csv", nrows=1).columns
a = pd.read_csv("01_data/claims_clean.csv", parse_dates=[c for c in cols if c.endswith("_at")])
wb = Workbook()
H = Font(name=F, bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="1F3864")
B = Font(name=F, bold=True); N = Font(name=F); T = Font(name=F, bold=True, size=14)

def hdr(ws, r, vals):
    for i, x in enumerate(vals, 1):
        c = ws.cell(r, i, x); c.font = H; c.fill = HF; c.alignment = Alignment(horizontal="center", wrap_text=True)

def setn(ws, r1, r2, c1, c2):
    for row in ws.iter_rows(min_row=r1, max_row=r2, min_col=c1, max_col=c2):
        for c in row:
            if c.value is not None and not c.font.bold:
                c.font = N

ws = wb.active; ws.title = "About"
for i, (t, f) in enumerate([
        ("CashlessClear: Cashless Claim & Discharge Delay Analysis", T),
        ("Narmada Hospitals (fictional, 3 units) · synthetic data · admissions Jan-Jun 2026", N), ("", N), ("Sheets", B),
        ("Cleaning_Log: what was cleaned in claims_raw.csv", N),
        ("Dept_Map: lookup table used to fix short department names", N),
        ("Clean_Data: 12,000 claims (Excel Table 'claims') + 8 formula columns (hours, IRDAI checks, extra night, order band)", N),
        ("Summary: claim outcome and the key KPIs (COUNTIF / COUNTIFS / AVERAGEIFS)", N),
        ("Analysis: payer & TPA, order time, pre-auth queries, discharge queries, deductions", N), ("", N),
        ("Targets (IRDAI timelines): pre-authorisation decided within 1 hour; final discharge approval within 3 hours.", N)], 1):
    ws.cell(i, 1, t).font = f
ws.column_dimensions["A"].width = 110

cl = wb.create_sheet("Cleaning_Log")
hdr(cl, 1, ["Step", "Issue in claims_raw.csv", "Fix", "Rows affected"])
for r, row in enumerate([(1, "Exact duplicate rows", "Data > Remove Duplicates", 180),
                         (2, "payer_type in wrong case / extra spaces", "TRIM + PROPER; 'Psu' fixed to 'PSU'", 500),
                         (3, "Short department names (Ortho, Cardio, OBG, Onco ...)", "VLOOKUP on Dept_Map, IFERROR keeps correct names", 300),
                         (4, "Result", "12,180 raw rows became 12,000 clean rows", 12000)], 2):
    for c, x in enumerate(row, 1):
        cl.cell(r, c, x).font = N
for col, w in zip("ABCD", [8, 52, 50, 15]):
    cl.column_dimensions[col].width = w

dm = wb.create_sheet("Dept_Map"); hdr(dm, 1, ["Raw name", "Clean name"])
for r, (k, v) in enumerate({"Ortho": "Orthopaedics", "Cardio": "Cardiology", "Surgery": "General Surgery",
                            "Gen Medicine": "General Medicine", "OBG": "Maternity", "Onco": "Oncology"}.items(), 2):
    dm.cell(r, 1, k).font = N; dm.cell(r, 2, v).font = N
dm.column_dimensions["A"].width = 16; dm.column_dimensions["B"].width = 20

cd = wb.create_sheet("Clean_Data")
extra = ["preauth_hours", "preauth_within_1h", "file_prep_hours", "insurer_approval_hours", "final_within_3h",
         "order_to_exit_hours", "extra_night", "order_time_band"]
hdr(cd, 1, list(a.columns) + extra)
n = len(a) + 1
for i, r in enumerate(a.itertuples(index=False), 2):
    cd.append([None if pd.isna(v) else (v.to_pydatetime() if isinstance(v, pd.Timestamp) else (int(v) if isinstance(v, float) and v == int(v) and cd.max_column else v)) for v in r])
    cd.cell(i, 24, f"=ROUND((K{i}-J{i})*24,2)")
    cd.cell(i, 25, f'=IF(X{i}<=1,"Yes","No")')
    cd.cell(i, 26, f'=IF(N{i}="","",ROUND((O{i}-N{i})*24,2))')
    cd.cell(i, 27, f'=IF(N{i}="","",ROUND((P{i}-O{i})*24,2))')
    cd.cell(i, 28, f'=IF(N{i}="","",IF(AA{i}<=3,"Yes","No"))')
    cd.cell(i, 29, f'=IF(N{i}="","",ROUND((Q{i}-N{i})*24,2))')
    cd.cell(i, 30, f'=IF(N{i}="","",IF(INT(Q{i})>INT(N{i}),"Yes","No"))')
    cd.cell(i, 31, f'=IF(N{i}="","",IF(HOUR(N{i})<12,"Before 12:00",IF(HOUR(N{i})<15,"12:00-15:00","After 15:00")))')
for row in cd.iter_rows(min_row=2, max_row=n, min_col=9, max_col=17):
    for c in row:
        if c.column in (9, 10, 11, 14, 15, 16, 17):
            c.number_format = "yyyy-mm-dd hh:mm"
tab = Table(displayName="claims", ref=f"A1:AE{n}"); tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
cd.add_table(tab)
for i in range(1, 32):
    cd.column_dimensions[get_column_letter(i)].width = 17 if i in (9, 10, 11, 14, 15, 16, 17) else 14
cd.freeze_panes = "B2"
C = lambda col: f"Clean_Data!${col}$2:${col}${n}"

su = wb.create_sheet("Summary"); su["A1"] = "Summary KPIs"; su["A1"].font = T
hdr(su, 3, ["Claim status", "Claims", "% of total"])
for k, s in enumerate(["Settled cashless", "Converted to reimbursement"]):
    r = 4 + k; su.cell(r, 1, s)
    su.cell(r, 2, f'=COUNTIF({C("W")},A{r})').number_format = "#,##0"
    su.cell(r, 3, f"=B{r}/SUM($B$4:$B$5)").number_format = "0.0%"
hdr(su, 7, ["KPI", "Value", ""])
kp = [("Pre-auth decided within 1 hour", f'=COUNTIF({C("Y")},"Yes")/COUNTA({C("A")})', "0.0%"),
      ("Average pre-auth hours", f'=AVERAGE({C("X")})', "0.00"),
      ("Final approval within 3 hours (settled)", f'=COUNTIF({C("AB")},"Yes")/B4', "0.0%"),
      ("Average discharge order to exit (hours)", f'=AVERAGE({C("AC")})', "0.00"),
      ("  of which hospital file prep (hours)", f'=AVERAGE({C("Z")})', "0.00"),
      ("  of which insurer approval (hours)", f'=AVERAGE({C("AA")})', "0.00"),
      ("Patients kept an extra night", f'=COUNTIF({C("AD")},"Yes")', "#,##0"),
      ("Deductions as % of bill (settled)", f'=SUM({C("T")})/SUM({C("S")})', "0.0%")]
for k, (lab, f, nf) in enumerate(kp):
    r = 8 + k; su.cell(r, 1, lab); su.cell(r, 2, f).number_format = nf
setn(su, 4, 15, 1, 3)
su.column_dimensions["A"].width = 44; su.column_dimensions["B"].width = 14; su.column_dimensions["C"].width = 12

an = wb.create_sheet("Analysis"); an["A1"] = "Analysis tables"; an["A1"].font = T
r = 3
def block(title, heads):
    global r
    an.cell(r, 1, title).font = B; r += 1; hdr(an, r, heads); r += 1

block("1. Final approval by payer type and TPA (settled claims)", ["Payer type", "Via TPA", "Claims", "Avg approval h", "% within 3h"])
for p, t in [("PSU General Insurer", "Yes"), ("Private General Insurer", "Yes"), ("Private General Insurer", "No"), ("Standalone Health Insurer", "No")]:
    an.cell(r, 1, p); an.cell(r, 2, t)
    an.cell(r, 3, f'=COUNTIFS({C("E")},A{r},{C("F")},B{r},{C("W")},"Settled cashless")').number_format = "#,##0"
    an.cell(r, 4, f'=AVERAGEIFS({C("AA")},{C("E")},A{r},{C("F")},B{r},{C("W")},"Settled cashless")').number_format = "0.00"
    an.cell(r, 5, f'=COUNTIFS({C("E")},A{r},{C("F")},B{r},{C("AB")},"Yes")/C{r}').number_format = "0.0%"; r += 1
r += 1
block("2. Discharge order time vs extra night (settled claims)", ["Order time", "Claims", "Avg order-to-exit h", "Extra nights", "% extra night"])
band_start = r
for s in ["Before 12:00", "12:00-15:00", "After 15:00"]:
    an.cell(r, 1, s)
    an.cell(r, 2, f'=COUNTIF({C("AE")},A{r})').number_format = "#,##0"
    an.cell(r, 3, f'=AVERAGEIFS({C("AC")},{C("AE")},A{r})').number_format = "0.00"
    an.cell(r, 4, f'=COUNTIFS({C("AE")},A{r},{C("AD")},"Yes")').number_format = "#,##0"
    an.cell(r, 5, f"=D{r}/B{r}").number_format = "0.0%"; r += 1
r += 1
block("3. Pre-authorisation by admission type", ["Admission type", "Claims", "With a query", "% with query", "% within 1h"])
for s in ["Planned", "Emergency"]:
    an.cell(r, 1, s)
    an.cell(r, 2, f'=COUNTIF({C("D")},A{r})').number_format = "#,##0"
    an.cell(r, 3, f'=COUNTIFS({C("D")},A{r},{C("M")},">0")').number_format = "#,##0"
    an.cell(r, 4, f"=C{r}/B{r}").number_format = "0.0%"
    an.cell(r, 5, f'=COUNTIFS({C("D")},A{r},{C("Y")},"Yes")/B{r}').number_format = "0.0%"; r += 1
r += 1
block("4. Discharge-stage query vs time to exit (settled claims)", ["Discharge queries", "Claims", "Avg order-to-exit h", "", ""])
for k in [0, 1]:
    an.cell(r, 1, k)
    an.cell(r, 2, f'=COUNTIFS({C("R")},A{r},{C("W")},"Settled cashless")').number_format = "#,##0"
    an.cell(r, 3, f'=AVERAGEIFS({C("AC")},{C("R")},A{r},{C("W")},"Settled cashless")').number_format = "0.00"; r += 1
r += 1
block("5. Deductions (what the patient pays)", ["Deduction reason", "Claims", "Avg bill", "Avg deduction", "% of bill"])
for s in ["Non-payable items", "Room rent capping + non-payable items"]:
    an.cell(r, 1, s)
    an.cell(r, 2, f'=COUNTIF({C("V")},A{r})').number_format = "#,##0"
    an.cell(r, 3, f'=AVERAGEIFS({C("S")},{C("V")},A{r})').number_format = "#,##0"
    an.cell(r, 4, f'=AVERAGEIFS({C("T")},{C("V")},A{r})').number_format = "#,##0"
    an.cell(r, 5, f'=SUMIFS({C("T")},{C("V")},A{r})/SUMIFS({C("S")},{C("V")},A{r})').number_format = "0.0%"; r += 1
setn(an, 3, r, 1, 5)
for col, w in zip("ABCDE", [38, 12, 18, 18, 14]):
    an.column_dimensions[col].width = w
ch = BarChart(); ch.type = "col"; ch.title = "% of patients kept an extra night, by discharge order time"; ch.style = 10
ch.add_data(Reference(an, min_col=5, min_row=band_start - 1, max_row=band_start + 2), titles_from_data=True)
ch.set_categories(Reference(an, min_col=1, min_row=band_start, max_row=band_start + 2))
ch.legend = None; ch.y_axis.numFmt = "0%"; ch.height = 8; ch.width = 15
ch.roundedCorners = False; ch.x_axis.delete = False; ch.y_axis.delete = False; ch.title.overlay = False
an.add_chart(ch, "G3")
wb.save("02_excel/CashlessClear_Analysis.xlsx"); print("saved")
