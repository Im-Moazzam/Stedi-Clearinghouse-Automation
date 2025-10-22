import pandas as pd
import streamlit as st
import requests
import datetime
import uuid
import os

API_URL = "https://manager.us.stedi.com/2024-04-01/eligibility-manager/batch-eligibility"
API_KEY = os.getenv("STEDI_API_KEY")  # store your API key securely

def render_batch_form():
    st.info("Upload an Excel file with subscriber demographics to check eligibility in batch.")
    
    # Optional: template download
    template_df = pd.DataFrame(columns=[
        "MemberID", "FirstName", "LastName", "DOB", 
        "ProviderName", "ProviderNPI", "ServiceCode", "TradingPartnerID"
    ])

    template_file = "batch_template.xlsx"
    template_df.to_excel(template_file, index=False)

    st.download_button(
        label="Download template Excel",
        data=open(template_file, "rb"),
        file_name="batch_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    uploaded_file = st.file_uploader("Drag and drop your Excel file here",
                                     type=["xlsx", "xls"],
                                     accept_multiple_files=False)
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Failed to read the uploaded file: {e}")
            return
        
        required_columns = ["MemberID", "FirstName", "LastName", "DOB", "ProviderName", "ProviderNPI", "ServiceCode", "TradingPartnerID"]
        missing_cols = [c for c in required_columns if c not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
            return
        
        if len(df) > 1000:
            st.error("Maximum batch size is 1000 checks per submission.")
            return
        
        st.success(f"File uploaded successfully: {uploaded_file.name}")
        st.dataframe(df.head(10))
        
        if st.button("Send Batch Request"):
            items = []
            for _, row in df.iterrows():
                # Sanitize names
                first_name = str(row["FirstName"]).replace("`", "'")
                last_name = str(row["LastName"]).replace("`", "'")
                
                # Format DOB
                dob_str = pd.to_datetime(row["DOB"]).strftime("%Y%m%d")
                
                items.append({
                    "encounter": {
                        "serviceTypeCodes": [str(row["ServiceCode"])]
                    },
                    "provider": {
                        "npi": str(row["ProviderNPI"]),
                        "organizationName": row["ProviderName"]
                    },
                    "submitterTransactionIdentifier": str(uuid.uuid4()),
                    "subscriber": {
                        "dateOfBirth": dob_str,
                        "firstName": first_name,
                        "lastName": last_name,
                        "memberId": str(row["MemberID"])
                    },
                    "tradingPartnerServiceId": row["TradingPartnerID"]
                })
            
            body = {
                "items": items,
                "name": f"batch-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
            }
            
            headers = {
                "Authorization": API_KEY,
                "Content-Type": "application/json"
            }
            
            with st.spinner("Sending batch eligibility request..."):
                try:
                    response = requests.post(API_URL, json=body, headers=headers)
                    response.raise_for_status()
                    batch_id = response.json().get("batchId", "N/A")
                    st.success(f"Batch submitted successfully. Batch ID: {batch_id}")
                    st.info("Results will be available asynchronously. Use the Poll Batch Eligibility Checks endpoint to retrieve them later.")
                except Exception as e:
                    st.error(f"Failed to send batch request: {e}")
