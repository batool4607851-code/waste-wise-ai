import pandas as pd


def calculate_basic_metrics(df: pd.DataFrame) -> dict:
    """Calculate basic dataset metrics."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def get_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for numeric columns."""
    return df.describe().T
