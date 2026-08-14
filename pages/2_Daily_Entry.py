import streamlit as st

from utils.google_sheet import (
    add_daily_record
)

st.title(
    "📝 Daily Data Entry"
)

entry_date = st.date_input(
    "Date"
)

current_level = st.number_input(
    "Current Level (ft)",
    508.00,
    531.00,
    step=0.01
)

withdrawal = st.number_input(
    "Withdrawal (MLD)",
    min_value=0.0
)

rainfall = st.number_input(
    "Rainfall (mm)",
    min_value=0.0
)

remarks = st.text_area(
    "Remarks"
)

if st.button(
    "Save Record"
):

    add_daily_record(
        entry_date,
        current_level,
        withdrawal,
        rainfall,
        remarks
    )

    st.success(
        "Record Saved"
    )
