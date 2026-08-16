import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Historical Comparison",
    layout="wide"
)

st.title("📊 Historical Comparison")

FILE_PATH = "data/rainfall_withdrawal.xlsx"

AVAILABLE_FY = [
    "FY23",
    "FY24",
    "FY25",
    "FY26",
    "FY27"
]

ALL_FY = [
    "FY23",
    "FY24",
    "FY25",
    "FY26",
    "FY27",
    "FY28",
    "FY29",
    "FY30",
    "FY31",
    "FY32",
    "FY33"
]

selected_fys = st.multiselect(
    "Select Financial Years",
    ALL_FY,
    default=["FY23", "FY24", "FY25"]
)

# ========================================
# RAINFALL COMPARISON
# ========================================

st.subheader("🌧 Rainfall Comparison")
st.caption("Unit: mm")

rain_df = pd.read_excel(
    FILE_PATH,
    sheet_name=0,
    header=None
)

rain_cols = {
    "FY27": 1,
    "FY26": 3,
    "FY25": 5,
    "FY24": 7,
    "FY23": 9
}

rain_chart = pd.DataFrame()

for fy in selected_fys:

    if fy in rain_cols:

        rain_chart[fy] = pd.to_numeric(
            rain_df.iloc[4:, rain_cols[fy]],
            errors="coerce"
        ).fillna(0)

    else:

        st.warning(
            f"{fy} : NA - Rainfall data not available."
        )

if not rain_chart.empty:

    st.line_chart(rain_chart)

else:

    st.info(
        "No rainfall data available."
    )

st.divider()

# ========================================
# WITHDRAWAL COMPARISON
# ========================================

st.subheader("💦 Withdrawal Comparison")
st.caption("Unit: MLD")

withdraw_df = pd.read_excel(
    FILE_PATH,
    sheet_name=1,
    header=None
)

withdraw_cols = {
    "FY23": 1,
    "FY24": 2,
    "FY25": 3,
    "FY26": 4,
    "FY27": 5
}

withdraw_chart = pd.DataFrame()

for fy in selected_fys:

    if fy in withdraw_cols:

        withdraw_chart[fy] = pd.to_numeric(
            withdraw_df.iloc[2:, withdraw_cols[fy]],
            errors="coerce"
        ).fillna(0)

    else:

        st.warning(
            f"{fy} : NA - Withdrawal data not available."
        )

if not withdraw_chart.empty:

    st.line_chart(withdraw_chart)

else:

    st.info(
        "No withdrawal data available."
    )

st.divider()

# ========================================
# SUMMARY
# ========================================

st.subheader("📌 Summary")

col1, col2 = st.columns(2)

with col1:

    if not rain_chart.empty:

        st.write("### Total Rainfall (mm)")

        st.dataframe(
            rain_chart.sum().to_frame(
                "Total Rainfall (mm)"
            )
        )

with col2:

    if not withdraw_chart.empty:

        st.write("### Average Withdrawal (MLD)")

        st.dataframe(
            withdraw_chart.mean().to_frame(
                "Average Withdrawal (MLD)"
            )
        )
