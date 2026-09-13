import pandas as pd


def calculate_waste_kpis(df, production_column, waste_column):
    production = pd.to_numeric(
        df[production_column],
        errors="coerce"
    ).fillna(0)

    waste = pd.to_numeric(
        df[waste_column],
        errors="coerce"
    ).fillna(0)

    total_production = production.sum()
    total_waste = waste.sum()

    waste_rate = (
        (total_waste / total_production) * 100
        if total_production > 0
        else 0
    )

    return {
        "total_production": total_production,
        "total_waste": total_waste,
        "waste_rate": waste_rate,
    }


def calculate_group_waste_rates(
    df,
    group_column,
    production_column,
    waste_column,
):
    if group_column not in df.columns:
        return pd.DataFrame()

    grouped = df.groupby(
        group_column,
        dropna=False
    ).agg(
        production=(production_column, "sum"),
        waste=(waste_column, "sum"),
    ).reset_index()

    grouped["waste_rate"] = (
        grouped["waste"] / grouped["production"] * 100
    ).where(
        grouped["production"] > 0,
        0
    )

    return grouped.sort_values(
        "waste_rate",
        ascending=False
    )


def calculate_top_waste_reasons(
    df,
    reason_column="event_reason",
    waste_column="loss_quantity",
    top_n=10,
    waste_reason_column=None,
):
    if waste_reason_column is not None:
        reason_column = waste_reason_column

    if reason_column not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby(
            reason_column,
            dropna=False
        )[waste_column]
        .sum()
        .reset_index()
        .sort_values(
            waste_column,
            ascending=False
        )
        .head(top_n)
    )

    return result


def loss_by_dimension(
    df,
    dimension,
    loss_column="loss_quantity",
):
    if (
        dimension not in df.columns
        or loss_column not in df.columns
    ):
        return pd.DataFrame()

    return (
        df.groupby(
            dimension,
            dropna=False
        )[loss_column]
        .sum()
        .reset_index()
        .sort_values(
            loss_column,
            ascending=False
        )
    )


def loss_by_product(
    df,
    loss_column="loss_quantity",
):
    return loss_by_dimension(
        df,
        "product",
        loss_column,
    )


def loss_by_line(
    df,
    loss_column="loss_quantity",
):
    return loss_by_dimension(
        df,
        "production_line",
        loss_column,
    )


def loss_by_shift(
    df,
    loss_column="loss_quantity",
):
    return loss_by_dimension(
        df,
        "shift",
        loss_column,
    )


def loss_by_process(
    df,
    loss_column="loss_quantity",
):
    return loss_by_dimension(
        df,
        "process",
        loss_column,
    )


def loss_by_reason(
    df,
    loss_column="loss_quantity",
):
    return loss_by_dimension(
        df,
        "event_reason",
        loss_column,
    )


def loss_trend(
    df,
    date_column="date",
    loss_column="loss_quantity",
):
    if (
        date_column not in df.columns
        or loss_column not in df.columns
    ):
        return pd.DataFrame()

    trend = df.copy()

    trend[date_column] = pd.to_datetime(
        trend[date_column],
        errors="coerce",
    )

    trend = trend.dropna(
        subset=[date_column]
    )

    return (
        trend.groupby(date_column)[loss_column]
        .sum()
        .reset_index()
        .sort_values(date_column)
    )


def investigation_priorities(
    df,
    loss_column="loss_quantity",
    top_n=10,
):
    dimensions = [
        column
        for column in [
            "product",
            "production_line",
            "shift",
            "process",
            "event_reason",
        ]
        if column in df.columns
    ]

    if (
        not dimensions
        or loss_column not in df.columns
    ):
        return pd.DataFrame()

    result = (
        df.groupby(
            dimensions,
            dropna=False
        )[loss_column]
        .sum()
        .reset_index()
        .sort_values(
            loss_column,
            ascending=False
        )
        .head(top_n)
    )

    result.insert(
        0,
        "priority_rank",
        range(1, len(result) + 1),
    )

    return result
