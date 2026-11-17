# SQL results

Run on PostgreSQL 16 against the clean data (12,000 claims, 6,581 insurer queries).

## Q1. How do cashless claims end?

```
        claim_status        | claims | pct  
----------------------------+--------+------
 Settled cashless           |  11565 | 96.4
 Converted to reimbursement |    435 |  3.6
(2 rows)
```

## Q2. Pre-authorisation: how many are decided within 1 hour?

```
 claims | avg_hours | pct_within_1h 
--------+-----------+---------------
  12000 |      2.79 |          50.5
(1 row)
```

## Q3. Pre-authorisation by admission type: query rate and 1-hour compliance

```
 admission_type | claims | pct_with_query | pct_within_1h 
----------------+--------+----------------+---------------
 Planned        |   5345 |           20.2 |          55.5
 Emergency      |   6655 |           35.4 |          46.5
(2 rows)
```

## Q4. Why do insurers raise queries? (both stages)

```
    query_stage    |              query_reason               | queries | avg_hours_for_hospital_to_answer 
-------------------+-----------------------------------------+---------+----------------------------------
 Final discharge   | Discharge summary incomplete            |     819 |                              3.4
 Final discharge   | Itemised bill breakup missing           |     722 |                              3.3
 Final discharge   | Implant / pharmacy invoice missing      |     474 |                              3.4
 Final discharge   | Final investigation reports missing     |     417 |                              3.4
 Pre-authorisation | Investigation reports missing           |    1602 |                              4.9
 Pre-authorisation | Doctor's notes / treatment plan unclear |    1142 |                              4.8
 Pre-authorisation | Policy / KYC copy missing               |     824 |                              5.0
 Pre-authorisation | Past medical history asked              |     581 |                              5.0
(8 rows)
```

## Q5. Where does discharge time go? (settled cashless claims)

```
 hospital_file_prep_h | insurer_approval_h | payment_and_exit_h | order_to_exit_h | hospital_prep_pct 
----------------------+--------------------+--------------------+-----------------+-------------------
                 2.85 |               3.01 |               1.73 |            7.59 |              37.6
(1 row)
```

## Q6. Final approval within 3 hours, by payer type and TPA

```
        payer_type         | via_tpa | claims | avg_approval_h | pct_within_3h 
---------------------------+---------+--------+----------------+---------------
 PSU General Insurer       | Yes     |   3246 |           4.20 |          48.2
 Private General Insurer   | Yes     |   1823 |           3.55 |          56.1
 Private General Insurer   | No      |   1904 |           2.52 |          75.1
 Standalone Health Insurer | No      |   4592 |           2.15 |          80.6
(4 rows)
```

## Q7. How much does a discharge-stage query cost the patient in time?

```
 discharge_queries | claims | avg_order_to_exit_h 
-------------------+--------+---------------------
                 0 |   9133 |                6.40
                 1 |   2432 |               12.03
(2 rows)
```

## Q8. Does the time of the discharge order matter? (extra night = patient leaves the next day or later)

```
   order_time    | claims | avg_order_to_exit_h | extra_nights | pct_extra_night 
-----------------+--------+---------------------+--------------+-----------------
 1) Before 12:00 |   3854 |                5.97 |          182 |             4.7
 2) 12:00-15:00  |   4700 |                6.88 |          682 |            14.5
 3) After 15:00  |   3011 |               10.76 |         1644 |            54.6
(3 rows)
```

## Q9. Beds blocked by discharge delay, by hospital

```
 hospital | discharges | extra_bed_nights | avg_order_to_exit_h | avg_length_of_stay_days 
----------+------------+------------------+---------------------+-------------------------
 Nagpur   |       4629 |             1016 |                7.61 |                     4.3
 Pune     |       4064 |              872 |                7.53 |                     4.3
 Nashik   |       2872 |              620 |                7.62 |                     4.3
(3 rows)
```

## Q10. Deductions: what the patient pays out of pocket

```
           deduction_reason            | claims | avg_bill | avg_deduction | deduction_pct_of_bill 
---------------------------------------+--------+----------+---------------+-----------------------
 Non-payable items                     |  10171 |   109198 |          6015 |                   5.5
 Room rent capping + non-payable items |   1394 |   107719 |         25992 |                  24.1
(2 rows)
```

## Q11. Which policies hit room-rent capping?

```
 policy_type | room_category | claims | pct_room_rent_capped 
-------------+---------------+--------+----------------------
 Retail      | Single Room   |   2346 |                 59.4
 Group       | General Ward  |   1217 |                  0.0
 Group       | Single Room   |   1236 |                  0.0
 Group       | Twin Sharing  |   1569 |                  0.0
 Retail      | General Ward  |   2170 |                  0.0
 Retail      | Twin Sharing  |   3027 |                  0.0
(6 rows)
```

## Q12. Monthly MIS for the insurance desk

```
  month  | claims | preauth_within_1h_pct | final_within_3h_pct | avg_order_to_exit_h 
---------+--------+-----------------------+---------------------+---------------------
 2026-01 |   2073 |                  51.0 |                67.4 |                7.55
 2026-02 |   1818 |                  51.2 |                66.7 |                7.63
 2026-03 |   2073 |                  47.9 |                66.0 |                7.69
 2026-04 |   2002 |                  51.1 |                67.8 |                7.39
 2026-05 |   1972 |                  49.6 |                66.8 |                7.52
 2026-06 |   2062 |                  52.2 |                65.7 |                7.72
(6 rows)
```
