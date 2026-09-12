%%writefile /content/waste-wise-ai/src/data_loader.py

import pandas as pd
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".xls", ".pdf")


def load_data(file):
    """Load CSV/Excel data or extract text from a PDF."""
    filename = file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file)

        if df.empty:
            raise ValueError("The uploaded file is empty.")

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return df

    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)

        if df.empty:
            raise ValueError("The uploaded file is empty.")

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return df

    elif filename.endswith(".pdf"):
        reader = PdfReader(file)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        pdf_text = "\n\n".join(text).strip()

        if not pdf_text:
            raise ValueError("No readable text was found in the PDF.")

        return pdf_text

    else:
        raise ValueError(
            "Unsupported file type. Please upload a CSV, XLSX, XLS, or PDF file."
        )


def validate_data(df):
    """Return basic validation information for tabular data."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "columns": list(df.columns),
    }
