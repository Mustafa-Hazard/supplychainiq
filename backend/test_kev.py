import requests

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

response = requests.get(KEV_URL, timeout=10)
print(f"Status code: {response.status_code}")

data = response.json()
vulns = data.get("vulnerabilities", [])
print(f"Total KEV entries: {len(vulns)}")
print("\nFirst 3 entries:")
for v in vulns[:3]:
    print(f"- {v.get('cveID')}: {v.get('vulnerabilityName')} (ransomware use: {v.get('knownRansomwareCampaignUse')})")
