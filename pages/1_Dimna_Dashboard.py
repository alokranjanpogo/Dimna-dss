import streamlit as st
import pandas as pd
from datetime import date

from utils.google_sheet import (
    add_daily_record,
    get_latest_record,
    get_all_records
)

from utils.calculations import (
    get_rule_level,
    get_current_volume,
    get_available_storage,
    get_buffer_ft,
    withdrawal_allowed
)

from utils.alerts import get_alert


st.title("💧 Dimna Reservoir Dashboard")

# ======================
# DATA ENTRY
# ======================

st.subheader("Daily Operations Entry")

c1, c2, c3 = st.columns(3)

with c1:

    entry_date = st.date_input(
        "Date"
    )

with c2:

    current_level = st.number_input(
        "Current Level (ft)",
        min_value=508.00,
        max_value=531.00,
        step=0.01
    )

with c3:

    withdrawal = st.number_input(
        "Withdrawal (MLD)",
        min_value=0.0,
        step=1.0
    )

rainfall = st.number_input(
    "Rainfall (mm)",
    min_value=0.0
)

remarks = st.text_area(
    "Remarks"
)

if st.button("Save Record"):

    add_daily_record(
        entry_date,
        current_level,
        withdrawal,
        rainfall,
        remarks
    )

    st.success(
        "Record Saved Successfully"
    )

st.divider()

# ======================
# LIVE DASHBOARD
# ======================

latest = get_latest_record()

if latest is not None:

    live_level = float(
        latest["Current_Level"]
    )

    rule_level = get_rule_level(
        date.today()
    )

    current_volume = get_current_volume(
        live_level
    )

    storage = get_available_storage(
        live_level,
        date.today()
    )

    buffer_ft = get_buffer_ft(
        live_level,
        date.today()
    )

    allowed = withdrawal_allowed(
        live_level,
        date.today()
    )

    alert = get_alert(
        live_level
    )

    st.subheader(
        "Live Reservoir Status"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Current Level",
            f"{live_level:.2f} ft"
        )

    with c2:
        st.metric(
            "Rule Level",
            f"{rule_level:.2f} ft"
        )

    with c3:
        st.metric(
            "Buffer",
            f"{buffer_ft:.2f} ft"
        )

    with c4:
        st.metric(
            "Current Volume",
            round(
                current_volume,
                2
            )
        )

    with c5:
        st.metric(
            "Available Storage",
            round(
                storage,
                2
            )
        )

    if allowed:

        st.success(
            "✅ Withdrawal Allowed"
        )

    else:

        st.error(
            "❌ Withdrawal Not Allowed"
        )

    # ALERTS

    if alert["status"] == "RED":

        st.error(
            """
            🔴 HIGH LEVEL ALERT

            MANDATORY WITHDRAWAL

            150 MLD
            """
        )

    elif alert["status"] == "YELLOW":

        st.warning(
            alert["message"]
        )

    else:

        st.success(
            alert["message"]
        )

    st.divider()

    st.subheader(
        "Reservoir Gauge"
    )

    gauge = (
        live_level - 518
    ) / (
        531 - 518
    )

    st.progress(
        min(
            max(gauge, 0),
            1
        )
    )

    st.write(
        f"""
        518 ft → Drawdown Limit

        524.5 ft → Storage Rule Level

        529.5 ft → Alert Level

        531 ft → Maximum Level
        """
    )

st.divider()

# ======================
# HISTORICAL DATA
# ======================

st.subheader(
    "Historical Records"
)

try:

    records = get_all_records()

    st.dataframe(
        records,
        use_container_width=True
    )

except:
    pass

