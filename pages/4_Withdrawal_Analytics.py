import streamlit as st
import pandas as pd

st.title("💦 Withdrawal Analytics")

df = pd.read_excel(
    "rainfall_withdrawal.xlsx",
    sheet_name=1,
    header=None
)

fy = st.selectbox(
    "Select FY",
    ["FY23","FY24","FY25","FY26","FY27"]
)

fy_cols = {
    "FY23": 1,
    "FY24": 2,
    "FY25": 3,
    "FY26": 4,
    "FY27": 5
}

withdrawal = pd.to_numeric(
    df.iloc[2:, fy_cols[fy]],
    errors="coerce"
).fillna(0)

chart_df = pd.DataFrame({
    "Day": range(1, len(withdrawal)+1),
    "Withdrawal": withdrawal.values
})

st.line_chart(
    chart_df.set_index("Day")
)
