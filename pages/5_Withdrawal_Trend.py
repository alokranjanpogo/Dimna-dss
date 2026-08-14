import streamlit as st
import pandas as pd

st.title(
    "🚰 Withdrawal Trends"
)

file = "data/rainfall_withdrawal.xlsx"

df = pd.read_excel(
    file,
    sheet_name=1
)

st.dataframe(
    df.head()
)

st.info(
    "Withdrawal graphs to be refined after data cleaning."
)
