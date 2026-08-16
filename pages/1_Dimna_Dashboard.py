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
    page_icon="💧",
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
    current_level_input = st.number_input(
        "Current Level (ft)",
        min_value=508.00,
        max_value=531.00,
        step=0.01
    )

with c3:
    withdrawal_input = st.number_input(
        "Withdrawal (MLD)",
        min_value=0.0,
        step=1.0
    )

c4, c5 = st.columns(2)

with c4:
    rainfall_input = st.number_input(
        "Rainfall (mm)",
        min_value=0.0
    )

with c5:
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
            "Record Saved Successfully"
        )

    except Exception as e:

        st.error(
            f"Save Error: {e}"
        )

st.divider()

# ==================================================
# LATEST DATA
# ==================================================

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

    current_volume = round(
        get_current_volume(
            live_level
        ),
        2
    )

except:

    current_volume = 0

try:

    available_storage = round(
        get_available_storage(
            live_level,
            date.today()
        ),
        2
    )

except:

    available_storage = 0

try:

    buffer_ft = round(
        get_buffer_ft(
            live_level,
            date.today()
        ),
        2
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

# ==================================================
# KPI CARDS
# ==================================================

st.subheader(
    "📊 Live Reservoir Status"
)

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
        "Available Buffer",
        f"{buffer_ft:.2f} ft"
    )

with k4:

    st.metric(
        "Current Volume (MG)",
        current_volume
    )

with k5:

    st.metric(
        "Available Storage (MG)",
        available_storage
    )

st.divider()

# ==================================================
# DECISION BOX
# ==================================================

st.subheader(
    "📋 Today's Reservoir Decision"
)

if allowed:

    st.success(
        f"""
Current Level : {live_level:.2f} ft

Rule Level : {rule_level:.2f} ft

Available Buffer : {buffer_ft:.2f} ft

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

# ==================================================
# ALERTS
# ==================================================

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
        f"""
🟡 ALERT

Current Level : {live_level:.2f} ft

Approaching alert level.
"""
    )

else:

    st.success(
        "🟢 Reservoir Operating Normally"
    )

st.divider()

# ==================================================
# RESERVOIR GAUGE
# ==================================================

st.subheader(
    "💧 Reservoir Gauge"
)

gauge_value = (
    live_level - 518
) / (
    531 - 518
)

st.progress(
    min(
        max(gauge_value, 0),
        1
    )
)

st.markdown(
    f"""
### Current Level : {live_level:.2f} ft

- Maximum Level : 531.0 ft
- Alert Level : 529.5 ft
- Rule Level : 524.5 ft
- Drawdown Level : 518.0 ft
"""
)

st.divider()

# ==================================================
# HISTORICAL RECORDS
# ==================================================

st.subheader(
    "📜 Historical Records"
)

try:

    records = get_all_records()

    st.dataframe(
        records,
        use_container_width=True
    )

except:

    st.info(
        "Historical records unavailable."
    )

st.divider()

# ==================================================
# TREND ANALYSIS
# ==================================================

st.subheader(
    "📈 Historical Trend Analysis"
)

trend_type = st.selectbox(
    "Select Trend",
    [
        "Rainfall",
        "Withdrawal"
    ]
)

try:

    excel_file = (
        "data/rainfall_withdrawal.xlsx"
    )

    if trend_type == "Rainfall":

        df = pd.read_excel(
            excel_file,
            sheet_name=0,
            header=None
        )

    else:

        df = pd.read_excel(
            excel_file,
            sheet_name=1,
            header=None
        )

    st.dataframe(
        df.head(30),
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Trend Error: {e}"
    )
