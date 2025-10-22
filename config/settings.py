import os
from dotenv import load_dotenv

load_dotenv()

STEDI_TEST_API = os.getenv("STEDI_TEST_API")
ELIGIBILITY_URL = os.getenv("ELIGIBILITY_URL")
BATCH_ELIGIBILITY_URL = os.getenv("BATCH_ELIGIBILITY_URL")
POLL_URL = os.getenv("POLL_URL")

if not ELIGIBILITY_URL:
    raise ValueError("ELIGIBILITY_URL not found in .env")
if not STEDI_TEST_API:
    raise ValueError("STEDI_TEST_API not found in .env")
if not POLL_URL:
    raise ValueError("POLL_URL not found in .env")
