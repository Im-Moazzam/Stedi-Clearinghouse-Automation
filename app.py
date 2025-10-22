import streamlit as st
from ui.realtime_eligibility import render_form

st.set_page_config(page_title="Eligibility Checker", layout="centered")
render_form()
