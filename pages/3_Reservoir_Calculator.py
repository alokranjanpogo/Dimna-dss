import streamlit as st
from datetime import date

from utils.calculations import (
    get_complete_summary
)

st.title(
    "📊 Reservoir Calculator"
)

level = st.number_input(
    "Enter Reservoir Level",
    508.00,
    531.00,
    step=0.01
)

summary = get_complete_summary(
    level,
    date.today()
)

st.metric(
    "Rule Level",
    summary["rule_level"]
)

st.metric(
    "Current Volume",
    summary["current_volume"]
)

st.metric(
    "Rule Volume",
    summary["rule_volume"]
)

st.metric(
    "Available Storage",
    summary["storage"]
)

if summary[
    "withdrawal_allowed"
]:

    st.success(
        "Withdrawal Allowed"
    )

else:

    st.error(
        "Withdrawal Not Allowed"
    )
