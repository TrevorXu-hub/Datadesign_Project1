# Numerical Feature Uncertainty

| Variable | Table | Mean | Std | Min | Max | Uncertainty Note |
|---|---|---:|---:|---:|---:|---|
| `age` | `clients` | 35.486 | 9.218 | 21 | 79 | Age is a stable demographic variable, but it is only an indirect indicator of financial risk and repayment capacity. |
| `limit_bal` | `credit_accounts` | 167484.323 | 129747.662 | 10000 | 1000000 | Credit limit reflects both client profile and lender policy, so it does not measure repayment ability directly. |
| `repayment_status` | `repayment_history` | -0.182 | 1.166 | -2 | 8 | Repayment status is an encoded summary of payment delay. It is useful for modeling, but the numeric coding compresses complex repayment behavior into a single value. |
| `bill_amount` | `monthly_financials` | 44976.950 | 66834.430 | -339603 | 1664089 | Bill amounts vary substantially across months and clients. Extreme values may reflect temporary spending spikes, adjustments, or account timing effects rather than long-term financial stress alone. |