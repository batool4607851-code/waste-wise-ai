import pandas as pd


def load_data(file):
    """Load CSV or Excel data into a pandas DataFrame."""
    filename = file.name.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(file)

    if filename.endswith(".xlsx"):
        return pd.read_excel(file)

    raise ValueError("Unsupported file type. Please upload a CSV or XLSX file.")
