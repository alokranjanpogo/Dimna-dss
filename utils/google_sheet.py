import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def connect_sheet():

    # TEMPORARY DEBUG
    st.write("Available Secrets:", dict(st.secrets))

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    workbook = client.open(
        "Dimna DSS Database"
    )

    return workbook


def get_daily_sheet():

    workbook = connect_sheet()

    return workbook.worksheet(
        "Daily_Operations"
    )


def add_daily_record(
    entry_date,
    level,
    withdrawal,
    rainfall,
    remarks
):

    sheet = get_daily_sheet()

    sheet.append_row([
        str(entry_date),
        level,
        withdrawal,
        rainfall,
        remarks
    ])


def get_all_records():

    sheet = get_daily_sheet()

    records = sheet.get_all_records()

    return pd.DataFrame(records)


def get_latest_record():

    df = get_all_records()

    if df.empty:
        return None

    return df.iloc[-1]
