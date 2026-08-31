import re

KEYWORDS = {
    "fleet_gps": [
        "fleet management", "gps tracking", "gps", "telematics",
        "vehicle tracking", "fleet tracking"
    ],
    "warehouse_iot": [
        "warehouse", "rfid", "scada", "industrial control system",
        "programmable logic controller", "iot sensor",
        "inventory management system", "hmi"
    ],
    "erp": [
        "erp", "sap", "oracle netsuite", "supply chain management",
        "enterprise resource planning", "netsuite"
    ],
    "port_shipping": [
        "port system", "maritime", "shipping platform", "customs system",
        "freight", "cargo management", "vessel tracking", "logistics platform"
    ],
}


def tag_threat(title: str, description: str, debug: bool = False):
    text = f"{title or ''} {description or ''}".lower()
    tags = []
    matched_keywords = []

    for category, keywords in KEYWORDS.items():
        for kw in keywords:
            pattern = r"\b" + re.escape(kw) + r"\b"
            match = re.search(pattern, text)
            if match:
                tags.append(category)
                matched_keywords.append((category, kw, text[max(0, match.start()-20):match.end()+20]))
                break

    if debug:
        return tags, matched_keywords
    return tags
