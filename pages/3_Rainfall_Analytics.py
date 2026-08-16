import streamlit as st
import pandas as pd

st.title("🌧 Rainfall Analytics")

df = pd.read_excel(
    "data/rainfall_withdrawal.xlsx",
    sheet_name=0,
    header=None
)

fy = st.selectbox(
    "Select FY",
    ["FY27", "FY26", "FY25", "FY24", "FY23"]
)

fy_map = {
    "FY27": [1, 2],
    "FY26": [3, 4],
    "FY25": [5, 6],
    "FY24": [7, 8],
    "FY23": [9, 10]
}

rainfall_type = st.radio(
    "Rainfall Type",
    ["Daily Rainfall", "YTD Rainfall"]
)

date_col = 0

value_col = (
    fy_map[fy][0]
    if rainfall_type == "Daily Rainfall"
    else fy_map[fy][1]
)

chart_df = pd.DataFrame()

chart_df["Date"] = pd.to_datetime(
    df.iloc[4:, date_col],
    origin="1899-12-30",
    unit="D",
    errors="coerce"
)

chart_df["Rainfall"] = pd.to_numeric(
    df.iloc[4:, value_col],
    errors="coerce"
)

chart_df = chart_df.dropna()

st.line_chart(
    chart_df.set_index("Date")
)
