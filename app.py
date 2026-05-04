import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Supply Chain Analysis", layout="wide")

# -------------------------------
# Title
# -------------------------------
st.title("📦 Supply Chain Analysis Dashboard")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding="latin1")

    st.dataframe(df.head())

    # -------------------------------
    # Basic Info
    # -------------------------------
    st.subheader("📈 Dataset Overview")
    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # -------------------------------
    # Column Selection
    # -------------------------------
    st.sidebar.header("⚙️ Controls")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        selected_col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)

        # -------------------------------
        # Distribution Plot
        # -------------------------------
        st.subheader(f"Distribution of {selected_col}")

        fig, ax = plt.subplots()
        sns.histplot(df[selected_col], kde=True, ax=ax)
        st.pyplot(fig)

        # -------------------------------
        # Box Plot
        # -------------------------------
        st.subheader(f"Box Plot of {selected_col}")

        fig2, ax2 = plt.subplots()
        sns.boxplot(x=df[selected_col], ax=ax2)
        st.pyplot(fig2)

    # -------------------------------
    # Correlation Heatmap
    # -------------------------------
    if len(numeric_cols) > 1:
        st.subheader("🔗 Correlation Heatmap")

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="viridis", ax=ax3)
        st.pyplot(fig3)

    # -------------------------------
    # Filtering
    # -------------------------------
    st.sidebar.subheader("🔍 Filter Data")

    for col in df.columns:
        if df[col].dtype == "object":
            selected_values = st.sidebar.multiselect(
                f"Filter {col}", df[col].unique()
            )
            if selected_values:
                df = df[df[col].isin(selected_values)]

    st.subheader("📌 Filtered Data")
    st.dataframe(df)

else:
    st.info("👆 Upload a CSV file to start analysis.")