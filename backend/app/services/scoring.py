from datetime import datetime, timezone


def score_severity(source: str, ransomware_use: str = None) -> float:
    if source == "cisa_kev":
        if ransomware_use and ransomware_use.lower() == "known":
            return 10.0
        return 6.0
    return 5.0


def score_relevance(tags: str) -> float:
    if not tags:
        return 0.0
    tag_count = len([t for t in tags.split(",") if t])
    if tag_count == 0:
        return 0.0
    if tag_count == 1:
        return 6.0
    return 10.0


def score_recency(date_str: str) -> float:
    if not date_str:
        return 1.0

    try:
        clean_date = date_str.split("T")[0]
        published = datetime.strptime(clean_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (ValueError, AttributeError):
        return 1.0

    days_old = (datetime.now(timezone.utc) - published).days

    if days_old <= 7:
        return 10.0
    if days_old <= 30:
        return 7.0
    if days_old <= 90:
        return 4.0
    return 1.0


def calculate_priority(source: str, tags: str, date_str: str, ransomware_use: str = None) -> dict:
    severity = score_severity(source, ransomware_use)
    relevance = score_relevance(tags)
    recency = score_recency(date_str)
    overall = round((severity + relevance + recency) / 3, 2)

    return {
        "severity": severity,
        "relevance": relevance,
        "recency": recency,
        "priority_score": overall,
    }
