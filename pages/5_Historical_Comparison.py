import streamlit as st
import pandas as pd

st.title("📊 Historical Comparison")

# ==============================
# RAINFALL COMPARISON
# ==============================

st.subheader("🌧 Monthly Rainfall Comparison")

rain_df = pd.read_excel(
    "rainfall_withdrawal.xlsx",
    sheet_name=0,
    header=None
)

date_col = pd.to_datetime(
    rain_df.iloc[4:, 0],
    unit="D",
    origin="1899-12-30",
    errors="coerce"
)

months = date_col.dt.month_name().str[:3]

monthly_rain = pd.DataFrame()

monthly_rain["Month"] = months

monthly_rain["FY27"] = pd.to_numeric(
    rain_df.iloc[4:, 1],
    errors="coerce"
)

monthly_rain["FY26"] = pd.to_numeric(
    rain_df.iloc[4:, 3],
    errors="coerce"
)

monthly_rain["FY25"] = pd.to_numeric(
    rain_df.iloc[4:, 5],
    errors="coerce"
)

monthly_rain["FY24"] = pd.to_numeric(
    rain_df.iloc[4:, 7],
    errors="coerce"
)

monthly_rain["FY23"] = pd.to_numeric(
    rain_df.iloc[4:, 9],
    errors="coerce"
)

rain_chart = monthly_rain.groupby(
    "Month"
).sum()

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

rain_chart = rain_chart.reindex(
    month_order
)

st.line_chart(
    rain_chart
)

st.divider()

# ==============================
# WITHDRAWAL COMPARISON
# ==============================

st.subheader("💦 Monthly Withdrawal Comparison")

with_df = pd.read_excel(
    "rainfall_withdrawal.xlsx",
    sheet_name=1,
    header=None
)

date_col = pd.to_datetime(
    with_df.iloc[2:, 0],
    unit="D",
    origin="1899-12-30",
    errors="coerce"
)

months = date_col.dt.month_name().str[:3]

monthly_with = pd.DataFrame()

monthly_with["Month"] = months

monthly_with["FY23"] = pd.to_numeric(
    with_df.iloc[2:, 1],
    errors="coerce"
)

monthly_with["FY24"] = pd.to_numeric(
    with_df.iloc[2:, 2],
    errors
