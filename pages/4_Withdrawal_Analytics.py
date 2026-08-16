import streamlit as st
import pandas as pd

st.title("💦 Withdrawal Analytics")

df = pd.read_excel(
    "data/rainfall_withdrawal.xlsx",
    sheet_name=1,
    header=None
)

fy = st.selectbox(
    "Select FY",
    ["FY23", "FY24", "FY25", "FY26", "FY27"]
)

fy_columns = {
    "FY23": 1,
    "FY24": 2,
    "FY25": 3,
    "FY26": 4,
    "FY27": 5
}

chart_df = pd.DataFrame()

chart_df["Date"] = pd.to_datetime(
    df.iloc[2:, 0],
    origin="1899-12-30",
    unit="D",
    errors="coerce"
)

chart_df["Withdrawal"] = pd.to_numeric(
    df.iloc[2:, fy_columns[fy]],
    errors="coerce"
)

chart_df = chart_df.dropna()

st.line_chart(
    chart_df.set_index("Date")
)
