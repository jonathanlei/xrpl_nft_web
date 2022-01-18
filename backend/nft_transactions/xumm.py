import requests
import os
from dotenv import load_dotenv


load_dotenv()
url = "https://xumm.app/api/v1/platform/payload"
print(os.getenv("XUMM_APP_SECRET"))
payload = {"txjson": {"TransactionType": "SignIn"}}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Key": os.environ.get("XUMM_APP_KEY"),
    "X-API-Secret": os.environ.get("XUMM_APP_SECRET"),
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
