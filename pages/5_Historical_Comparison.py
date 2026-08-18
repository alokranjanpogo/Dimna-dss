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

# =====================================
# FILTERS
# =====================================

col1, col2 = st.columns(2)

with col1:

    selected_fys = st.multiselect(
        "Select Financial Years",
        ALL_FY,
        default=["FY23", "FY24", "FY25"]
    )

with col2:

    selected_months = st.multiselect(
        "Select Months",
        MONTHS,
        default=MONTHS
    )

# =====================================
# RAINFALL
# =====================================

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

filtered_rain = rain_chart.loc[
    selected_months
]

st.line_chart(
    filtered_rain
)

# =====================================
# RAINFALL SUMMARY
# =====================================

st.write("### Rainfall Summary")

if not filtered_rain.empty:

    st.dataframe(
        filtered_rain.sum().to_frame(
            "Total Rainfall (mm)"
        )
    )

st.divider()

# =====================================
# WITHDRAWAL OUTPUT
# =====================================

if len(selected_months) == 12:

    st.line_chart(
        withdraw_chart
    )

    st.write("### Withdrawal Summary")

    st.dataframe(
        withdraw_chart.mean().to_frame(
            "Average Withdrawal (MLD)"
        )
    )

else:

    st.subheader(
        "📅 Date-wise Withdrawal Data"
    )

    st.info(
        "Showing date-wise withdrawal records for selected month(s)."
    )

    dates = pd.to_datetime(
        pd.to_numeric(
            withdraw_df.iloc[2:, 0],
            errors="coerce"
        ),
        unit="D",
        origin="1899-12-30",
        errors="coerce"
    )

    raw_withdraw = pd.DataFrame()

    raw_withdraw["Date"] = dates

    selected_fy = selected_fys[0]

    raw_withdraw["Withdrawal_MLD"] = pd.to_numeric(
        withdraw_df.iloc[
            2:,
            withdraw_columns[selected_fy]
        ],
        errors="coerce"
    )

    raw_withdraw = raw_withdraw.dropna()

    raw_withdraw["Month"] = (
        raw_withdraw["Date"]
        .dt.strftime("%b")
    )

    filtered_daily = raw_withdraw[
        raw_withdraw["Month"].isin(
            selected_months
        )
    ]

    st.dataframe(
        filtered_daily,
        use_container_width=True
    )

    st.line_chart(
        filtered_daily.set_index(
            "Date"
        )[
            ["Withdrawal_MLD"]
        ]
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Average Withdrawal",
            f"{filtered_daily['Withdrawal_MLD'].mean():.0f} MLD"
        )

    with c2:

        st.metric(
            "Maximum Withdrawal",
            f"{filtered_daily['Withdrawal_MLD'].max():.0f} MLD"
        )

    with c3:

        st.metric(
            "Minimum Withdrawal",
            f"{filtered_daily['Withdrawal_MLD'].min():.0f} MLD"
        )
