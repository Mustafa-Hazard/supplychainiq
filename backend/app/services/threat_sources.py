from dotenv import load_dotenv
load_dotenv()

import os
import requests

OTX_API_KEY = os.getenv("OTX_API_KEY")
OTX_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def fetch_otx(max_pulses: int = 100):
    # AlienVault OTX blocks the default python-requests User-Agent as basic
    # bot protection (returns 403 even with a valid key). A browser-like UA
    # is required.
    #
    # OTX also silently caps unpaginated requests at ~5 results per page
    # (confirmed: 9000+ pulses available, only 5 returned with no limit/page
    # param). We follow the API's own "next" pagination links up to
    # max_pulses, rather than hardcoding a page count, since page size is
    # not guaranteed to stay at 5.
    headers = {
        "X-OTX-API-KEY": OTX_API_KEY,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    }

    pulses = []
    url = OTX_URL
    params = {"limit": 50}

    while url and len(pulses) < max_pulses:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        pulses.extend(data.get("results", []))
        url = data.get("next")
        params = None  # "next" URL already contains query params

    pulses = pulses[:max_pulses]

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
    response = requests.get(KEV_URL, timeout=20)
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
