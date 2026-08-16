import streamlit as st
import pandas as pd

st.title("📊 Historical Comparison")

# Rainfall Comparison

st.subheader(
    "Rainfall FY Comparison"
)

rainfall_df = pd.read_excel(
    "data/rainfall_withdrawal.xlsx",
    sheet_name=0,
    header=None
)

comparison = pd.DataFrame()

comparison["FY27"] = pd.to_numeric(
    rainfall_df.iloc[4:, 2],
    errors="coerce"
)

comparison["FY26"] = pd.to_numeric(
    rainfall_df.iloc[4:, 4],
    errors="coerce"
)

comparison["FY25"] = pd.to_numeric(
    rainfall_df.iloc[4:, 6],
    errors="coerce"
)

comparison["FY24"] = pd.to_numeric(
    rainfall_df.iloc[4:, 8],
    errors="coerce"
)

comparison["FY23"] = pd.to_numeric(
    rainfall_df.iloc[4:, 10],
    errors="coerce"
)

st.line_chart(
    comparison.fillna(0)
)

st.divider()

# Withdrawal Comparison

st.subheader(
    "Withdrawal FY Comparison"
)

withdrawal_df = pd.read_excel(
    "data/rainfall_withdrawal.xlsx",
    sheet_name=1,
    header=None
)

comparison2 = pd.DataFrame()

comparison2["FY23"] = pd.to_numeric(
    withdrawal_df.iloc[2:, 1],
    errors="coerce"
)

comparison2["FY24"] = pd.to_numeric(
    withdrawal_df.iloc[2:, 2],
    errors="coerce"
)

comparison2["FY25"] = pd.to_numeric(
    withdrawal_df.iloc[2:, 3],
    errors="coerce"
)

comparison2["FY26"] = pd.to_numeric(
    withdrawal_df.iloc[2:, 4],
    errors="coerce"
)

comparison2["FY27"] = pd.to_numeric(
    withdrawal_df.iloc[2:, 5],
    errors="coerce"
)

st.line_chart(
    comparison2.fillna(0)
)
