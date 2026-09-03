from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.models.threat import Threat


def get_weekly_trend(db: Session) -> dict:
    """
    Buckets threats by week (Monday-start) using published_at, broken down
    by source, all computed in a single SQL aggregation query.

    Rows with null published_at (aged-out OTX pulses, see PR #8 gotcha)
    are excluded from the trend and counted separately.
    """
    week_start = func.date(Threat.published_at, "weekday 0", "-6 days").label(
        "week_start"
    )

    rows = (
        db.query(
            week_start,
            func.sum(case((Threat.source == "otx", 1), else_=0)).label("otx"),
            func.sum(case((Threat.source == "cisa_kev", 1), else_=0)).label("kev"),
            func.count().label("total"),
        )
        .filter(Threat.published_at.isnot(None))
        .group_by(week_start)
        .order_by(week_start)
        .all()
    )

    excluded_null_count = (
        db.query(func.count(Threat.id)).filter(Threat.published_at.is_(None)).scalar()
    )

    return {
        "trend": [
            {
                "week_start": row.week_start,
                "otx": row.otx,
                "kev": row.kev,
                "total": row.total,
            }
            for row in rows
        ],
        "excluded_null_count": excluded_null_count,
    }
