# 9. UAT test cases

| TC | Requirement | Steps | Expected result | Result |
| --- | --- | --- | --- | --- |
| TC-01 | BR-01 | Admit a Cardiology patient → open pre-auth form | Cardiology checklist shown | |
| TC-02 | BR-01 | Leave the echo report unattached → click Send | Sending blocked; "Echo report missing" shown | |
| TC-03 | BR-01 | Sign an ECG report in the hospital system → open pre-auth form | ECG report already attached | |
| TC-04 | BR-02 | Discharge summary unsigned → click Send to insurer | Sending blocked; "Discharge summary incomplete" | |
| TC-05 | BR-02 | Bill with knee implant charges → prepare file | Implant invoice listed as required | |
| TC-06 | BR-03 | Doctor marks patient "expected discharge tomorrow" at 19:00 | Patient appears on medical records' list | |
| TC-07 | BR-03 | Run night job for listed patients | Provisional bills ready by 08:00 | |
| TC-08 | BR-04 | Send pre-auth, wait 45 minutes without a decision | Claim shown in amber on tracker | |
| TC-09 | BR-04 | Final approval pending for 3 h 5 min | Claim shown in red | |
| TC-10 | BR-04 | Let the hourly check run on the red claim | Escalation email sent with claim ID and request time | |
| TC-11 | BR-05 | Admit retail-policy patient to a single room above the limit | Limit and estimated deduction shown; acknowledgement saved | |
| TC-12 | BR-06 | Open last month's payer scorecard | % within 3 h per insurer / TPA matches the data | |
| TC-13 | BR-07 | Send a test pre-auth through the NHCX sandbox | Request accepted and acknowledgement received | |

Result column is filled during UAT (Pass / Fail + defect ID).
