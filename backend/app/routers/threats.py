from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import requests
from app.services.threat_sources import fetch_otx, fetch_kev
from app.database import get_db
from app.models.threat import Threat

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


def _serialize(t: Threat) -> dict:
    return {
        "id": t.id,
        "source": t.source,
        "external_id": t.external_id,
        "title": t.title,
        "description": t.description,
        "indicators": t.indicators,
        "tags": t.tags,
        "priority_score": t.priority_score,
        "published_at": t.published_at,
        "pulled_at": t.pulled_at,
    }


@router.get("/threats")
def get_threats(db: Session = Depends(get_db)):
    threats = (
        db.query(Threat)
        .order_by(Threat.priority_score.desc())
        .all()
    )

    return {
        "count": len(threats),
        "threats": [_serialize(t) for t in threats],
    }
