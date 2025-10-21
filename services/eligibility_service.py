import requests
from config.settings import ELIGIBILITY_URL, STEDI_TEST_API

def build_request_body(form_data):
    return {
        "encounter": {"serviceTypeCodes": [form_data["service_type_code"]]},
        "provider": {
            "npi": form_data["provider_npi"],
            "organizationName": form_data["provider_name"],
        },
        "subscriber": {
            "dateOfBirth": form_data["dob"].replace("-", ""),
            "firstName": form_data["first_name"],
            "lastName": form_data["last_name"],
            "memberId": form_data["member_id"],
        },
        "tradingPartnerServiceId": form_data["payer_id"],
    }

def check_eligibility(form_data):
    body = build_request_body(form_data)
    headers = {
        "Authorization": STEDI_TEST_API,
        "Content-Type": "application/json",
    }
    response = requests.post(ELIGIBILITY_URL, json=body, headers=headers, timeout=15)
    return response.json()
