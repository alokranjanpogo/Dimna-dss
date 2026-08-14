import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def connect_sheet():

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
    date,
    level,
    withdrawal,
    rainfall,
    remarks
):

    sheet = get_daily_sheet()

    sheet.append_row(
        [
            str(date),
            level,
            withdrawal,
            rainfall,
            remarks
        ]
    )


def get_all_records():

    sheet = get_daily_sheet()

    data = sheet.get_all_records()

    return pd.DataFrame(data)


def get_latest_record():

    df = get_all_records()

    if len(df) == 0:
        return None

    return df.iloc[-1]
