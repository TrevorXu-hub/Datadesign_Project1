CREATE OR REPLACE TABLE modeling_table AS
WITH repayment_features AS (
    SELECT
        client_id,
        MAX(repayment_status) AS max_repayment_status,
        AVG(repayment_status) AS avg_repayment_status,
        SUM(CASE WHEN repayment_status > 0 THEN 1 ELSE 0 END) AS delayed_month_count
    FROM repayment_history
    GROUP BY client_id
),
financial_features AS (
    SELECT
        client_id,
        AVG(bill_amount) AS avg_bill_amount,
        AVG(pay_amount) AS avg_pay_amount,
        CASE
            WHEN AVG(bill_amount) = 0 THEN NULL
            ELSE AVG(pay_amount) / AVG(bill_amount)
        END AS avg_payment_bill_ratio
    FROM monthly_financials
    GROUP BY client_id
)
SELECT
    c.client_id,
    c.sex,
    c.education,
    c.marriage,
    c.age,
    a.limit_bal,
    a.default_next_month,
    r.max_repayment_status,
    r.avg_repayment_status,
    r.delayed_month_count,
    f.avg_bill_amount,
    f.avg_pay_amount,
    f.avg_payment_bill_ratio
FROM clients c
JOIN credit_accounts a
    ON c.client_id = a.client_id
JOIN repayment_features r
    ON c.client_id = r.client_id
JOIN financial_features f
    ON c.client_id = f.client_id;