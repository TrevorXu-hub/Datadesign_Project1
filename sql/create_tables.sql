CREATE OR REPLACE TABLE clients (
    client_id INTEGER,
    sex INTEGER,
    education INTEGER,
    marriage INTEGER,
    age INTEGER
);

CREATE OR REPLACE TABLE credit_accounts (
    client_id INTEGER,
    limit_bal INTEGER,
    default_next_month INTEGER
);

CREATE OR REPLACE TABLE repayment_history (
    client_id INTEGER,
    month_index INTEGER,
    repayment_status INTEGER
);

CREATE OR REPLACE TABLE monthly_financials (
    client_id INTEGER,
    month_index INTEGER,
    bill_amount DOUBLE,
    pay_amount DOUBLE
);
