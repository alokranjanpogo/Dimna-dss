import streamlit as st

from utils.google_sheet import (
    add_daily_record,
    get_all_records,
    update_record,
    delete_record
)

st.title("📝 Daily Operations")

st.subheader("Add Record")

entry_date = st.date_input("Date")

level = st.number_input(
    "Current Level (ft)",
    min_value=508.0,
    max_value=531.0,
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

remarks = st.text_input(
    "Remarks"
)

if st.button("Save Record"):

    add_daily_record(
        entry_date,
        level,
        withdrawal,
        rainfall,
        remarks
    )

    st.success("Record Saved")

st.divider()

st.subheader("Historical Records")

records = get_all_records()

st.dataframe(
    records,
    use_container_width=True
)

st.divider()

st.subheader("Edit Record")

if not records.empty:

    idx = st.selectbox(
        "Select Record",
        records.index
    )

    row = records.loc[idx]

    edit_date = st.text_input(
        "Date",
        value=str(row["Date"])
    )

    edit_level = st.number_input(
        "Edit Level",
        value=float(row["Current_Level"])
    )

    edit_withdrawal = st.number_input(
        "Edit Withdrawal",
        value=float(row["Withdrawal_MLD"])
    )

    edit_rainfall = st.number_input(
        "Edit Rainfall",
        value=float(row["Rainfall_mm"])
    )

    edit_remarks = st.text_input(
        "Edit Remarks",
        value=str(row["Remarks"])
    )

    if st.button("Update Record"):

        update_record(
            idx + 2,
            edit_date,
            edit_level,
            edit_withdrawal,
            edit_rainfall,
            edit_remarks
        )

        st.success("Updated Successfully")

st.divider()

st.subheader("Delete Record")

if not records.empty:

    delete_idx = st.selectbox(
        "Select Record To Delete",
        records.index,
        key="delete"
    )

    if st.button("Delete Record"):

        delete_record(
            delete_idx + 2
        )

        st.success(
            "Record Deleted"
        )
