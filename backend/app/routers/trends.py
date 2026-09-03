from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.trends import get_weekly_trend

router = APIRouter()


@router.get("/trends")
def get_trends(db: Session = Depends(get_db)):
    return get_weekly_trend(db)
