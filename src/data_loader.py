import pandas as pd


SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".xls")


def load_data(file):
    """Load CSV or Excel data into a pandas DataFrame."""
    filename = file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file)
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
    else:
        raise ValueError(
            "Unsupported file type. Please upload a CSV, XLSX, or XLS file."
        )

    if df.empty:
        raise ValueError("The uploaded file is empty.")

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def validate_data(df):
    """Return basic validation information for the uploaded dataset."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "columns": list(df.columns),
    }
