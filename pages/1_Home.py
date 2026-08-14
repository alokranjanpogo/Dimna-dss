import streamlit as st
from datetime import date

from utils.google_sheet import (
    get_latest_record
)

from utils.calculations import (
    get_complete_summary
)

from utils.alerts import (
    get_alert
)

st.title(
    "💧 Dimna DSS Dashboard"
)

latest = get_latest_record()

if latest is not None:

    current_level = float(
        latest["Current_Level"]
    )

    summary = get_complete_summary(
        current_level,
        date.today()
    )

    alert = get_alert(
        current_level
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Current Level",
            f"{current_level:.2f} ft"
        )

    with c2:
        st.metric(
            "Rule Level",
            f"{summary['rule_level']} ft"
        )

    with c3:
        st.metric(
            "Current Volume",
            round(
                summary[
                    "current_volume"
                ],
                2
            )
        )

    with c4:
        st.metric(
            "Available Storage",
            round(
                summary[
                    "storage"
                ],
                2
            )
        )

    if alert["status"] == "RED":

        st.error(
            alert["message"]
        )

    elif alert["status"] == "YELLOW":

        st.warning(
            alert["message"]
        )

    else:

        st.success(
            alert["message"]
        )

else:

    st.info(
        "No data available"
    )
