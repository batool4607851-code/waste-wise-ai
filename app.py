import streamlit as st

from src.data_loader import load_data, validate_data
from src.analytics import (
    calculate_waste_kpis,
    calculate_group_waste_rates,
    calculate_top_waste_reasons,
    loss_trend,
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
        df = load_data(uploaded_file)

        if not hasattr(df, "columns"):
            raise ValueError("The file could not be converted into a data table.")

        validation = validate_data(df)

        st.success("File uploaded and data extracted successfully.")

        st.subheader("Data Preview")
        st.dataframe(
            df.head(10).reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
        )

        # ---------------------------------------------------------
        # COLUMN MAPPING
        # ---------------------------------------------------------

        st.divider()
        st.subheader("Column Mapping")

        st.write(
            "WasteWise maps your factory's column names to standard fields "
            "used by the analytics engine."
        )

        mapping = {}

        canonical_fields = [
            "date",
            "product",
            "production_line",
            "shift",
            "production_quantity",
            "event_reason",
            "loss_quantity",
        ]

        for field in canonical_fields:

            current_match = None

            for column in df.columns:
                normalized = column.lower().replace(" ", "_")

                if field == normalized:
                    current_match = column
                    break

            options = ["Not available"] + list(df.columns)

            default_index = (
                options.index(current_match)
                if current_match in options
                else 0
            )

            mapping[field] = st.selectbox(
                field.replace("_", " ").title(),
                options,
                index=default_index,
                key=f"mapping_{field}",
            )

        if st.button("Confirm Mapping & Continue", type="primary"):

            rename_map = {
                selected: canonical
                for canonical, selected in mapping.items()
                if selected != "Not available"
            }

            normalized_df = df.rename(columns=rename_map).copy()

            required_fields = [
                "production_quantity",
                "loss_quantity",
            ]

            missing_required = [
                field
                for field in required_fields
                if field not in normalized_df.columns
            ]

            if missing_required:
                st.error(
                    "Missing required fields: "
                    + ", ".join(missing_required)
                )
                st.stop()

            for numeric_field in [
                "production_quantity",
                "loss_quantity",
            ]:
                normalized_df[numeric_field] = (
                    normalized_df[numeric_field]
                    .astype(str)
                    .str.replace(",", "", regex=False)
                )

                normalized_df[numeric_field] = (
                    __import__("pandas")
                    .to_numeric(
                        normalized_df[numeric_field],
                        errors="coerce",
                    )
                    .fillna(0)
                )

            st.session_state["normalized_df"] = normalized_df
            st.session_state["mapping_confirmed"] = True

            st.success("Column mapping confirmed and data normalized.")

        # ---------------------------------------------------------
        # ANALYSIS ONLY AFTER MAPPING
        # ---------------------------------------------------------

        if st.session_state.get("mapping_confirmed", False):

            normalized_df = st.session_state["normalized_df"]

            st.subheader("Normalized WasteWise Data")

            st.dataframe(
                normalized_df.head(10).reset_index(drop=True),
                use_container_width=True,
                hide_index=True,
            )

            st.subheader("Available Fields")
            st.write(", ".join(normalized_df.columns.tolist()))

            st.divider()

            # -----------------------------------------------------
            # DATASET INFORMATION
            # -----------------------------------------------------

            st.subheader("Dataset Information")

            col1, col2, col3, col4 = st.columns(4)

            normalized_validation = validate_data(normalized_df)

            col1.metric("Rows", normalized_validation["rows"])
            col2.metric("Columns", normalized_validation["columns"])
            col3.metric(
                "Missing Values",
                normalized_validation["missing_values"],
            )
            col4.metric(
                "Duplicate Rows",
                normalized_validation["duplicate_rows"],
            )

            st.divider()

            # -----------------------------------------------------
            # KPI DASHBOARD
            # -----------------------------------------------------

            st.subheader("Waste KPI Dashboard")

            kpis = calculate_waste_kpis(
                normalized_df,
                "production_quantity",
                "loss_quantity",
            )

            kpi1, kpi2, kpi3 = st.columns(3)

            kpi1.metric(
                "Total Production",
                f"{kpis['total_production']:,.0f}",
            )

            kpi2.metric(
                "Total Loss",
                f"{kpis['total_waste']:,.0f}",
            )

            kpi3.metric(
                "Loss Rate",
                f"{kpis['waste_rate']:.2f}%",
            )

            st.divider()

            # -----------------------------------------------------
            # LOSS RATE ANALYSIS
            # -----------------------------------------------------

            st.subheader("Loss Rate Analysis")

            group_options = [
                column
                for column in normalized_df.columns
                if column not in [
                    "production_quantity",
                    "loss_quantity",
                ]
            ]

            if group_options:

                group_column = st.selectbox(
                    "Group analysis by",
                    group_options,
                )

                if st.button("Analyze Waste Rates"):

                    result = calculate_group_waste_rates(
                        normalized_df,
                        group_column=group_column,
                        production_column="production_quantity",
                        waste_column="loss_quantity",
                    )

                    st.dataframe(
                        result.reset_index(drop=True),
                        use_container_width=True,
                        hide_index=True,
                    )

            st.divider()

            # -----------------------------------------------------
            # TOP LOSS REASONS
            # -----------------------------------------------------

            if "event_reason" in normalized_df.columns:

                st.subheader("Top Loss Reasons")

                reason_result = calculate_top_waste_reasons(
                    normalized_df,
                    "event_reason",
                    "loss_quantity",
                )

                st.dataframe(
                    reason_result.reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

            st.divider()

            # -----------------------------------------------------
            # LOSS TREND
            # -----------------------------------------------------

            st.subheader("Loss Trend")

            if "date" in normalized_df.columns:

                trend_result = loss_trend(
                    normalized_df,
                    date_column="date",
                    loss_column="loss_quantity",
                )

                if not trend_result.empty:

                    st.line_chart(
                        trend_result.set_index("date")["loss_quantity"]
                    )

                else:

                    st.info(
                        "A usable date field is required to display the loss trend."
                    )

            else:

                st.info(
                    "A date field is required to display the loss trend."
                )

    except Exception as e:

        st.error(f"Could not process the file: {e}")

else:

    st.info(
        "Upload a CSV, XLSX, XLS, or PDF file to begin analysis."
    )
