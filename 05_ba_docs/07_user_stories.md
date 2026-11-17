# 7. User stories and acceptance criteria

**Epic E1: Complete documents first time** · **Epic E2: Planned, faster discharge** · **Epic E3: Visibility and patient communication**

| ID | Epic | User story | Priority |
| --- | --- | --- | --- |
| US-01 | E1 | As an insurance desk executive, I want a pre-auth checklist for the patient's department, so that I send a complete request the first time. | Must |
| US-02 | E1 | As an insurance desk executive, I want investigation reports attached automatically from the hospital system, so that I do not have to collect them by hand. | Must |
| US-03 | E1 | As a billing executive, I want a discharge file checklist that blocks sending until every document is attached, so that the insurer does not raise a query. | Must |
| US-04 | E2 | As a doctor, I want to mark a patient as "expected discharge tomorrow" on my evening round, so that the file can be prepared overnight. | Must |
| US-05 | E2 | As a medical records officer, I want a list of tomorrow's expected discharges, so that I can complete the draft discharge summaries tonight. | Must |
| US-06 | E3 | As the insurance desk manager, I want a live list of claims with their 1-hour / 3-hour clocks, so that I can chase delays before they breach. | Must |
| US-07 | E3 | As the insurance desk manager, I want an automatic escalation email to the insurer or TPA when a final approval passes 3 hours, so that delays are flagged with evidence. | Must |
| US-08 | E3 | As a patient, I want to know my room-rent limit and likely deductions at admission, so that I can choose a room and am not surprised at discharge. | Should |
| US-09 | E3 | As the COO, I want a monthly scorecard of approval times by insurer and TPA, so that I can raise delays in insurer reviews. | Should |
| US-10 | E1 | As an IT lead, I want claims sent through NHCX, so that requests and approvals move in a standard digital format. | Could |

## Acceptance criteria (Given-When-Then)

**US-01 Pre-auth checklist**
- Given the patient is admitted to Cardiology, when the desk opens the pre-auth form, then the checklist shows the documents needed for Cardiology (e.g. ECG, echo report, doctor's treatment plan, policy and KYC copy).
- Given a checklist item is missing, when the executive clicks Send, then sending is blocked and the missing item is named.

**US-02 Auto-attach reports**
- Given an investigation report is signed in the hospital system, when the pre-auth form is opened, then the report is already attached.

**US-03 Discharge file checklist**
- Given the discharge summary is not signed, when billing clicks Send to insurer, then sending is blocked with "Discharge summary incomplete".
- Given the bill has implant charges, when the file is prepared, then the implant invoice is a required item.

**US-04 / US-05 Discharge planning**
- Given a doctor marks a patient "expected discharge tomorrow" before 20:00, when medical records opens the list, then the patient appears with the draft summary task.
- Given the patient is on the list, when billing runs the night job, then a provisional bill is ready by 08:00.

**US-06 Live tracker**
- Given a pre-auth request was sent 45 minutes ago without a decision, when the tracker refreshes, then the claim is shown in amber.
- Given a final approval request is older than 3 hours, then the claim is shown in red.

**US-07 Escalation**
- Given a final approval passes 3 hours, when the hourly check runs, then an escalation email goes to the insurer / TPA contact with the claim ID and request time.

**US-08 Room-rent check**
- Given a retail policy with a room-rent limit below the chosen room's rate, when the patient is admitted, then the desk shows the limit and an estimated deduction, and the patient's acknowledgement is recorded.
