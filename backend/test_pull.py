import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OTX_API_KEY")

url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
headers = {
    "X-OTX-API-KEY": API_KEY,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
}

response = requests.get(url, headers=headers, params={"limit": 3})

print("Status code:", response.status_code)
if response.status_code == 200:
    data = response.json()
    print("Number of pulses returned:", len(data.get("results", [])))
    for pulse in data.get("results", []):
        print("-", pulse.get("name"))
else:
    print("Error response:", response.text)
