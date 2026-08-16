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

# =====================================================
# DAILY ENTRY
# =====================================================

st.subheader("📝 Daily Operations Entry")

col1, col2, col3 = st.columns(3)

with col1:
    entry_date = st.date_input("Date")

with col2:
    current_level_input = st.number_input(
        "Current Level (ft)",
        min_value=508.0,
        max_value=531.0,
        step=0.01
    )

with col3:
    withdrawal_input = st.number_input(
        "Withdrawal (MLD)",
        min_value=0.0,
        step=1.0
    )

col4, col5 = st.columns(2)

with col4:
    rainfall_input = st.number_input(
        "Rainfall (mm)",
        min_value=0.0
    )

with col5:
    remarks_input = st.text_input(
        "Remarks"
    )

if st.button("✅ Save Record"):

    try:

        add_daily_record(
            entry_date,
            current_level_input,
            withdrawal_input,
            rainfall_input,
            remarks_input
        )

        st.success(
            "Record saved successfully."
        )

    except Exception as e:

        st.error(
            f"Save Error: {e}"
        )

st.divider()

# =====================================================
# GET LATEST DATA
# =====================================================

try:

    latest = get_latest_record()

    if latest is None:

        latest = {
            "Current_Level": 527.35,
            "Withdrawal_MLD": 0
        }

except Exception:

    latest = {
        "Current_Level": 527.35,
        "Withdrawal_MLD": 0
    }

live_level = float(
    latest["Current_Level"]
)

rule_level = get_rule_level(
    date.today()
)

try:
    current_volume = get_current_volume(
        live_level
    )
except:
    current_volume = 0

try:
    available_storage = get_available_storage(
        live_level,
        date.today()
    )
except:
    available_storage = 0

try:
    buffer_ft = get_buffer_ft(
        live_level,
        date.today()
    )
except:
    buffer_ft = 0

try:
    allowed = withdrawal_allowed(
        live_level,
        date.today()
    )
except:
    allowed = False

alert = get_alert(
    live_level
)

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Live Reservoir Status")

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric(
        "Current Level",
        f"{live_level:.2f} ft"
    )

with k2:
    st.metric(
        "Rule Level",
        f"{rule_level:.2f} ft"
    )

with k3:
    st.metric(
        "Buffer",
        f"{buffer_ft:.2f} ft"
    )

with k4:
    st.metric(
        "Current Volume",
        current_volume
    )

with k5:
    st.metric(
        "Available Storage",
        available_storage
    )

# =====================================================
# DECISION BOX
# =====================================================

st.subheader("📋 Today's Decision")

if allowed:

    st.success(
        f"""
Current Level : {live_level:.2f} ft

Rule Level : {rule_level:.2f} ft

Buffer Available : {buffer_ft:.2f} ft

✅ WITHDRAWAL ALLOWED
"""
    )

else:

    st.error(
        f"""
Current Level : {live_level:.2f} ft

Rule Level : {rule_level:.2f} ft

❌ WITHDRAWAL NOT ALLOWED
"""
    )

st.divider()

# =====================================================
# ALERTS
# =====================================================

if live_level >= 529.5:

    st.error(
        f"""
🔴 HIGH LEVEL ALERT

Current Level : {live_level:.2f} ft

MANDATORY WITHDRAWAL : 150 MLD
"""
    )

elif live_level >= 529:

    st.warning(
        "🟡 Reservoir Approaching Alert Level"
    )

else:

    st.success(
        "🟢 Reservoir Operating Normally"
    )

st.divider
