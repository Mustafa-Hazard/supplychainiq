from fastapi import APIRouter, HTTPException
import requests
from app.services.threat_sources import fetch_otx, fetch_kev

router = APIRouter()


@router.get("/otx")
def get_otx():
    try:
        threats = fetch_otx()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"OTX request failed: {e}")
    return {"count": len(threats), "threats": threats}


@router.get("/kev")
def get_kev():
    try:
        threats = fetch_kev()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"CISA KEV request failed: {e}")
    return {"count": len(threats), "threats": threats}


@router.get("/threats")
def get_threats():
    combined = []
    errors = []

    try:
        combined.extend(fetch_otx())
    except requests.exceptions.RequestException as e:
        errors.append(f"OTX failed: {e}")

    try:
        combined.extend(fetch_kev())
    except requests.exceptions.RequestException as e:
        errors.append(f"CISA KEV failed: {e}")

    if not combined and errors:
        raise HTTPException(status_code=502, detail="; ".join(errors))

    return {
        "count": len(combined),
        "sources_with_errors": errors if errors else None,
        "threats": combined,
    }
