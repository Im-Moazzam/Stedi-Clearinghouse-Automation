import os
from dotenv import load_dotenv

load_dotenv()

ELIGIBILITY_URL = os.getenv("ELIGIBILITY_URL")
STEDI_TEST_API = os.getenv("STEDI_TEST_API")

if not ELIGIBILITY_URL:
    raise ValueError("ELIGIBILITY_URL not found in .env")
if not STEDI_TEST_API:
    raise ValueError("STEDI_TEST_API not found in .env")
