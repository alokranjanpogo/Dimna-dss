import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Historical Comparison",
    layout="wide"
)

st.title("📊 Historical Comparison")

FILE_PATH = "data/rainfall_withdrawal.xlsx"

ALL_FY = [
    "FY23", "FY24", "FY25",
    "FY26", "FY27",
    "FY28", "FY29",
    "FY30", "FY31",
    "FY32", "FY33"
]

AVAILABLE_FY = [
    "FY23",
    "FY24",
    "FY25",
    "FY26",
    "FY27"
]

MONTHS = [
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan",
    "Feb",
    "Mar"
]

selected_fys = st.multiselect(
    "Select Financial Years",
    ALL_FY,
    default=["FY23", "FY24", "FY25"]
)

selected_month = st.selectbox(
    "Select Month",
    ["All"] + MONTHS
)

# ==========================================
# RAINFALL COMPARISON
# ==========================================

st.subheader("🌧 Rainfall Comparison")
st.caption("Unit : mm")

rain_df = pd.read_excel(
    FILE_PATH,
    sheet_name=0,
    header=None
)

rain_columns = {
    "FY27": 1,
    "FY26": 3,
    "FY25": 5,
    "FY24": 7,
    "FY23": 9
}

rain_chart = pd.DataFrame(
    index=MONTHS
)

for fy in selected_fys:

    if fy not in AVAILABLE_FY:

        st.warning(
            f"{fy} : NA - Rainfall Data Not Available"
        )

        continue

    values = pd.to_numeric(
        rain_df.iloc[4:, rain_columns[fy]],
        errors="coerce"
    ).fillna(0)

    monthly_values = []

    chunk_size = max(
        int(len(values) / 12),
        1
    )

    for i in range(12):

        start = i * chunk_size
        end = start + chunk_size

        monthly_values.append(
            round(
                values.iloc[start:end].sum(),
                2
            )
        )

    rain_chart[fy] = monthly_values

if selected_month != "All":

    st.bar_chart(
        rain_chart.loc[[selected_month]]
    )

else:

    st.line_chart(
        rain_chart
    )

st.divider()

# ==========================================
# WITHDRAWAL COMPARISON
# ==========================================

st.subheader("💦 Withdrawal Comparison")
st.caption("Unit : MLD")

withdraw_df = pd.read_excel(
    FILE_PATH,
    sheet_name=1,
    header=None
)

withdraw_columns = {
    "FY23": 1,
    "FY24": 2,
    "FY25": 3,
    "FY26": 4,
    "FY27": 5
}

withdraw_chart = pd.DataFrame(
    index=MONTHS
)

for fy in selected_fys:

    if fy not in AVAILABLE_FY:

        st.warning(
            f"{fy} : NA - Withdrawal Data Not Available"
        )

        continue

    values = pd.to_numeric(
        withdraw_df.iloc[2:, withdraw_columns[fy]],
        errors="coerce"
    ).fillna(0)

    monthly_values = []

    chunk_size = max(
        int(len(values) / 12),
        1
    )

    for i in range(12):

        start = i * chunk_size
        end = start + chunk_size

        monthly_values.append(
            round(
                values.iloc[start:end].mean(),
                2
            )
        )

    withdraw_chart[fy] = monthly_values

if selected_month != "All":

    st.bar_chart(
        withdraw_chart.loc[[selected_month]]
    )

else:

    st.line_chart(
        withdraw_chart
    )

st.divider()

# ==========================================
# SUMMARY
# ==========================================

st.subheader("📌 Summary")

c1, c2 = st.columns(2)

with c1:

    st.write(
        "### Total Rainfall (mm)"
    )

    if not rain_chart.empty:

        st.dataframe(
            rain_chart.sum().to_frame(
                "Rainfall (mm)"
            )
        )

with c2:

    st.write(
        "### Average Withdrawal (MLD)"
    )

    if not withdraw_chart.empty:

        st.dataframe(
            withdraw_chart.mean().to_frame(
                "Withdrawal (MLD)"
            )
        )
