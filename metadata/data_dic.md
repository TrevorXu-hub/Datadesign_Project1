# Data Dictionary

## clients

| Name | Data Type | Description | Example |
|---|---|---|---|
| `client_id` | integer | Unique identifier for each client. | `1` |
| `sex` | integer | Encoded sex variable from the source dataset. | `2` |
| `education` | integer | Encoded education level from the source dataset. | `2` |
| `marriage` | integer | Encoded marital status from the source dataset. | `1` |
| `age` | integer | Age of the client in years. | `24` |

## credit_accounts

| Name | Data Type | Description | Example |
|---|---|---|---|
| `client_id` | integer | Unique identifier linking the account to the client table. | `1` |
| `limit_bal` | integer | Amount of given credit for the client account. | `20000` |
| `default_next_month` | binary | Indicates whether the client defaulted on payment next month. | `1` |

## repayment_history

| Name | Data Type | Description | Example |
|---|---|---|---|
| `client_id` | integer | Unique identifier linking the record to the client table. | `1` |
| `month_index` | integer | Relative month index for the repayment record, where 1 is the most recent month and 6 is the least recent month. | `1` |
| `repayment_status` | integer | Monthly repayment status code indicating repayment delay or payment condition. | `2` |

## monthly_financials

| Name | Data Type | Description | Example |
|---|---|---|---|
| `client_id` | integer | Unique identifier linking the record to the client table. | `1` |
| `month_index` | integer | Relative month index for the financial record, where 1 is the most recent month and 6 is the least recent month. | `1` |
| `bill_amount` | numeric | Monthly bill statement amount for the client. | `3913` |
| `pay_amount` | numeric | Monthly payment amount made by the client. | `689` |