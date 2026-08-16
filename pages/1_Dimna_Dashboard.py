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


st.set_page_config(
    page_title="Dimna DSS",
    layout="wide"
)

st.title("💧 Dimna Reservoir Decision Support System")

# ==================================================
# DAILY ENTRY
# ==================================================

st.subheader("📝 Daily Operations Entry")

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

c4, c5 = st.columns(2)

with c4:
    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0
    )

with c5:
    remarks = st.text_input(
        "Remarks"
    )

if st.button("✅ Save Record"):

    try:

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

    except Exception as e:

        st.error(
            f"Save Error: {e}"
        )

st.divider()

# ==================================================
# LIVE DATA
# ==================================================

try:

    latest = get_latest_record()

except:

    latest = {
        "Current_
