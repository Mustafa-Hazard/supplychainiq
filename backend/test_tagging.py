from app.services.tagging import tag_threat

tests = [
    ("SAP NetWeaver Vulnerability", "SAP NetWeaver contains a vulnerability allowing remote code execution."),
    ("Fake MP4 File Carries Malicious Payload", "A sophisticated infection chain leverages PowerShell loaders."),
    ("GPS Tracking Device Flaw", "A popular fleet GPS tracking device exposes vehicle location data."),
    ("Random Linux Kernel Bug", "Linux Kernel contains an unspecified vulnerability."),
]

for title, desc in tests:
    tags = tag_threat(title, desc)
    print(f"{title}")
    print(f"  tags: {tags if tags else '(none)'}")
