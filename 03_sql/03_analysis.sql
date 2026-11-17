-- CashlessClear: business questions answered in SQL
-- IRDAI timelines used as targets: cashless pre-authorisation decided within 1 hour of the request,
-- final discharge approval within 3 hours of the hospital's request.

-- Q1. How do cashless claims end?
SELECT claim_status,
       COUNT(*) AS claims,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM claims
GROUP BY claim_status;

-- Q2. Pre-authorisation: how many are decided within 1 hour?
SELECT COUNT(*) AS claims,
       ROUND(AVG(EXTRACT(EPOCH FROM (preauth_decided_at - preauth_requested_at)) / 3600), 2) AS avg_hours,
       ROUND(100.0 * SUM(CASE WHEN preauth_decided_at - preauth_requested_at <= INTERVAL '1 hour' THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS pct_within_1h
FROM claims;

-- Q3. Pre-authorisation by admission type: query rate and 1-hour compliance
SELECT admission_type,
       COUNT(*) AS claims,
       ROUND(100.0 * SUM(CASE WHEN preauth_queries > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_with_query,
       ROUND(100.0 * SUM(CASE WHEN preauth_decided_at - preauth_requested_at <= INTERVAL '1 hour' THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS pct_within_1h
FROM claims
GROUP BY admission_type;

-- Q4. Why do insurers raise queries? (both stages)
SELECT query_stage, query_reason,
       COUNT(*) AS queries,
       ROUND(AVG(EXTRACT(EPOCH FROM (answered_at - raised_at)) / 3600), 1) AS avg_hours_for_hospital_to_answer
FROM insurer_queries
GROUP BY query_stage, query_reason
ORDER BY query_stage, queries DESC;

-- Q5. Where does discharge time go? (settled cashless claims)
WITH d AS (
    SELECT EXTRACT(EPOCH FROM (discharge_file_sent_at - discharge_ordered_at)) / 3600 AS hospital_prep,
           EXTRACT(EPOCH FROM (final_approval_at - discharge_file_sent_at)) / 3600 AS insurer_approval,
           EXTRACT(EPOCH FROM (patient_left_at - final_approval_at)) / 3600 AS payment_and_exit,
           EXTRACT(EPOCH FROM (patient_left_at - discharge_ordered_at)) / 3600 AS total
    FROM claims
    WHERE claim_status = 'Settled cashless'
)
SELECT ROUND(AVG(hospital_prep), 2) AS hospital_file_prep_h,
       ROUND(AVG(insurer_approval), 2) AS insurer_approval_h,
       ROUND(AVG(payment_and_exit), 2) AS payment_and_exit_h,
       ROUND(AVG(total), 2) AS order_to_exit_h,
       ROUND(100.0 * AVG(hospital_prep) / AVG(total), 1) AS hospital_prep_pct
FROM d;

-- Q6. Final approval within 3 hours, by payer type and TPA
SELECT payer_type, via_tpa,
       COUNT(*) AS claims,
       ROUND(AVG(EXTRACT(EPOCH FROM (final_approval_at - discharge_file_sent_at)) / 3600), 2) AS avg_approval_h,
       ROUND(100.0 * SUM(CASE WHEN final_approval_at - discharge_file_sent_at <= INTERVAL '3 hours' THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS pct_within_3h
FROM claims
WHERE claim_status = 'Settled cashless'
GROUP BY payer_type, via_tpa
ORDER BY avg_approval_h DESC;

-- Q7. How much does a discharge-stage query cost the patient in time?
SELECT discharge_queries,
       COUNT(*) AS claims,
       ROUND(AVG(EXTRACT(EPOCH FROM (patient_left_at - discharge_ordered_at)) / 3600), 2) AS avg_order_to_exit_h
FROM claims
WHERE claim_status = 'Settled cashless'
GROUP BY discharge_queries
ORDER BY discharge_queries;

-- Q8. Does the time of the discharge order matter? (extra night = patient leaves the next day or later)
SELECT CASE WHEN EXTRACT(HOUR FROM discharge_ordered_at) < 12 THEN '1) Before 12:00'
            WHEN EXTRACT(HOUR FROM discharge_ordered_at) < 15 THEN '2) 12:00-15:00'
            ELSE '3) After 15:00' END AS order_time,
       COUNT(*) AS claims,
       ROUND(AVG(EXTRACT(EPOCH FROM (patient_left_at - discharge_ordered_at)) / 3600), 2) AS avg_order_to_exit_h,
       SUM(CASE WHEN patient_left_at::date > discharge_ordered_at::date THEN 1 ELSE 0 END) AS extra_nights,
       ROUND(100.0 * SUM(CASE WHEN patient_left_at::date > discharge_ordered_at::date THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS pct_extra_night
FROM claims
WHERE claim_status = 'Settled cashless'
GROUP BY 1
ORDER BY 1;

-- Q9. Beds blocked by discharge delay, by hospital
SELECT hospital,
       COUNT(*) AS discharges,
       SUM(CASE WHEN patient_left_at::date > discharge_ordered_at::date THEN 1 ELSE 0 END) AS extra_bed_nights,
       ROUND(AVG(EXTRACT(EPOCH FROM (patient_left_at - discharge_ordered_at)) / 3600), 2) AS avg_order_to_exit_h,
       ROUND(AVG(discharge_ordered_at::date - admitted_at::date), 1) AS avg_length_of_stay_days
FROM claims
WHERE claim_status = 'Settled cashless'
GROUP BY hospital
ORDER BY extra_bed_nights DESC;

-- Q10. Deductions: what the patient pays out of pocket
SELECT deduction_reason,
       COUNT(*) AS claims,
       ROUND(AVG(billed_amount)) AS avg_bill,
       ROUND(AVG(deduction_amount)) AS avg_deduction,
       ROUND(100.0 * SUM(deduction_amount) / SUM(billed_amount), 1) AS deduction_pct_of_bill
FROM claims
WHERE claim_status = 'Settled cashless'
GROUP BY deduction_reason;

-- Q11. Which policies hit room-rent capping?
SELECT policy_type, room_category,
       COUNT(*) AS claims,
       ROUND(100.0 * SUM(CASE WHEN deduction_reason LIKE 'Room rent%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_room_rent_capped
FROM claims
WHERE claim_status = 'Settled cashless'
GROUP BY policy_type, room_category
ORDER BY pct_room_rent_capped DESC;

-- Q12. Monthly MIS for the insurance desk
SELECT TO_CHAR(admitted_at, 'YYYY-MM') AS month,
       COUNT(*) AS claims,
       ROUND(100.0 * SUM(CASE WHEN preauth_decided_at - preauth_requested_at <= INTERVAL '1 hour' THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS preauth_within_1h_pct,
       ROUND(100.0 * SUM(CASE WHEN final_approval_at - discharge_file_sent_at <= INTERVAL '3 hours' THEN 1 ELSE 0 END)
             / NULLIF(SUM(CASE WHEN claim_status = 'Settled cashless' THEN 1 ELSE 0 END), 0), 1) AS final_within_3h_pct,
       ROUND(AVG(EXTRACT(EPOCH FROM (patient_left_at - discharge_ordered_at)) / 3600), 2) AS avg_order_to_exit_h
FROM claims
GROUP BY 1
ORDER BY 1;
