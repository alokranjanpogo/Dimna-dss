import streamlit as st

st.set_page_config(
    page_title="Dimna DSS",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Dimna Reservoir Withdrawal Decision Support System")

st.markdown("""
### Purpose

This dashboard helps:

- Monitor daily Dimna level
- Track withdrawals
- Track rainfall
- Calculate available storage
- Generate withdrawal alerts
- Show historical rainfall trends
- Show historical withdrawal trends
""")
