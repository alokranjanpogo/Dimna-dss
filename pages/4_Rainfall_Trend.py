import streamlit as st
import pandas as pd
import plotly.express as px

st.title(
    "🌧 Rainfall Trends"
)

file = "data/rainfall_withdrawal.xlsx"

df = pd.read_excel(
    file,
    sheet_name=0
)

st.dataframe(
    df.head()
)

st.info(
    "Rainfall graphs to be refined after data cleaning."
)
