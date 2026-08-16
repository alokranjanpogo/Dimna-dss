import streamlit as st
import pandas as pd

st.title("📊 Historical Comparison")

# ==================================
# RAINFALL COMPARISON
# ==================================

st.subheader("🌧 Monthly Rainfall Comparison")

rain_df = pd.read_excel(
    "rainfall_withdrawal.xlsx",
    sheet_name=0,
    header=None
)

dates = pd.to_datetime(
    rain_df.iloc[4:, 0],
    unit="D",
    origin="1899-12-30",
    errors="coerce"
)

months = dates.dt.strftime("%b")

rain_monthly = pd.DataFrame({
    "Month": months,
    "FY27": pd.to_numeric(rain_df.iloc[4:, 1], errors="coerce"),
    "FY26": pd.to_numeric(rain_df.iloc[4:, 3], errors="coerce"),
    "FY25": pd.to_numeric(rain_df.iloc[4:, 5], errors="coerce"),
    "FY24": pd.to_numeric(rain_df.iloc[4:, 7], errors="coerce"),
    "FY23": pd.to_numeric(rain_df.iloc[4:, 9], errors="coerce")
})

rain_chart = rain_monthly.groupby(
    "Month"
).sum()

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

rain_chart = rain_chart.reindex(
    month_order
)

st.line_chart(rain_chart)

st.divider()

# ==================================
# WITHDRAWAL COMPARISON
# ==================================

st.subheader("💦 Monthly Withdrawal Comparison")

with_df = pd.read_excel(
    "rainfall_withdrawal.xlsx",
    sheet_name=1,
    header=None
)

dates = pd.to_datetime(
    with_df.iloc[2:, 0],
    unit="D",
    origin="1899-12-30",
    errors="coerce"
)

months = dates.dt.strftime("%b")

withdrawal_monthly = pd.DataFrame({
    "Month": months,
    "FY23": pd.to_numeric(with_df.iloc[2:, 1], errors="coerce"),
    "FY24": pd.to_numeric(with_df.iloc[2:, 2], errors="coerce"),
    "FY25": pd.to_numeric(with_df.iloc[2:, 3], errors="coerce"),
    "FY26": pd.to_numeric(with_df.iloc[2:, 4], errors="coerce"),
    "FY27": pd.to_numeric(with_df.iloc[2:, 5], errors="coerce")
})

withdrawal_chart = withdrawal_monthly.groupby(
    "Month"
).mean()

withdrawal_chart = withdrawal_chart.reindex(
    month_order
)

st.line_chart(withdrawal_chart)
