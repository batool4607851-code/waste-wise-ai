
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
    "Upload factory production or waste data",
    type=["csv", "xlsx", "xls", "pdf"],
)


if uploaded_file:

    try:
        # Every supported file is converted to a DataFrame
        df = load_data(uploaded_file)

        if not hasattr(df, "columns"):
            raise ValueError(
                "The file could not be converted into a data table."
            )

        validation = validate_data(df)

        st.success("File uploaded and data extracted successfully.")

        st.subheader("Data Preview")
        st.dataframe(
            df.head(10),
            use_container_width=True,
        )

        st.subheader("Dataset Information")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", validation["rows"])
        col2.metric("Columns", len(validation["columns"]))
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
                f"{kpis['total_production']:,.0f}",
            )

            kpi2.metric(
                "Total Waste",
                f"{kpis['total_waste']:,.0f}",
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

                reason_result = calculate_top_waste_reasons(
                    df,
                    waste_reason_column=reason_candidates[0],
                    waste_column=waste_column,
                )

                st.dataframe(
                    reason_result,
                    use_container_width=True,
                )

        else:

            st.warning(
                "The uploaded file does not contain at least "
                "two numeric columns required for waste analysis."
            )

    except Exception as e:

        st.error(f"Could not process the file: {e}")

else:

    st.info(
        "Upload a CSV, XLSX, XLS, or PDF file to begin analysis."
    )
