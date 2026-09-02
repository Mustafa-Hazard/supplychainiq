from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.threat import Threat
from app.services.summary import build_briefing_prompt, get_ai_summary

router = APIRouter()


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    top_threats = (
        db.query(Threat)
        .order_by(Threat.priority_score.desc())
        .limit(10)
        .all()
    )

    if not top_threats:
        return {
            "generated_by": "none",
            "summary": "No threats in the database yet. Run the ingest pipeline first.",
            "based_on_count": 0,
        }

    prompt = build_briefing_prompt(top_threats)
    summary_text, tier = get_ai_summary(prompt)

    return {
        "generated_by": tier,
        "summary": summary_text,
        "based_on_count": len(top_threats),
    }
