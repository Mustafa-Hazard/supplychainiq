import os
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

OTX_API_KEY = os.getenv("OTX_API_KEY")
OTX_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"

@router.get("/threats")
def get_threats():
    headers = {"X-OTX-API-KEY": OTX_API_KEY}
    try:
        response = requests.get(OTX_URL, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"OTX request failed: {e}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="OTX API error")

    data = response.json()
    pulses = data.get("results", [])

    threats = [
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

    return {"count": len(threats), "threats": threats}
