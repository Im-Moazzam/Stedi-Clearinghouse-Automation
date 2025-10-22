import streamlit as st
from ui.realtime_eligibility import render_form
from ui.batch_eligibility import render_batch_form
import os
import sys

sys.path.append(os.path.abspath("ui"))

st.set_page_config(page_title="Eligibility Checker", layout="centered")

st.title("Eligibility Checker")

tabs = st.tabs(["Check Real-Time Eligibility", "Batch Eligibility Check"])

with tabs[0]:
    render_form()

with tabs[1]:
    render_batch_form()