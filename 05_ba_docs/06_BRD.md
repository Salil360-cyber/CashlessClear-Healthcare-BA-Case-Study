# Business Requirements Document (BRD)

**Project:** CashlessClear: Faster Cashless Claims and Discharge · **Organisation:** Narmada Hospitals (fictional) · **Version:** 1.0 (Draft) · **Prepared by:** Salil Gokhale, Business Analyst

> Case study on synthetic data. Stakeholders and sign-offs are simulated.

## 1. Background

Narmada Hospitals runs three multispeciality hospitals (Nagpur, Pune, Nashik). For cashless patients, the insurance desk requests pre-authorisation at admission and final approval at discharge from the insurer, directly or through a TPA. IRDAI's Master Circular on Health Insurance (May 2024) sets 1 hour for cashless decisions and 3 hours for final discharge approval; the hospital uses these as targets.

## 2. Problem statement

From January to June 2026, 50.5% of 12,000 pre-authorisations were decided within 1 hour and 66.8% of final approvals came within 3 hours. Patients waited 7.6 hours on average from discharge order to exit, and 2,508 were kept an extra night. 37.6% of the wait is the hospital's own file preparation, and most insurer queries ask for documents the hospital already holds.

## 3. Objectives

1. Average discharge order-to-exit under 6 hours (from 7.6).
2. Extra bed-nights under 1,900 per six months (from 2,508).
3. Pre-auth decided within 1 hour for at least 65% (from 50.5%).

All within 6 months of launch.

## 4. Scope

**In scope:** pre-auth and discharge checklists; discharge planning; live tracker, escalation and MIS; room-rent check at admission; payer scorecard; NHCX (next phase).
**Out of scope:** insurer / TPA rules; tariffs and packages; reimbursement claims; clinical decisions; hospital system replacement.

## 5. Stakeholders

COO (sponsor, Accountable); Insurance desk manager, Billing, IT / HIS and Business Analyst (Responsible); Doctors, Medical records, Nursing, Insurers / TPAs (Consulted); Patients and families (Informed). Full RACI: [02_stakeholders_raci.md](02_stakeholders_raci.md).

## 6. Current process (AS-IS)

Pre-auth request with manually collected documents → insurer query if incomplete → treatment → discharge order (often afternoon) → file built after the order → insurer query if incomplete → final approval → patient pays the difference and leaves, or stays the night if it is after 22:00. Flow: [03_process_flows.md](03_process_flows.md).

## 7. Data findings

| # | Finding | Value |
| --- | --- | --- |
| 1 | Pre-auth decided within 1 hour | 50.5% (avg 2.79 h) |
| 2 | Pre-auths with a query: emergency vs planned | 35.4% vs 20.2% |
| 3 | Top pre-auth query reason | Investigation reports missing (1,602 of 4,149) |
| 4 | Discharge order to exit | 7.59 h: hospital file 2.85 h, insurer 3.01 h, payment & exit 1.73 h |
| 5 | Final approval within 3 hours | 66.8% (PSU + TPA 48.2%, standalone health insurers 80.6%) |
| 6 | Effect of a discharge-stage query | 12.03 h vs 6.40 h order-to-exit |
| 7 | Extra night: order after 15:00 vs before 12:00 | 54.6% vs 4.7% (2,508 extra nights in total) |
| 8 | Room-rent capped claims | 24.1% of the bill deducted (vs 5.5%); 59.4% of retail single-room claims |

Source: [03_sql/results.md](../03_sql/results.md), matched in the Excel workbook.

## 8. Business requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| BR-01 | The system shall show a pre-auth checklist by department and attach signed investigation reports automatically; sending is blocked until the checklist is complete. | Must |
| BR-02 | The system shall block sending the discharge file until the signed summary, itemised bill, implant / pharmacy invoices and final reports are attached. | Must |
| BR-03 | Doctors shall be able to mark expected discharges the evening before; the system shall list them for medical records and create provisional bills by 08:00. | Must |
| BR-04 | The insurance desk shall see a live tracker of each claim's 1-hour and 3-hour clocks, with automatic escalation to the insurer / TPA and a daily MIS report. | Must |
| BR-05 | At admission, the desk shall show the policy's room-rent limit and an estimated deduction, and record the patient's acknowledgement. | Should |
| BR-06 | Management shall receive a monthly approval-time scorecard by insurer and TPA. | Should |
| BR-07 | The hospital shall exchange claims through NHCX. | Could |

User stories and acceptance criteria: [07_user_stories.md](07_user_stories.md).

## 9. Non-functional requirements

| Area | Requirement |
| --- | --- |
| Performance | Tracker refreshes at least every 5 minutes; checklist check in under 3 seconds |
| Security and privacy | Patient documents encrypted; access by role; follows the hospital's health data privacy policy |
| Audit | Every sent file, query and escalation is logged with time and user |
| Availability | Insurance desk tools available 24x7 |
| Reporting | Daily MIS ready by 08:00 |

## 10. Assumptions

- The hospital information system can expose signed reports and bills to the desk tool.
- Doctors agree to mark expected discharges on the evening round.
- Insurers and TPAs accept escalation emails at a named contact.

## 11. Constraints

- IRDAI rules and each policy's terms apply; the hospital cannot change insurer decisions.
- Patient data privacy rules apply to all documents shared.

## 12. Risks and mitigation

| Risk | Mitigation |
| --- | --- |
| Doctors resist evening marking | Pilot in two departments; show extra-night numbers per ward |
| Checklist slows urgent emergency pre-auths | Emergency mode: send with minimum documents, rest within 2 hours |
| Integration with the hospital system takes long | Phase 1 manual checklist; auto-attach in phase 2 |
| Insurers ignore escalations | Use the payer scorecard in quarterly insurer reviews |

## 13. Success KPIs

% pre-auth within 1 h · % final approval within 3 h · average order-to-exit hours · extra bed-nights · query rate by reason · room-rent complaints.

## 14. Expected impact

Counting only discharge planning and the discharge checklist: about 604 bed-nights freed (room for about 140 more admissions, about Rs 1.5 crore billing) and about 1,216 fewer discharge queries per six months. Details: [10_ROI_estimate.md](10_ROI_estimate.md).

## 15. Appendix

RTM: [08_RTM.csv](08_RTM.csv) · UAT: [09_UAT_test_cases.md](09_UAT_test_cases.md) · Data dictionary: [01_data/DATA_DICTIONARY.md](../01_data/DATA_DICTIONARY.md)

**Sign-off (simulated):** COO · Insurance desk manager · Medical Superintendent
