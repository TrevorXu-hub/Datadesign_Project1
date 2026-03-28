# DS 4320 Project 1 Pipeline: Predicting Credit Card Default Risk

This notebook presents the end-to-end pipeline for the credit default prediction project. It loads relational tables into DuckDB, uses SQL to create a modeling table, performs exploratory analysis, trains machine learning models, and evaluates model performance.

## Research Question
Can demographic information, credit limit, billing history, and repayment behavior from the previous six months predict whether a client will default next month?

## Import Libraries

```python
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report, roc_curve,
    ConfusionMatrixDisplay
)
```

## Connect to DuckDB

```python
con = duckdb.connect("credit_default.duckdb")
with open("../sql/load_tables.sql", "r") as f:
    load_sql = f.read()

con.execute(load_sql)
```

## Data Preparation and Relational Restructuring

The original dataset was stored as a wide table with repeated monthly variables. A separate Python script (`scr/create_tables.py`) was used to restructure the raw data into four relational tables:

- `clients`
- `credit_accounts`
- `repayment_history`
- `monthly_financials`

This notebook begins from those processed tables and loads them into DuckDB for SQL-based feature engineering and modeling.

```python
con.sql("SELECT * FROM clients LIMIT 5").df()
```

```python
con.sql("SELECT * FROM credit_accounts LIMIT 5").df()
```

```python
con.sql("SELECT * FROM monthly_financials LIMIT 5").df()
```

```python
con.sql("SELECT * FROM repayment_history LIMIT 5").df()
```

```python
clients = pd.read_csv("/workspaces/Datadesign_Project1/data_processed/clients.csv")
credit_accounts = pd.read_csv("/workspaces/Datadesign_Project1/data_processed/credit_accounts.csv")
repayment_history = pd.read_csv("/workspaces/Datadesign_Project1/data_processed/repayment_history.csv")
monthly_financials = pd.read_csv("/workspaces/Datadesign_Project1/data_processed/monthly_financials.csv")

clients["age"].agg(["mean", "std", "min", "max"])
```

```python
credit_accounts["limit_bal"].agg(["mean", "std", "min", "max"])
```

```python
repayment_history["repayment_status"].agg(["mean", "std", "min", "max"])
```

```python
monthly_financials["bill_amount"].agg(["mean", "std", "min", "max"])
```

## Making the Main Modeling Table

Right now we have 4 seperate tables, which are record the clients information, the account status, the repayment history and the monthly_financials, but we do not need all the information for sovling our question, also we need to summarize some features to one features, like for features: bill_amt1...bill_amt6, pay_amt1...pay_amt6. We only need the average. So I am doing the feature queries here, to join the tables by primary keys, and summarize some features, and drops some features to make a new final table.

```python
con.execute(open("../sql/feature_queries.sql").read())
```

```python
con.sql("SELECT * FROM modeling_table LIMIT 5").df()
```

The modeling table aggregates the monthly repayment and financial history into client-level features so that each row corresponds to one client.

## Loading the Table to Pandas and Check the Data Quality

```python
Model_df = con.sql("SELECT * FROM modeling_table").df()
Model_df.head()
```

```python
Model_df.isna().sum()
```

The only feature contain missing value is "avg_payment_bill_ratio", which is a feature i made for the modeling table. If one client do not need to pay any for the bill, the ratio will be zero. So this kind of missing value will not effect model a lot.

```python
Model_df["default_next_month"].value_counts()
```

```python
Model_df["default_next_month"].value_counts(normalize=True)
```

## Describative Analysis

```python
Model_df["default_next_month"].mean()
```

```python
Model_df.groupby("delayed_month_count")["default_next_month"].mean()
```

```python
Model_df.groupby("max_repayment_status")["default_next_month"].mean()
```

```python
delay_default = (
    Model_df.groupby("delayed_month_count")["default_next_month"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(delay_default["delayed_month_count"], delay_default["default_next_month"])
plt.xlabel("Number of Delayed Months")
plt.ylabel("Default Rate")
plt.title("Default Rate by Number of Delayed Months")
plt.tight_layout()
plt.savefig("figures", dpi=300)
plt.show()
```

Clients with more delayed months tend to have a higher probability to default next month.

## Train Test Split

```python
X = Model_df.drop(columns=["client_id", "default_next_month"])
y = Model_df["default_next_month"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

## Train the Model

```python
rf_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    min_samples_split=10,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)
```

```python
y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)[:, 1]
```

## Model Evaulation

```python
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

results_df = pd.DataFrame({
    "Metric": ["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"],
    "Value": [accuracy, precision, recall, f1, roc_auc]
})

results_df
```

The random forest model achieved an accuracy of 0.747, a precision of 0.449, a recall of 0.625, an F1 score of 0.523, and a ROC AUC of 0.766. These results suggest that the model has moderate predictive performance overall and is meaningfully better than random classification.

Among these metrics, recall is especially important in this project because the goal is to identify clients at risk of default. A recall of 0.625 means that the model correctly identifies about 62.5% of actual default cases. This indicates that the model is reasonably effective at detecting higher-risk clients, although it still misses a portion of them.

The ROC AUC of 0.766 shows that the model has a good overall ability to distinguish between default and non-default clients. While the precision of 0.449 indicates that the model also produces false positives, the results are still useful for risk screening, where identifying more potentially risky clients may be preferable to missing too many true defaults.


```python
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

## Confusion Matrix

```python
fig, ax = plt.subplots(figsize=(6, 5))
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax)
ax.set_title("Confusion Matrix: Random Forest")
plt.tight_layout()
plt.savefig("../figures/confusion_matrix_random_forest.png", dpi=300)
plt.show()
```

## ROC Curve

```python
fpr, tpr, thresholds = roc_curve(y_test, y_prob)

plt.figure(figsize=(8, 5))
plt.plot(fpr, tpr, label=f"Random Forest (AUC = {roc_auc:.3f})")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.tight_layout()
plt.savefig("../figures/roc_curve_random_forest.png", dpi=300)
plt.show()
```

## Future Importance

```python
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": rf_model.feature_importances_
}).sort_values("importance", ascending=False)

feature_importance.head(10)
```

```python
top_features = feature_importance.head(10).sort_values("importance")

plt.figure(figsize=(8, 6))
plt.barh(top_features["feature"], top_features["importance"])
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Random Forest Feature Importances")
plt.tight_layout()
plt.savefig("../figures/feature_importance_random_forest.png", dpi=300)
plt.show()
```

The feature importance results show that repayment-related variables are the strongest predictors in the model. The three most important features are `delayed_month_count` (0.245), `max_repayment_status` (0.226), and `avg_repayment_status` (0.179). This suggests that recent repayment behavior carries the most predictive information about whether a client will default next month.

Financial summary variables such as `avg_pay_amount`, `avg_payment_bill_ratio`, `avg_bill_amount`, and `limit_bal` also contribute to prediction, but their importance is noticeably lower than the repayment-history features. In contrast, demographic variables such as `education`, `marriage`, and `age` play a much smaller role in the model.

Overall, these results support the idea that recent behavioral signals are more informative than static background characteristics in predicting credit default risk.

## Discussion

The model results support the main idea of this project: recent repayment behavior is one of the strongest indicators of future default risk. Clients with more delayed months, worse repayment status, and weaker payment patterns are more likely to default in the following month. This is consistent with the financial logic of the problem, since recent payment difficulties often reflect growing financial stress.

These results also validate the relational data design used in the project. The original dataset stored repeated monthly information in a wide format, but restructuring it into relational tables made it easier to summarize repayment and financial history into client-level features. In this sense, the data design directly supported the modeling process.

At the same time, the model is not perfect. The recall is stronger than the precision, which means the model is better at identifying true default cases than at avoiding false alarms. For a credit risk setting, this may still be acceptable, since missing true high-risk clients can be more costly than flagging some lower-risk clients incorrectly.

## Conclusion

This project shows that demographic information, account information, repayment history, and monthly financial behavior can be used together to predict whether a client will default next month. Using the UCI Credit Card Default dataset, I first restructured the original wide table into relational tables, then used DuckDB and SQL to create a client-level modeling table, and finally trained a random forest classifier.

The final model achieved moderate predictive performance, with a ROC AUC of 0.766 and a recall of 0.625. The most important predictors were all related to repayment history, especially delayed months and repayment status. Overall, the project demonstrates how relational data design, SQL-based feature engineering, and machine learning can work together to support credit risk prediction.
