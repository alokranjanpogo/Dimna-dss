import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Historical Comparison",
    layout="wide"
)

st.title("📊 Historical Comparison")

file_path = "data/rainfall_withdrawal.xlsx"

# =====================================
# RAINFALL COMPARISON
# =====================================

st.subheader("🌧 Rainfall Comparison (FY23-FY27)")

rain_df = pd.read_excel(
    file_path,
    sheet_name=0,
    header=None
)

rain_compare = pd.DataFrame()

rain_compare["FY27"] = pd.to_numeric(
    rain_df.iloc[4:, 1],
    errors="coerce"
)

rain_compare["FY26"] = pd.to_numeric(
    rain_df.iloc[4:, 3],
    errors="coerce"
)

rain_compare["FY25"] = pd.to_numeric(
    rain_df.iloc[4:, 5],
    errors="coerce"
)

rain_compare["FY24"] = pd.to_numeric(
    rain_df.iloc[4:, 7],
    errors="coerce"
)

rain_compare["FY23"] = pd.to_numeric(
    rain_df.iloc[4:, 9],
    errors="coerce"
)

rain_compare = rain_compare.fillna(0)

st.line_chart(rain_compare)

st.divider()

# =====================================
# WITHDRAWAL COMPARISON
# =====================================

st.subheader("💦 Withdrawal Comparison (FY23-FY27)")

withdraw_df = pd.read_excel(
    file_path,
    sheet_name=1,
    header=None
)

withdraw_compare = pd.DataFrame()

withdraw_compare["FY23"] = pd.to_numeric(
    withdraw_df.iloc[2:, 1],
    errors="coerce"
)

withdraw_compare["FY24"] = pd.to_numeric(
    withdraw_df.iloc[2:, 2],
    errors="coerce"
)

withdraw_compare["FY25"] = pd.to_numeric(
    withdraw_df.iloc[2:, 3],
    errors="coerce"
)

withdraw_compare["FY26"] = pd.to_numeric(
    withdraw_df.iloc[2:, 4],
    errors="coerce"
)

withdraw_compare["FY27"] = pd.to_numeric(
    withdraw_df.iloc[2:, 5],
    errors="coerce"
)

withdraw_compare = withdraw_compare.fillna(0)

st.line_chart(withdraw_compare)

st.divider()

# =====================================
# SUMMARY
# =====================================

st.subheader("📌 Summary Statistics")

col1, col2 = st.columns(2)

with col1:

    st.write("### Rainfall Totals")

    st.dataframe(
        rain_compare.sum().to_frame(
            "Total Rainfall"
        )
    )

with col2:

    st.write("### Average Withdrawal")

    st.dataframe(
        withdraw_compare.mean().to_frame(
            "Average Withdrawal"
        )
    )
