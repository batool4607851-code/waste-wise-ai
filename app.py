import streamlit as st

from src.data_loader import load_data, validate_data
from src.analytics import (
    calculate_waste_kpis,
    calculate_group_waste_rates,
    calculate_top_waste_reasons,
)

st.set_page_config(
    page_title="WasteWise AI",
    page_icon="♻️",
    layout="wide",
)

st.title("♻️ WasteWise AI")
st.subheader("Turn factory data into actionable waste intelligence.")
st.divider()

uploaded_file = st.file_uploader(
    "Upload factory data or documents",
    type=["csv", "xlsx", "xls", "pdf"],
)

if uploaded_file:
    try:
        file_name = uploaded_file.name.lower()

        if file_name.endswith(".pdf"):
            pdf_text = load_data(uploaded_file)

            st.success("PDF uploaded successfully.")

            st.subheader("Document Preview")
            st.text_area(
                "Extracted PDF text",
                pdf_text,
                height=400,
            )

            st.info(
                "PDF text extraction is working. "
                "AI document reasoning will be added in a later phase."
            )

        else:
            df = load_data(uploaded_file)
            validation = validate_data(df)

            st.success("File uploaded successfully.")

            st.subheader("Data Preview")
            st.dataframe(
                df.head(10),
                use_container_width=True,
            )

            st.subheader("Dataset Information")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Rows", validation["rows"])
            col2.metric("Columns", validation["columns"])
            col3.metric("Missing Values", validation["missing_values"])
            col4.metric("Duplicate Rows", validation["duplicate_rows"])

            st.divider()

            numeric_columns = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if len(numeric_columns) >= 2:

                st.subheader("Waste KPI Dashboard")

                production_column = st.selectbox(
                    "Production column",
                    numeric_columns,
                )

                waste_options = [
                    column
                    for column in numeric_columns
                    if column != production_column
                ]

                waste_column = st.selectbox(
                    "Waste column",
                    waste_options,
                )

                kpis = calculate_waste_kpis(
                    df,
                    production_column,
                    waste_column,
                )

                kpi1, kpi2, kpi3 = st.columns(3)

                kpi1.metric(
                    "Total Production",
                    f"{kpis['total_production']:,}",
                )

                kpi2.metric(
                    "Total Waste",
                    f"{kpis['total_waste']:,}",
                )

                kpi3.metric(
                    "Waste Rate",
                    f"{kpis['waste_rate']:.2f}%",
                )

                st.divider()

                st.subheader("Waste Rate Analysis")

                group_options = [
                    column
                    for column in df.columns
                    if column not in [
                        production_column,
                        waste_column,
                    ]
                ]

                if group_options:

                    group_column = st.selectbox(
                        "Group analysis by",
                        group_options,
                    )

                    if st.button("Analyze Waste Rates"):

                        result = calculate_group_waste_rates(
                            df,
                            group_column=group_column,
                            production_column=production_column,
                            waste_column=waste_column,
                        )

                        st.dataframe(
                            result,
                            use_container_width=True,
                        )

                st.divider()

                reason_candidates = [
                    column
                    for column in df.columns
                    if "reason" in column.lower()
                ]

                if reason_candidates:

                    st.subheader("Top Waste Reasons")

                    reason_column = reason_candidates[0]

                    reason_result = calculate_top_waste_reasons(
                        df,
                        waste_reason_column=reason_column,
                        waste_column=waste_column,
                    )

                    st.dataframe(
                        reason_result,
                        use_container_width=True,
                    )

            else:
                st.info(
                    "At least two numeric columns are required "
                    "for waste analysis."
                )

    except Exception as e:
        st.error(f"Could not process the file: {e}")

else:
    st.info(
        "Upload a CSV, XLSX, XLS, or PDF file to begin analysis."
    )
