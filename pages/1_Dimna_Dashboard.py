import streamlit as st
import pandas as pd
from datetime import date

from utils.google_sheet import (
    add_daily_record,
    get_latest_record,
    get_all_records,
    update_record,
    delete_record
)

from utils.calculations import (
    get_rule_level,
    get_current_volume,
    get_target_volume,
    get_available_storage,
    get_withdrawal_potential,
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

target_volume = get_target_volume(
    date.today()
)

withdrawal_potential = get_withdrawal_potential(
    live_level,
    date.today()
)

status = (
    "✅ Allowed"
    if allowed
    else
    "❌ Not Allowed"
)

st.subheader(
    "📊 Live Reservoir Status"
)

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:

    st.metric(
        "Current Level",
        f"{live_level:.2f} ft"
    )

with k2:

    st.metric(
        "Target Level",
        f"{rule_level:.2f} ft"
    )

with k3:

    st.metric(
        "Current Storage",
        f"{current_volume:.2f} MG"
    )

with k4:

    st.metric(
        "Target Storage",
        f"{target_volume:.2f} MG"
    )

with k5:

    st.metric(
        "Withdrawal Potential",
        f"{withdrawal_potential:.2f} MG"
    )

with k6:

    st.metric(
        "Status",
        status
    )

st.divider()

# ==================================================
# DECISION BOX
# ==================================================

st.subheader(
    "📋 Reservoir Decision"
)

if allowed:

    st.success(
        f"""
### ✅ WITHDRAWAL ALLOWED

Current Level : {live_level:.2f} ft

Target Level : {rule_level:.2f} ft

Current Storage : {current_volume:.2f} MG

Target Storage : {target_volume:.2f} MG

Withdrawal Potential : {withdrawal_potential:.2f} MG
"""
    )

else:

    st.error(
        f"""
### ❌ WITHDRAWAL NOT ALLOWED

Current Level : {live_level:.2f} ft

Target Level : {rule_level:.2f} ft

Current Storage : {current_volume:.2f} MG

Target Storage : {target_volume:.2f} MG

Withdrawal Potential : {withdrawal_potential:.2f} MG
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
st.divider()

st.subheader("✏️ Edit Record")

try:

    records = get_all_records()

    if not records.empty:

        edit_index = st.selectbox(
            "Select Record To Edit",
            records.index
        )

        selected_row = records.loc[
            edit_index
        ]

        edit_date = st.text_input(
            "Date",
            value=str(selected_row["Date"]),
            key="edit_date"
        )

        edit_level = st.number_input(
            "Level",
            value=float(selected_row["Current_Level"]),
            key="edit_level"
        )

        edit_withdrawal = st.number_input(
            "Withdrawal",
            value=float(selected_row["Withdrawal_MLD"]),
            key="edit_withdrawal"
        )

        edit_rainfall = st.number_input(
            "Rainfall",
            value=float(selected_row["Rainfall_mm"]),
            key="edit_rainfall"
        )

        edit_remarks = st.text_input(
            "Remarks",
            value=str(selected_row["Remarks"]),
            key="edit_remarks"
        )

        if st.button("Update Record"):

            update_record(
                edit_index + 2,
                edit_date,
                edit_level,
                edit_withdrawal,
                edit_rainfall,
                edit_remarks
            )

            st.success(
                "Record Updated Successfully"
            )

            st.rerun()

except Exception as e:

    st.error(
        f"Edit Error: {e}"
    )

st.divider()

st.subheader("🗑 Delete Record")

try:

    records = get_all_records()

    if not records.empty:

        delete_index = st.selectbox(
            "Select Record To Delete",
            records.index,
            key="delete_index"
        )

        st.warning(
            "Deleted records cannot be recovered."
        )

        if st.button(
            "Delete Selected Record"
        ):

            delete_record(
                delete_index + 2
            )

            st.success(
                "Record Deleted Successfully"
            )

            st.rerun()

except Exception as e:

    st.error(
        f"Delete Error: {e}"
    )
