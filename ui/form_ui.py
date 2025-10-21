import streamlit as st
import json
import datetime
from pathlib import Path
from services.eligibility_service import check_eligibility, build_request_body

def load_service_type_codes():
    path = Path("data/service_type_codes.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [f"{k}: {v}" for k, v in data.items()]

def load_payers():
    path = Path("data/payers.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Only show those that support eligibility
    return [
        {
            "displayName": p["displayName"],
            "primaryPayerId": p["primaryPayerId"],
            "eligibility": p["transactionSupport"].get("eligibilityCheck") == "SUPPORTED",
        }
        for p in data["items"]
        if p["transactionSupport"].get("eligibilityCheck") == "SUPPORTED"
    ]

def render_form():
    st.header("Payer Information")

    payers = load_payers()
    payer_names = sorted([p["displayName"] for p in payers])
    payer_name = st.selectbox("Payer *", ["Select a Payer"] + payer_names)

    # Automatically fill payer_id when payer is selected
    auto_payer_id = ""
    if payer_name != "Select a Payer":
        auto_payer_id = next(
            (p["primaryPayerId"] for p in payers if p["displayName"] == payer_name),
            ""
        )

    # Allow manual override (user can still type their own)
    payer_id = st.text_input(
        "Payer ID",
        value=auto_payer_id,
        placeholder="Enter or confirm Payer ID",
    )

    st.header("Encounter")
    service_type_code = st.selectbox(
        "Service type code *",
        load_service_type_codes(),
        placeholder="Select a Service Type Code",
    )

    st.header("Subscriber")
    member_id = st.text_input("Member ID *")
    c1, c2, c3 = st.columns(3)
    with c1:
        first_name = st.text_input("First name *")
    with c2:
        middle_name = st.text_input("Middle name")
    with c3:
        last_name = st.text_input("Last name *")

    c1, c2 = st.columns(2)
    with c1:
        dob = st.date_input("Date of birth *", min_value=datetime.date(1900, 1, 1)).strftime("%Y-%m-%d")
    with c2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    st.header("Provider")
    c1, c2 = st.columns(2)
    with c1:
        provider_name = st.text_input("Provider name *", placeholder="Enter Provider Name")
    with c2:
        provider_npi = st.text_input("Provider NPI *")

    if st.button("Check Eligibility"):
        if not payer_id:
            st.error("Payer ID is required.")
            return

        # Prepare form data
        form_data = {
            "payer_id": payer_id.strip(),
            "service_type_code": service_type_code.split(":")[0].strip(),
            "member_id": member_id.strip(),
            "first_name": first_name.strip(),
            "middle_name": middle_name.strip(),
            "last_name": last_name.strip(),
            "dob": dob,
            "gender": gender,
            "provider_name": provider_name.strip(),
            "provider_npi": provider_npi.strip(),
        }

        st.subheader("Request Body")
        st.json(build_request_body(form_data))
        print(build_request_body(form_data))

        with st.spinner("Checking eligibility..."):
            response = check_eligibility(form_data)

        st.subheader("Response")
        st.json(response)

