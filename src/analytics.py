import pandas as pd


def calculate_basic_metrics(df: pd.DataFrame) -> dict:
    """Calculate basic dataset metrics."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def calculate_waste_kpis(
    df: pd.DataFrame,
    production_column: str,
    waste_column: str,
) -> dict:
    """Calculate core production and waste KPIs."""

    production = pd.to_numeric(
        df[production_column], errors="coerce"
    ).sum()

    waste = pd.to_numeric(
        df[waste_column], errors="coerce"
    ).sum()

    waste_rate = (waste / production * 100) if production else 0

    return {
        "total_production": int(production),
        "total_waste": int(waste),
        "waste_rate": float(waste_rate),
    }

def get_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for numeric columns."""
    return df.describe().T
