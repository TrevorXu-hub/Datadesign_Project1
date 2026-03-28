# DS 4320 Project 1: Predicting Credit Card Default Risk with the UCI Credit Card Default Dataset

## Executive Summary

This project studies whether demographic information, credit limit, repayment history, and monthly financial behavior can predict whether a credit card client will default on payment next month. I use the UCI Credit Card Default dataset, restructure the original wide data into four relational tables, load those tables into DuckDB, use SQL to build a client-level modeling table, and then train a random forest classifier. This repository includes the write-up, processed data links, background reading, metadata, SQL scripts, Python scripts, pipeline files, and a press release.

## Name

Trevor (Zilu) Xu

## NetID

pxg6af

## DOI

`<ADD_ZENODO_DOI_HERE>`

## Press Release

- [Press Release](press_release/press_release.md)

## Data

- [UVA OneDrive Data Folder](https://myuva-my.sharepoint.com/:f:/r/personal/pxg6af_virginia_edu/Documents/DataDesign_Project1?csf=1&web=1&e=IQ4uOR)
- [Raw Data Folder](data_raw/)
- [Processed Data Folder](data_processed/)

## Pipeline

- [Jupyter Notebook Pipeline](pipeline/project1_pipeline.ipynb)
- [Markdown Export of Pipeline](pipeline/project1_pipeline.md)

## License

This project is licensed under the [MIT License](LICENSE).

---

## Problem Definition

### Initial General Problem

How can financial and behavioral information be used to understand and predict credit default risk?

### Refined Specific Problem Statement

Using the UCI Credit Card Default dataset, this project predicts whether a client will default on payment next month based on demographic variables, account credit limit, repayment behavior, and monthly financial records from the previous six months.

### Rationale for Refinement

The general problem of predicting loan default risk is too broad because it could apply to many different borrower groups, lending settings, and kinds of repayment data. I narrowed the project to one public dataset with a clear target variable and a clear six-month history of repayment, billing, and payment behavior. This makes the project easier to document, easier to reproduce, and better suited to the relational model required for the assignment.

### Motivation

Default prediction matters because missed payments create risk for lenders and often reflect real financial stress. I wanted to see whether recent repayment behavior is more useful than simple background variables for identifying future default risk. This topic also fits the course well because it lets me combine relational data design, SQL feature engineering, and machine learning in one project.

### Press Release Headline

[New Model Helps Identify Which Credit Card Clients Are More Likely to Default](press_release/press_release.md)

---

## Domain Exposition

### Terminology

| Term | Meaning |
|---|---|
| Default | Failure to make a required payment. |
| Credit Risk | The risk that a borrower or client will not repay as expected. |
| Credit Limit | The amount of credit available to the client. |
| Repayment Status | A coded monthly indicator showing payment delay or repayment condition. |
| Bill Amount | The monthly statement amount owed by the client. |
| Payment Amount | The amount actually paid in a given month. |
| Feature Engineering | Turning raw data into useful model inputs. |
| Recall | The share of actual default cases correctly identified by the model. |
| ROC AUC | A metric showing how well the model separates default and non-default clients. |

### Domain Background

This project is in the area of consumer finance and credit risk. In this setting, lenders use repayment behavior, account information, and other financial signals to estimate whether a client is likely to default in the future. The main idea in this project is that recent repayment and payment patterns may tell us more about default risk than basic demographic variables alone.

### Background Reading

Background readings are stored in the [background_reading/](background_reading/) folder.

### Background Reading Summary

| Title | Brief Description | File in Folder | Source |
|---|---|---|---|
| Credit (FDIC) | Basic background on how consumer credit works and why repayment matters. | [<ADD_FILE_NAME>](background_reading/<ADD_FILE_NAME>) | [FDIC Credit](https://www.fdic.gov/credit) |
| Credit Reports and Scores (CFPB) | Explains how credit reports and scores are used and why payment history matters. | [<ADD_FILE_NAME>](background_reading/<ADD_FILE_NAME>) | [CFPB Credit Reports and Scores](https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores) |
| Default of Credit Card Clients (UCI Machine Learning Repository) | Gives the dataset description, variable information, and target definition for this project. | [<ADD_FILE_NAME>](background_reading/<ADD_FILE_NAME>) | [UCI Dataset Page](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) |

---

## Data Creation

### Raw Data Acquisition and Provenance

The raw dataset comes from the UCI Credit Card Default dataset. The source data were stored as a wide table, where each client had one row and monthly repayment, bill, and payment variables appeared across multiple columns. For this project, I used a separate Python script to restructure the data into four relational tables so the data would match the required relational model.

### Code Used to Create the Data

| File | Description | Link |
|---|---|---|
| `scr/create_tables.py` | Loads the raw data, renames the ID field, reshapes repeated monthly variables, and saves processed tables. | [scr/create_tables.py](scr/create_tables.py) |
| `sql/create_tables.sql` | Defines the SQL table structure used in the DuckDB workflow. | [sql/create_tables.sql](sql/create_tables.sql) |
| `sql/load_tables.sql` | Loads processed CSV files into DuckDB. | [sql/load_tables.sql](sql/load_tables.sql) |
| `sql/feature_queries.sql` | Builds the final modeling table from the relational tables. | [sql/feature_queries.sql](sql/feature_queries.sql) |

### Bias Identification

Bias can enter this project in several ways. The dataset comes from a specific setting and does not represent every borrower population. Demographic variables such as sex, education, and marriage may reflect social patterns that are not the same as actual repayment ability. Repayment history is useful, but it may also reflect larger structural constraints that are not directly measured in the dataset.

### Bias Mitigation

To reduce overreliance on simple background variables, the project emphasizes repayment and financial behavior features. I also report several evaluation metrics instead of using accuracy alone. In the write-up, I treat the model as a prediction tool for analysis, not as a complete or neutral decision rule.

### Rationale for Critical Decisions

A key decision in this project was to split the original wide dataset into four relational tables. This made the monthly structure easier to work with and easier to explain. Another important decision was to aggregate monthly repayment and financial history into client-level features before modeling, since the target variable is defined at the client level. I used a random forest classifier because it can pick up nonlinear patterns and interactions without requiring a simple linear relationship.

---

## Metadata

### Schema ER Diagram

- [ER Diagram](metadata/er_diagram.png)

### Data Table

| Table Name | Description | CSV File |
|---|---|---|
| `clients` | Stores client-level demographic information. | [clients.csv](data_processed/clients.csv) |
| `credit_accounts` | Stores account-level summary variables, including credit limit and the target variable. | [credit_accounts.csv](data_processed/credit_accounts.csv) |
| `repayment_history` | Stores monthly repayment status for each client across six months. | [repayment_history.csv](data_processed/repayment_history.csv) |
| `monthly_financials` | Stores monthly bill and payment amounts for each client across six months. | [monthly_financials.csv](data_processed/monthly_financials.csv) |

### Data Dictionary

A full copy is also stored in [metadata/data_dictionary.md](metadata/data_dictionary.md).

#### clients

| Name | Data Type | Description | Example |
|---|---|---|---|
| `client_id` | integer | Unique identifier for each client. | `1` |
| `sex` | integer | Encoded sex variable from the source dataset. | `2` |
| `education` | integer | Encoded education level from the source dataset. | `2` |
| `marriage` | integer | Encoded marital status from the source dataset. | `1` |
| `age` | integer | Age of the client in years. | `24` |

#### credit_accounts

| Name | Data Type | Description | Example |
|---|---|---|---|
| `client_id` | integer | Unique identifier linking the account to the client table. | `1` |
| `limit_bal` | integer | Amount of given credit for the client account. | `20000` |
| `default_next_month` | binary | Whether the client defaulted on payment next month. | `1` |

#### repayment_history

| Name | Data Type | Description | Example |
|---|---|---|---|
| `client_id` | integer | Unique identifier linking the record to the client table. | `1` |
| `month_index` | integer | Relative month index, where 1 is the most recent month and 6 is the least recent month. | `1` |
| `repayment_status` | integer | Monthly repayment status code indicating repayment delay or payment condition. | `2` |

#### monthly_financials

| Name | Data Type | Description | Example |
|---|---|---|---|
| `client_id` | integer | Unique identifier linking the record to the client table. | `1` |
| `month_index` | integer | Relative month index, where 1 is the most recent month and 6 is the least recent month. | `1` |
| `bill_amount` | numeric | Monthly bill statement amount for the client. | `3913` |
| `pay_amount` | numeric | Monthly payment amount made by the client. | `689` |

### Data Dictionary Quantification of Uncertainty for Numerical Features

A full copy can also be stored in [metadata/numerical_uncertainty.md](metadata/numerical_uncertainty.md).

| Variable | Table | Mean | Std | Min | Max | Uncertainty Note |
|---|---|---:|---:|---:|---:|---|
| `age` | `clients` | 35.486 | 9.218 | 21 | 79 | Age is stable, but it is only an indirect indicator of financial risk. |
| `limit_bal` | `credit_accounts` | 167484.323 | 129747.662 | 10000 | 1000000 | Credit limit reflects both client profile and lender policy. |
| `repayment_status` | `repayment_history` | -0.182 | 1.166 | -2 | 8 | This is a coded measure of repayment condition, so it compresses more complex behavior into one number. |
| `bill_amount` | `monthly_financials` | 44976.950 | 66834.430 | -339603 | 1664089 | Bill amounts vary a lot across clients and months and may reflect temporary spikes. |
| `pay_amount` | `monthly_financials` | `<ADD_MEAN>` | `<ADD_STD>` | `<ADD_MIN>` | `<ADD_MAX>` | Payment amounts can change a lot from month to month. |

---

## Results Summary

The final random forest model produced the following results on the test set:

| Metric | Value |
|---|---:|
| Accuracy | 0.747 |
| Precision | 0.449 |
| Recall | 0.625 |
| F1 Score | 0.523 |
| ROC AUC | 0.766 |

The model shows moderate predictive performance. Recall is more important than accuracy here because the project is trying to identify clients who may default. The feature importance results also show that repayment-history variables matter most.

### Top Features

| Feature | Importance |
|---|---:|
| `delayed_month_count` | 0.244863 |
| `max_repayment_status` | 0.226357 |
| `avg_repayment_status` | 0.179348 |
| `avg_pay_amount` | 0.084459 |
| `avg_payment_bill_ratio` | 0.075865 |
| `avg_bill_amount` | 0.069826 |
| `limit_bal` | 0.066381 |
| `age` | 0.030043 |
| `education` | 0.011631 |
| `marriage` | 0.005619 |

---

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── data_raw/
├── data_processed/
├── background_reading/
├── metadata/
├── sql/
├── scr/
├── pipeline/
├── figures/
└── press_release/