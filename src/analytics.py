import pandas as pd


def calculate_basic_metrics(df: pd.DataFrame) -> dict:
    """Calculate basic production and waste metrics."""
    metrics = {
        "rows": len(df),
        "columns": len(df.columns),
    }

    return metrics
