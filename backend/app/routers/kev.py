import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

@router.get("/kev")
def get_kev():
    try:
        response = requests.get(KEV_URL, timeout=10)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"CISA KEV request failed: {e}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="CISA KEV API error")

    data = response.json()
    vulns = data.get("vulnerabilities", [])

    threats = [
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

    return {"count": len(threats), "threats": threats}
