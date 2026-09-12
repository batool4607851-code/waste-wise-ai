
import re
import pandas as pd


CANONICAL_FIELDS = {
    "date": [
        "date",
        "production_date",
        "manufacturing_date",
        "timestamp",
    ],
    "product": [
        "product",
        "product_name",
        "sku",
        "item",
        "item_name",
    ],
    "batch": [
        "batch",
        "batch_id",
        "batch_number",
        "lot",
        "lot_number",
    ],
    "production_line": [
        "line",
        "production_line",
        "line_name",
        "line_id",
    ],
    "shift": [
        "shift",
        "shift_name",
        "work_shift",
    ],
    "production_quantity": [
        "production_quantity",
        "production_qty",
        "produced_quantity",
        "produced_qty",
        "output_quantity",
        "output_qty",
        "production_kg",
        "output_kg",
    ],
    "event_type": [
        "event_type",
        "loss_type",
        "event_category",
        "category",
    ],
    "event_reason": [
        "event_reason",
        "waste_reason",
        "loss_reason",
        "reason",
        "waste_cause",
        "loss_cause",
    ],
    "affected_quantity": [
        "affected_quantity",
        "affected_qty",
        "affected_kg",
    ],
    "loss_quantity": [
        "loss_quantity",
        "loss_qty",
        "waste_quantity",
        "waste_qty",
        "waste_kg",
        "loss_kg",
    ],
    "rework_quantity": [
        "rework_quantity",
        "rework_qty",
        "rework_kg",
    ],
    "recovered_quantity": [
        "recovered_quantity",
        "recovered_qty",
        "recovered_kg",
    ],
    "final_loss_quantity": [
        "final_loss_quantity",
        "final_loss_qty",
        "final_loss_kg",
        "disposed_quantity",
        "disposed_qty",
    ],
    "disposition": [
        "disposition",
        "disposition_status",
        "outcome",
        "final_disposition",
    ],
    "unit_cost": [
        "unit_cost",
        "cost_per_unit",
        "cost_per_kg",
        "unit_price",
    ],
    "rework_cost": [
        "rework_cost",
        "rework_expense",
    ],
    "loss_cost": [
        "loss_cost",
        "waste_cost",
        "loss_expense",
    ],
    "quality_parameter": [
        "quality_parameter",
        "quality_metric",
        "parameter",
        "qc_parameter",
    ],
    "quality_value": [
        "quality_value",
        "measured_value",
        "qc_value",
        "measurement",
    ],
    "quality_status": [
        "quality_status",
        "qc_status",
        "quality_result",
        "qc_result",
    ],
}


REQUIRED_FOR_BASIC_ANALYSIS = [
    "production_quantity",
    "loss_quantity",
]


def normalize_name(name):
    """Normalize a source column name for comparison."""
    value = str(name).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _build_alias_lookup():
    lookup = {}

    for canonical, aliases in CANONICAL_FIELDS.items():
        for alias in aliases:
            lookup[normalize_name(alias)] = canonical

    return lookup


ALIAS_LOOKUP = _build_alias_lookup()


def suggest_mapping(df):
    """
    Suggest mappings from source columns to canonical WasteWise fields.

    Exact normalized alias matches receive high confidence.
    Keyword matches receive lower confidence.
    """
    suggestions = {}

    for column in df.columns:
        normalized = normalize_name(column)

        if normalized in ALIAS_LOOKUP:
            canonical = ALIAS_LOOKUP[normalized]

            suggestions[column] = {
                "canonical_field": canonical,
                "confidence": "high",
                "reason": "Exact alias match",
            }
            continue

        matches = []

        for canonical, aliases in CANONICAL_FIELDS.items():
            for alias in aliases:
                alias_normalized = normalize_name(alias)

                if (
                    alias_normalized in normalized
                    or normalized in alias_normalized
                ):
                    matches.append(canonical)

        matches = list(dict.fromkeys(matches))

        if len(matches) == 1:
            suggestions[column] = {
                "canonical_field": matches[0],
                "confidence": "medium",
                "reason": "Keyword similarity",
            }

        elif len(matches) > 1:
            suggestions[column] = {
                "canonical_field": None,
                "confidence": "ambiguous",
                "reason": f"Possible matches: {', '.join(matches)}",
            }

        else:
            suggestions[column] = {
                "canonical_field": None,
                "confidence": "none",
                "reason": "No reliable mapping found",
            }

    return suggestions


def apply_mapping(df, mapping):
    """
    Apply a confirmed source-column -> canonical-field mapping.

    mapping format:
        {
            "source_column": "canonical_field"
        }
    """
    rename_map = {}

    for source_column, canonical_field in mapping.items():
        if source_column not in df.columns:
            continue

        if canonical_field not in CANONICAL_FIELDS:
            continue

        rename_map[source_column] = canonical_field

    normalized_df = df.rename(columns=rename_map).copy()

    return normalized_df


def validate_mapping(df):
    """Report required, available, and missing canonical fields."""
    available = [
        field
        for field in CANONICAL_FIELDS
        if field in df.columns
    ]

    missing_required = [
        field
        for field in REQUIRED_FOR_BASIC_ANALYSIS
        if field not in df.columns
    ]

    return {
        "available_fields": available,
        "missing_required_fields": missing_required,
        "basic_analysis_supported": len(missing_required) == 0,
    }


def normalize_data_types(df):
    """Normalize numeric and date fields when they are available."""
    result = df.copy()

    numeric_fields = [
        "production_quantity",
        "affected_quantity",
        "loss_quantity",
        "rework_quantity",
        "recovered_quantity",
        "final_loss_quantity",
        "unit_cost",
        "rework_cost",
        "loss_cost",
        "quality_value",
    ]

    for field in numeric_fields:
        if field in result.columns:
            result[field] = pd.to_numeric(
                result[field],
                errors="coerce",
            )

    if "date" in result.columns:
        result["date"] = pd.to_datetime(
            result["date"],
            errors="coerce",
        )

    return result


def prepare_data(df, mapping):
    """
    Apply confirmed mapping and normalize data types.
    """
    normalized_df = apply_mapping(df, mapping)
    normalized_df = normalize_data_types(normalized_df)

    validation = validate_mapping(normalized_df)

    return normalized_df, validation
