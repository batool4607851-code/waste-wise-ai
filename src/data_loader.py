import pandas as pd
from pypdf import PdfReader

from src.data_mapper import normalize_name


def clean_columns(df):
    df = df.copy()
    df.columns = [
        normalize_name(column)
        for column in df.columns
    ]
    return df


def load_data(file):
    filename = file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file)

    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)

    elif filename.endswith(".pdf"):

        reader = PdfReader(file)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        pdf_text = "\n".join(text).strip()

        if not pdf_text:
            raise ValueError(
                "No readable text was found in the PDF."
            )

        lines = [
            line.strip()
            for line in pdf_text.splitlines()
            if line.strip()
        ]

        rows = []

        for line in lines:

            parts = line.split()

            if len(parts) < 8:
                continue

            try:
                production = float(parts[-2])
                waste = float(parts[-1])

            except ValueError:
                continue

            date = parts[0]
            product = parts[1]
            line_name = parts[2]
            shift = parts[3]
            process = parts[4]
            reason = " ".join(parts[5:-2])

            rows.append({
                "date": date,
                "product": product,
                "line": line_name,
                "shift": shift,
                "process": process,
                "waste_reason": reason,
                "production_kg": production,
                "waste_kg": waste,
            })

        if not rows:
            raise ValueError(
                "Could not extract structured production data from the PDF."
            )

        df = pd.DataFrame(rows)

    else:
        raise ValueError(
            "Unsupported file type. Please upload CSV, XLSX, XLS, or PDF."
        )

    if df.empty:
        raise ValueError(
            "The uploaded file contains no data."
        )

    return clean_columns(df)


def validate_data(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(
            df.isna().sum().sum()
        ),
        "duplicate_rows": int(
            df.duplicated().sum()
        ),
        "column_names": list(df.columns),
    }
