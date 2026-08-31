from dotenv import load_dotenv
load_dotenv()

import os
import requests

OTX_API_KEY = os.getenv("OTX_API_KEY")
OTX_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def fetch_otx():
    headers = {"X-OTX-API-KEY": OTX_API_KEY}
    response = requests.get(OTX_URL, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    pulses = data.get("results", [])

    return [
        {
            "source": "otx",
            "external_id": p.get("id"),
            "title": p.get("name"),
            "description": p.get("description"),
            "indicator_count": len(p.get("indicators", [])),
            "created": p.get("created"),
        }
        for p in pulses
    ]


def fetch_kev():
    response = requests.get(KEV_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    vulns = data.get("vulnerabilities", [])

    return [
        {
            "source": "cisa_kev",
            "external_id": v.get("cveID"),
            "title": v.get("vulnerabilityName"),
            "description": v.get("shortDescription"),
            "ransomware_use": v.get("knownRansomwareCampaignUse"),
            "date_added": v.get("dateAdded"),
        }
        for v in vulns
    ]
