CREATE OR REPLACE TABLE clients AS
SELECT * FROM read_csv_auto('../data_processed/clients.csv');

CREATE OR REPLACE TABLE credit_accounts AS
SELECT * FROM read_csv_auto('../data_processed/credit_accounts.csv');

CREATE OR REPLACE TABLE repayment_history AS
SELECT * FROM read_csv_auto('../data_processed/repayment_history.csv');

CREATE OR REPLACE TABLE monthly_financials AS
SELECT * FROM read_csv_auto('../data_processed/monthly_financials.csv');