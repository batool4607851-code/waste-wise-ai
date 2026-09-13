import streamlit as st
import pandas as pd
from src.rag import build_chunks, build_vector_index, retrieve_chunks
from src.groq_client import generate_answer
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
st.markdown(
    """
    <style>
    /* SOP evidence typography */
    .stMarkdown p {
        font-size: 0.95rem;
    }

    div[data-testid="stExpander"] summary p {
        font-size: 0.95rem;
        font-weight: 600;
    }

    div[data-testid="stExpander"] .stMarkdown h3 {
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("♻️ WasteWise AI")
st.subheader("Turn factory data into actionable waste intelligence.")


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("WasteWise AI")
st.sidebar.caption("Factory Waste Intelligence")

page = st.sidebar.radio(
    "Navigate",
    [
        "Data & Mapping",
        "KPI Dashboard",
        "Loss Analysis",
        "Investigation",
               "Anomaly Detection",
        "SOP / RAG",
    ],
)

st.divider()


# =========================================================
# DATA & MAPPING
# =========================================================


def format_sop_evidence(text):
    """Format raw SOP extraction into readable evidence."""
    import re

    text = str(text).replace("\r", " ").replace("\n", " ")

    # Remove PDF-to-Markdown link artifacts such as [svg](...)
    text = re.sub(r"\[svg\]\([^)]*\)", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    # Separate numbered SOP sections.
    text = re.sub(r"\s+(?=\d+\.\s+[A-Z])", "\n\n", text)

    # Format numbered section headings.
    text = re.sub(
        r"(?m)^(\d+\.\s+[A-Z][^\n]+)",
        r"### \1",
        text,
    )

    return re.sub(r"\n{3,}", "\n\n", text).strip()


if page == "Data & Mapping":

    uploaded_file = st.file_uploader(
        "Upload factory production or waste data",
        type=["csv", "xlsx", "xls", "pdf"],
    )

    if uploaded_file:

        try:

            df = load_data(uploaded_file)

            if not hasattr(df, "columns"):
                raise ValueError(
                    "The file could not be converted into a data table."
                )

            validate_data(df)

            st.success(
                "File uploaded and data extracted successfully."
            )

            st.subheader("Data Preview")

            st.dataframe(
                df.head(10).reset_index(drop=True),
                use_container_width=True,
                hide_index=True,
            )

            st.divider()

            st.subheader("Column Mapping")

            st.write(
                "WasteWise maps your factory's column names to "
                "standard fields used by the analytics engine."
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

                    normalized = (
                        column.lower()
                        .replace(" ", "_")
                    )

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

            if st.button(
                "Confirm Mapping & Continue",
                type="primary",
            ):

                rename_map = {
                    selected: canonical
                    for canonical, selected in mapping.items()
                    if selected != "Not available"
                }

                normalized_df = df.rename(
                    columns=rename_map
                ).copy()

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

                else:

                    for numeric_field in [
                        "production_quantity",
                        "loss_quantity",
                    ]:

                        normalized_df[numeric_field] = (
                            normalized_df[numeric_field]
                            .astype(str)
                            .str.replace(",", "", regex=False)
                        )

                        normalized_df[numeric_field] = pd.to_numeric(
                            normalized_df[numeric_field],
                            errors="coerce",
                        ).fillna(0)

                    st.session_state["normalized_df"] = normalized_df
                    st.session_state["mapping_confirmed"] = True

                    st.success(
                        "Column mapping confirmed and data normalized."
                    )

            if st.session_state.get(
                "mapping_confirmed",
                False,
            ):

                normalized_df = st.session_state["normalized_df"]

                st.divider()

                st.subheader("Normalized WasteWise Data")

                st.dataframe(
                    normalized_df.head(10).reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

                st.subheader("Available Fields")

                st.write(
                    ", ".join(normalized_df.columns.tolist())
                )

                st.divider()

                st.subheader("Dataset Information")

                col1, col2, col3, col4 = st.columns(4)

                validation = validate_data(normalized_df)

                col1.metric("Rows", validation["rows"])
                col2.metric("Columns", validation["columns"])
                col3.metric(
                    "Missing Values",
                    validation["missing_values"],
                )
                col4.metric(
                    "Duplicate Rows",
                    validation["duplicate_rows"],
                )

        except Exception as e:

            st.error(
                f"Could not process the file: {e}"
            )

    else:

        st.info(
            "Upload a CSV, XLSX, XLS, or PDF file to begin analysis."
        )


# =========================================================
# OTHER PAGES
# =========================================================

elif page in [
    "KPI Dashboard",
    "Loss Analysis",
    "Investigation",
    "Anomaly Detection",
]:

    normalized_df = st.session_state.get("normalized_df")

    if normalized_df is None:

        st.info(
            "Please go to Data & Mapping, upload your dataset, "
            "and confirm the mapping first."
        )

    else:

        # =====================================================
        # KPI DASHBOARD
        # =====================================================

        if page == "KPI Dashboard":

            st.header("📊 Waste KPI Dashboard")

            kpis = calculate_waste_kpis(normalized_df)

            st.caption(
                "A quick view of overall production performance and material loss."
            )

            kpi1, kpi2, kpi3 = st.columns(3)

            with kpi1:
                st.metric(
                    "Total Production",
                    f"{kpis['total_production']:,.0f}"
                )

            with kpi2:
                st.metric(
                    "Total Loss",
                    f"{kpis['total_loss']:,.0f}"
                )

            with kpi3:
                st.metric(
                    "Loss Rate",
                    f"{kpis['waste_rate']:.2f}%"
                )

            st.divider()

            st.subheader("🎯 What to investigate next")
            st.write(
                "Use Loss Analysis to identify the products, lines, shifts, "
                "processes, and loss reasons contributing most to the total loss."
            )


        # =====================================================
        # LOSS ANALYSIS
        # =====================================================

        elif page == "Loss Analysis":

            st.header("📈 Loss Analysis")

            if "product" in normalized_df.columns:

                st.subheader("Loss by Product")

                product_result = (
                    normalized_df
                    .groupby("product", dropna=False)["loss_quantity"]
                    .sum()
                    .reset_index()
                    .sort_values(
                        "loss_quantity",
                        ascending=False,
                    )
                )

                st.bar_chart(
                    product_result.set_index("product")[
                        "loss_quantity"
                    ]
                )

                st.dataframe(
                    product_result.reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

            st.divider()

            if "production_line" in normalized_df.columns:

                st.subheader("Loss by Production Line")

                line_result = (
                    normalized_df
                    .groupby(
                        "production_line",
                        dropna=False,
                    )["loss_quantity"]
                    .sum()
                    .reset_index()
                    .sort_values(
                        "loss_quantity",
                        ascending=False,
                    )
                )

                st.bar_chart(
                    line_result.set_index("production_line")[
                        "loss_quantity"
                    ]
                )

                st.dataframe(
                    line_result.reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

            st.divider()

            if "shift" in normalized_df.columns:

                st.subheader("Loss by Shift")

                shift_result = (
                    normalized_df
                    .groupby("shift", dropna=False)["loss_quantity"]
                    .sum()
                    .reset_index()
                    .sort_values(
                        "loss_quantity",
                        ascending=False,
                    )
                )

                st.bar_chart(
                    shift_result.set_index("shift")[
                        "loss_quantity"
                    ]
                )

                st.dataframe(
                    shift_result.reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

            st.divider()

            if "process" in normalized_df.columns:

                st.subheader("Loss by Process")

                process_result = (
                    normalized_df
                    .groupby("process", dropna=False)["loss_quantity"]
                    .sum()
                    .reset_index()
                    .sort_values(
                        "loss_quantity",
                        ascending=False,
                    )
                )

                st.bar_chart(
                    process_result.set_index("process")[
                        "loss_quantity"
                    ]
                )

                st.dataframe(
                    process_result.reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

            st.divider()

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
                    key="loss_analysis_group",
                )

                if st.button(
                    "Analyze Waste Rates",
                    key="loss_analysis_button",
                ):

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

            st.subheader("Loss Trend")

            if "date" in normalized_df.columns:

                trend_result = loss_trend(
                    normalized_df,
                    date_column="date",
                    loss_column="loss_quantity",
                )

                if not trend_result.empty:

                    st.line_chart(
                        trend_result.set_index("date")[
                            "loss_quantity"
                        ]
                    )

                else:

                    st.info(
                        "A usable date field is required to display the loss trend."
                    )

            else:

                st.info(
                    "A date field is required to display the loss trend."
                )


        # =====================================================
        # INVESTIGATION
        # =====================================================

        elif page == "Investigation":

            st.header("🔎 Investigation Priorities")

            priority_columns = [
                column
                for column in [
                    "product",
                    "production_line",
                    "shift",
                    "process",
                    "event_reason",
                ]
                if column in normalized_df.columns
            ]

            if priority_columns:

                priority_result = (
                    normalized_df
                    .groupby(
                        priority_columns,
                        dropna=False,
                    )["loss_quantity"]
                    .sum()
                    .reset_index()
                    .sort_values(
                        "loss_quantity",
                        ascending=False,
                    )
                    .head(10)
                )

                priority_result.insert(
                    0,
                    "Priority Rank",
                    range(
                        1,
                        len(priority_result) + 1,
                    ),
                )

                st.write(
                    "Highest-loss combinations that should be investigated first."
                )

                st.dataframe(
                    priority_result.reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

            else:

                st.info(
                    "Additional fields are required to generate investigation priorities."
                )


        # =====================================================
        # ANOMALY DETECTION
        # =====================================================

        elif page == "Anomaly Detection":

            st.header("🚨 High-Loss Anomaly Detection")

            loss_values = normalized_df["loss_quantity"]

            average_loss = loss_values.mean()
            std_loss = loss_values.std()

            anomaly_threshold = (
                average_loss + (2 * std_loss)
            )

            anomalies = normalized_df[
                normalized_df["loss_quantity"]
                > anomaly_threshold
            ].copy()

            st.metric(
                "Anomaly Threshold",
                f"{anomaly_threshold:,.2f}",
            )

            if not anomalies.empty:

                st.warning(
                    f"{len(anomalies)} unusually high-loss record(s) detected."
                )

                st.dataframe(
                    anomalies.reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

            else:

                st.success(
                    "No unusually high-loss records detected."
                )


# =========================================================
# SOP / RAG + GROQ
# =========================================================

elif page == "SOP / RAG":

    st.header("📘 SOP / RAG Assistant")

    st.write(
        "Upload an SOP PDF, ask a question, and WasteWise AI will "
        "retrieve relevant SOP evidence and generate a grounded answer."
    )

    sop_file = st.file_uploader(
        "Upload SOP PDF",
        type=["pdf"],
        key="sop_rag_upload",
    )

    if sop_file:

        sop_path = "uploaded_sop.pdf"

        with open(sop_path, "wb") as f:
            f.write(sop_file.getbuffer())

        try:

            chunks = build_chunks(sop_path)

            model, index, stored_chunks = build_vector_index(chunks)

            st.success(
                f"SOP processed successfully: {len(chunks)} text chunks created."
            )

            question = st.text_input(
                "Ask a question about the SOP",
                placeholder=(
                    "e.g. What should the supervisor investigate "
                    "when waste is unusually high?"
                ),
                key="sop_question",
            )

            if question.strip():

                results = retrieve_chunks(
                    question,
                    model,
                    index,
                    stored_chunks,
                    top_k=5,
                )

                context = "\n\n".join(
                    [
                        (
                            f"[Source: {result['source']}, "
                            f"Page: {result['page']}]\n"
                            f"{result['text']}"
                        )
                        for result in results
                    ]
                )

                try:

                    answer = generate_answer(
                        question,
                        context,
                    )

                    st.subheader("🤖 WasteWise AI Answer")

                    st.write(answer)

                except Exception as e:

                    st.error(
                        f"Could not generate AI answer: {e}"
                    )

                st.subheader("🔎 SOP Evidence")
                st.caption(
                    f"{len(results)} relevant SOP section(s) found. "
                    "Expand an item to review the supporting evidence."
                )

                for i, result in enumerate(
                    results,
                    start=1,
                ):

                    relevance_pct = min(
                        max(float(result["score"]), 0),
                        1,
                    ) * 100

                    with st.expander(
                        f"📄 Evidence {i}  ·  Page {result['page']}  ·  "
                        f"Relevance {relevance_pct:.0f}%",
                        expanded=(i == 1),
                    ):

                        st.markdown(
                            f"**Source:** `{result['source']}`"
                        )

                        st.progress(
                            int(relevance_pct),
                            text=f"Evidence relevance: {relevance_pct:.0f}%"
                        )

                        st.markdown("**Supporting SOP content**")

                        evidence_text = format_sop_evidence(result["text"])

                        st.markdown(
                            f"> {evidence_text.replace(chr(10), chr(10) + '> ')}"
                        )


        except Exception as e:

            st.error(
                f"Could not process the SOP: {e}"
            )

    else:

        st.info(
            "Upload an SOP PDF to start asking questions."
        )
