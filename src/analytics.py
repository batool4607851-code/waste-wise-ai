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


def calculate_group_waste_rates(
    df: pd.DataFrame,
    group_column: str,
    production_column: str,
    waste_column: str,
) -> pd.DataFrame:
    """Calculate waste rate for each product, line, shift, or category."""

    grouped = (
        df.groupby(group_column)
        .agg(
            production=(production_column, "sum"),
            waste=(waste_column, "sum"),
        )
        .reset_index()
    )

    grouped["waste_rate"] = (
        grouped["waste"]
        / grouped["production"]
        * 100
    ).fillna(0)

    return grouped.sort_values(
        "waste_rate",
        ascending=False,
    )
