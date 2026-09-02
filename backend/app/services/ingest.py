from datetime import datetime, timezone
from app.database import SessionLocal, engine, Base
from app.models.threat import Threat
from app.services.threat_sources import fetch_otx, fetch_kev
from app.services.tagging import tag_threat
from app.services.scoring import calculate_priority


def _parse_published_at(date_str):
    if not date_str:
        return None
    # OTX: ISO datetime, sometimes with trailing "Z"
    try:
        cleaned = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned)
    except (ValueError, TypeError):
        pass
    # KEV: date-only, e.g. "2026-08-15"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def run_ingest():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    combined = []
    errors = []
    try:
        combined.extend(fetch_otx())
    except Exception as e:
        errors.append(f"OTX failed: {e}")
    try:
        combined.extend(fetch_kev())
    except Exception as e:
        errors.append(f"CISA KEV failed: {e}")

    saved = 0
    updated = 0
    for item in combined:
        tags = tag_threat(item.get("title"), item.get("description"))
        tags_str = ",".join(tags) if tags else ""
        date_for_scoring = item.get("date_added") or item.get("created")
        score_result = calculate_priority(
            source=item.get("source"),
            tags=tags_str,
            date_str=date_for_scoring,
            ransomware_use=item.get("ransomware_use"),
        )
        published_at = _parse_published_at(date_for_scoring)

        existing = db.query(Threat).filter(
            Threat.external_id == item.get("external_id")
        ).first()
        if existing:
            existing.tags = tags_str
            existing.title = item.get("title")
            existing.description = item.get("description")
            existing.priority_score = score_result["priority_score"]
            existing.published_at = published_at
            updated += 1
        else:
            new_threat = Threat(
                source=item.get("source"),
                external_id=item.get("external_id"),
                title=item.get("title"),
                description=item.get("description"),
                tags=tags_str,
                priority_score=score_result["priority_score"],
                published_at=published_at,
                pulled_at=datetime.now(timezone.utc),
            )
            db.add(new_threat)
            saved += 1

    db.commit()
    db.close()
    return {
        "new": saved,
        "updated": updated,
        "total_fetched": len(combined),
        "errors": errors,
    }


if __name__ == "__main__":
    result = run_ingest()
    print(result)
