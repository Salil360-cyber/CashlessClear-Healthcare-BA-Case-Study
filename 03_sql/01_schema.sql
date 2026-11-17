-- CashlessClear: PostgreSQL schema
DROP TABLE IF EXISTS insurer_queries;
DROP TABLE IF EXISTS claims;

CREATE TABLE claims (
    claim_id               VARCHAR(10) PRIMARY KEY,
    hospital               VARCHAR(20),
    department             VARCHAR(25),
    admission_type         VARCHAR(10),     -- Planned / Emergency
    payer_type             VARCHAR(30),
    via_tpa                VARCHAR(3),      -- Yes / No
    policy_type            VARCHAR(10),     -- Retail / Group
    room_category          VARCHAR(15),
    admitted_at            TIMESTAMP,
    preauth_requested_at   TIMESTAMP,
    preauth_decided_at     TIMESTAMP,
    preauth_outcome        VARCHAR(10),     -- Approved / Denied
    preauth_queries        SMALLINT,
    discharge_ordered_at   TIMESTAMP,       -- doctor signs the discharge order
    discharge_file_sent_at TIMESTAMP,       -- hospital sends final bill + papers to insurer
    final_approval_at      TIMESTAMP,       -- insurer approves the final amount
    patient_left_at        TIMESTAMP,
    discharge_queries      SMALLINT,
    billed_amount          INTEGER,
    deduction_amount       INTEGER,
    approved_amount        INTEGER,
    deduction_reason       VARCHAR(40),
    claim_status           VARCHAR(30)      -- Settled cashless / Converted to reimbursement
);

CREATE TABLE insurer_queries (
    query_id      VARCHAR(10) PRIMARY KEY,
    claim_id      VARCHAR(10) REFERENCES claims(claim_id),
    query_stage   VARCHAR(20),              -- Pre-authorisation / Final discharge
    query_reason  VARCHAR(45),
    raised_at     TIMESTAMP,
    answered_at   TIMESTAMP
);
