# 03_sql

PostgreSQL 16 (pgAdmin 4 or psql).

| File | What it does |
| --- | --- |
| [`01_schema.sql`](01_schema.sql) | Creates `claims` and `insurer_queries` (primary key, foreign key) |
| [`02_load.sql`](02_load.sql) | Loads the two clean CSVs and counts rows |
| [`03_analysis.sql`](03_analysis.sql) | 12 business questions: outcomes, 1-hour and 3-hour compliance, query reasons, where discharge time goes, payer / TPA comparison, cost of a query, order time vs extra night, beds blocked, deductions, room-rent capping, monthly MIS |
| [`results.md`](results.md) | Output of every query |

SQL used: `GROUP BY`, `CASE WHEN`, a CTE (`WITH`), `INTERVAL` comparisons, `EXTRACT(EPOCH ...)` and `EXTRACT(HOUR ...)`, date casting (`::date`), `SUM(...) OVER ()` for % of total, `NULLIF`.
