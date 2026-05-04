import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

st.title("📦 Supply Chain Data Dashboard")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

@st.cache_data
def load_data(file):
    df = pd.read_csv(file, encoding="latin1", nrows=10000)
    df.columns = df.columns.str.strip()
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)

    st.success("Dataset uploaded successfully!")

    st.sidebar.header("⚙️ Controls")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if numeric_cols:
        selected_numeric = st.sidebar.selectbox(
            "Select Numeric Column",
            numeric_cols
        )
    else:
        selected_numeric = None
        st.sidebar.warning("No numeric columns found.")

    st.sidebar.subheader("🔍 Filter Data")

    preferred_filters = [
        "Type",
        "Delivery Status",
        "Category Name",
        "Customer City",
        "Customer Country",
        "Customer Email",
        "Customer Fname"
    ]

    available_filters = [col for col in preferred_filters if col in df.columns]

    if not available_filters:
        available_filters = df.select_dtypes(include=["object"]).columns.tolist()[:7]

    df_filtered = df.copy()

    for col in available_filters:
        unique_values = (
            df_filtered[col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        unique_values = sorted(unique_values)[:300]

        selected_values = st.sidebar.multiselect(
            f"Filter {col}",
            options=unique_values,
            key=f"filter_{col}"
        )

        if selected_values:
            df_filtered = df_filtered[
                df_filtered[col].astype(str).isin(selected_values)
            ]

    st.subheader("📊 Dataset Preview")
    st.write(f"Rows displayed: {df_filtered.shape[0]}")
    st.dataframe(df_filtered.head(100))

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", df.shape[0])
    col2.metric("Filtered Rows", df_filtered.shape[0])
    col3.metric("Total Columns", df.shape[1])

    if selected_numeric:
        st.subheader(f"📈 Distribution of {selected_numeric}")

        fig, ax = plt.subplots()
        sns.histplot(df_filtered[selected_numeric].dropna(), kde=True, ax=ax)
        ax.set_xlabel(selected_numeric)
        ax.set_ylabel("Count")
        st.pyplot(fig)

    st.subheader("🧾 Columns Detected")
    st.write(df.columns.tolist())

else:
    st.info("Please upload a CSV file to begin.")
