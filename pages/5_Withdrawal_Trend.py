import streamlit as st
import pandas as pd
import plotly.express as px

st.title(
    "🚰 Withdrawal Trend Analysis"
)

file_path = "data/rainfall_withdrawal.xlsx"

try:

    df = pd.read_excel(
        file_path,
        sheet_name=1
    )

    st.success(
        "Withdrawal data loaded"
    )

    st.subheader(
        "Withdrawal Data Preview"
    )

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    numeric_df = df.select_dtypes(
        include="number"
    )

    if not numeric_df.empty:

        fig = px.line(
            numeric_df,
            title="Historical Withdrawal Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

except Exception as e:

    st.error(
        f"Error loading data: {e}"
    )
