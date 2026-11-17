-- Run in psql from the repo root. In pgAdmin: right-click each table > Import/Export Data,
-- choose the CSV, tick Header, and leave NULL strings blank.
\copy claims FROM '01_data/claims_clean.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy insurer_queries FROM '01_data/insurer_queries.csv' WITH (FORMAT csv, HEADER true, NULL '')

SELECT 'claims' AS table_name, COUNT(*) FROM claims
UNION ALL
SELECT 'insurer_queries', COUNT(*) FROM insurer_queries;
