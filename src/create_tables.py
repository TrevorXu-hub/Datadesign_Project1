import logging
from pathlib import Path

import pandas as pd


# ----------------------------
# Project paths
# ----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data_raw" / "default_of_credit_card_clients.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data_processed"
LOG_PATH = PROJECT_ROOT / "project1.log"


# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ----------------------------
# Load raw data
# ----------------------------
def load_raw_data(file_path: Path) -> pd.DataFrame:
    """
    Load the raw CSV dataset.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded raw data from {file_path}")
        print("Raw columns:", df.columns.tolist())
        return df
    except FileNotFoundError:
        logger.error(f"Raw data file not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading raw data: {e}")
        raise


# ----------------------------
# Standardize column names
# ----------------------------
def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename only the ID column so the schema uses client_id consistently.
    """
    rename_map = {
        "id": "client_id"
    }

    df = df.rename(columns=rename_map)
    logger.info("Standardized column names")
    return df


# ----------------------------
# Create clients table
# ----------------------------
def create_clients_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the clients table with demographic variables.
    """
    clients = df[[
        "client_id",
        "sex",
        "education",
        "marriage",
        "age"
    ]].copy()

    logger.info("Created clients table")
    return clients


# ----------------------------
# Create credit_accounts table
# ----------------------------
def create_credit_accounts_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the credit_accounts table with account-level variables.
    """
    credit_accounts = df[[
        "client_id",
        "limit_bal",
        "default_next_month"
    ]].copy()

    logger.info("Created credit_accounts table")
    return credit_accounts


# ----------------------------
# Create repayment_history table
# ----------------------------
def create_repayment_history_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert wide repayment status columns into a long repayment history table.
    """
    repayment_columns = ["pay_0", "pay_2", "pay_3", "pay_4", "pay_5", "pay_6"]

    repayment_history = df[["client_id"] + repayment_columns].melt(
        id_vars="client_id",
        value_vars=repayment_columns,
        var_name="source_month",
        value_name="repayment_status"
    )

    month_map = {
        "pay_0": 1,
        "pay_2": 2,
        "pay_3": 3,
        "pay_4": 4,
        "pay_5": 5,
        "pay_6": 6
    }

    repayment_history["month_index"] = repayment_history["source_month"].map(month_map)

    repayment_history = repayment_history[[
        "client_id",
        "month_index",
        "repayment_status"
    ]].sort_values(["client_id", "month_index"])

    logger.info("Created repayment_history table")
    return repayment_history


# ----------------------------
# Create monthly_financials table
# ----------------------------
def create_monthly_financials_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert wide bill and payment columns into a long monthly financials table.
    """
    bill_columns = [
        "bill_amt1", "bill_amt2", "bill_amt3",
        "bill_amt4", "bill_amt5", "bill_amt6"
    ]
    pay_columns = [
        "pay_amt1", "pay_amt2", "pay_amt3",
        "pay_amt4", "pay_amt5", "pay_amt6"
    ]

    bills_long = df[["client_id"] + bill_columns].melt(
        id_vars="client_id",
        value_vars=bill_columns,
        var_name="bill_month",
        value_name="bill_amount"
    )

    pays_long = df[["client_id"] + pay_columns].melt(
        id_vars="client_id",
        value_vars=pay_columns,
        var_name="pay_month",
        value_name="pay_amount"
    )

    bill_month_map = {
        "bill_amt1": 1,
        "bill_amt2": 2,
        "bill_amt3": 3,
        "bill_amt4": 4,
        "bill_amt5": 5,
        "bill_amt6": 6
    }

    pay_month_map = {
        "pay_amt1": 1,
        "pay_amt2": 2,
        "pay_amt3": 3,
        "pay_amt4": 4,
        "pay_amt5": 5,
        "pay_amt6": 6
    }

    bills_long["month_index"] = bills_long["bill_month"].map(bill_month_map)
    pays_long["month_index"] = pays_long["pay_month"].map(pay_month_map)

    bills_long = bills_long[["client_id", "month_index", "bill_amount"]]
    pays_long = pays_long[["client_id", "month_index", "pay_amount"]]

    monthly_financials = pd.merge(
        bills_long,
        pays_long,
        on=["client_id", "month_index"],
        how="inner"
    ).sort_values(["client_id", "month_index"])

    logger.info("Created monthly_financials table")
    return monthly_financials


# ----------------------------
# Save output tables
# ----------------------------
def save_table(df: pd.DataFrame, file_stem: str, output_dir: Path) -> None:
    """
    Save a dataframe as both CSV and Parquet.
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)

        csv_path = output_dir / f"{file_stem}.csv"
        parquet_path = output_dir / f"{file_stem}.parquet"

        df.to_csv(csv_path, index=False)
        df.to_parquet(parquet_path, index=False)

        logger.info(f"Saved table: {csv_path}")
        logger.info(f"Saved table: {parquet_path}")
    except Exception as e:
        logger.error(f"Error saving table {file_stem}: {e}")
        raise


# ----------------------------
# Main pipeline
# ----------------------------
def main() -> None:
    """
    Load raw data, create relational tables, and save them.
    """
    logger.info("Starting create_tables.py")

    raw_df = load_raw_data(RAW_DATA_PATH)
    raw_df = standardize_column_names(raw_df)

    print("Renamed columns:", raw_df.columns.tolist())

    clients = create_clients_table(raw_df)
    credit_accounts = create_credit_accounts_table(raw_df)
    repayment_history = create_repayment_history_table(raw_df)
    monthly_financials = create_monthly_financials_table(raw_df)

    save_table(clients, "clients", PROCESSED_DATA_DIR)
    save_table(credit_accounts, "credit_accounts", PROCESSED_DATA_DIR)
    save_table(repayment_history, "repayment_history", PROCESSED_DATA_DIR)
    save_table(monthly_financials, "monthly_financials", PROCESSED_DATA_DIR)

    logger.info("Finished building all processed tables")
    print("Done. Processed tables saved to:", PROCESSED_DATA_DIR)


if __name__ == "__main__":
    main()