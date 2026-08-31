from app.services.scoring import calculate_priority
from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
old_date = (datetime.now(timezone.utc) - timedelta(days=200)).strftime("%Y-%m-%d")

cases = [
    ("cisa_kev, ransomware, recent, tagged", "cisa_kev", "erp", today, "Known"),
    ("cisa_kev, no ransomware, old, untagged", "cisa_kev", "", old_date, "Unknown"),
    ("otx, recent, multi-tagged", "otx", "erp,warehouse_iot", today, None),
    ("otx, old, untagged", "otx", "", old_date, None),
]

for label, source, tags, date_str, ransomware in cases:
    result = calculate_priority(source, tags, date_str, ransomware)
    print(label)
    print(f"  {result}")
