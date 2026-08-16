import streamlit as st
import pandas as pd

st.title("🌧 Rainfall Analytics")

df = pd.read_excel(
    "rainfall/withdrawal.xlsx",
    sheet_name=0,
    header=None
)

fy = st.selectbox(
    "Select FY",
    ["FY27","FY26","FY25","FY24","FY23"]
)

fy_map = {
    "FY27": (1, 2),
    "FY26": (3, 4),
    "FY25": (5, 6),
    "FY24": (7, 8),
    "FY23": (9, 10)
}

rainfall_type = st.radio(
    "Rainfall Type",
    ["Daily", "YTD"]
)

col = fy_map[fy][0] if rainfall_type == "Daily" else fy_map[fy][1]

rainfall = pd.to_numeric(
    df.iloc[4:, col],
    errors="coerce"
).fillna(0)

chart_df = pd.DataFrame({
    "Day": range(1, len(rainfall)+1),
    "Rainfall": rainfall.values
})

st.line_chart(
    chart_df.set_index("Day")
)
