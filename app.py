import streamlit as st

from src.data_loader import load_data
from src.analytics import calculate_basic_metrics


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
    type=["csv", "xlsx"],
)

if uploaded_file:
    try:
        df = load_data(uploaded_file)

        st.success("File uploaded successfully.")

        st.subheader("Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

        metrics = calculate_basic_metrics(df)

        st.subheader("Basic Dataset Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", metrics["rows"])

        with col2:
            st.metric("Columns", metrics["columns"])

    except Exception as e:
        st.error(f"Could not process the file: {e}")
else:
    st.info("Upload a CSV or XLSX file to begin analysis.")
