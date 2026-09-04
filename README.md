# SupplyChainIQ

Threat intelligence dashboard focused on systems relevant to logistics and supply chain
security — fleet/GPS software, warehouse IoT, ERP, port/shipping systems. Pulls real threat
data from OTX and CISA's Known Exploited Vulnerabilities catalog, tags what's actually
relevant to that world, and summarizes it in plain English using an AI fallback chain
(Gemini → Groq → static template).

Built as a portfolio project — the goal is a small custom app that shows real backend +
data + AI integration skills, not a toy CRUD demo.

## Status: in progress

This is being built incrementally, one tested slice at a time. Current state:

- [x] FastAPI backend scaffolded
- [x] `/threats` endpoint pulling live OTX pulse data
- [x] Gemini + Groq API keys wired up, fallback chain proven working
- [ ] CISA KEV integration (in progress on `feature/cisa-kev-integration`)
- [ ] Relevance tagging for logistics-specific systems
- [ ] Priority scoring (severity x relevance x recency)
- [ ] Splunk Free secondary path (HTTP Event Collector + SPL searches + dashboard panel)
- [ ] `/summary` endpoint (AI-generated plain-English briefing)
- [ ] `/trends` endpoint
- [ ] React + TypeScript + Tailwind frontend
- [ ] Dockerized (backend + frontend; Splunk kept separate)

## Tech stack

- **Backend:** FastAPI (Python), SQLite
- **Frontend:** React + TypeScript + Tailwind (not built yet)
- **AI:** Gemini 3.6 Flash → Groq (gpt-oss-120b) → static template fallback
- **Data sources:** AlienVault OTX, CISA KEV
- **Secondary deliverable:** Splunk Free (HTTP Event Collector + SPL + one dashboard panel)

## Running locally (backend only, for now)

\`\`\`bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # not generated yet
cp .env.example .env              # then fill in real keys
uvicorn main:app --reload --port 8000
\`\`\`

Full run instructions (including Docker, once that's built) will land in the final README.

## Known Gotchas

- **OTX data is sparse by design, not a bug.** The ingest uses AlienVault OTX's
  `/pulses/subscribed` endpoint, which is non-historical — it only surfaces pulses
  from subscribed feeds going forward, not a queryable historical archive. CISA KEV,
  by contrast, is a static cumulative catalog with full history back to 2021. So the
  vast majority of weeks in the trend chart legitimately show zero OTX activity; this
  reflects the endpoint's limitations, not missing real-world threats. (As of the last
  DB rebuild: 5 OTX rows across 3 of 226 weeks, out of 1700 total threats.)

## Why not just use a full SIEM?

More detail coming once this section can point at the Splunk piece for comparison — short
version: the custom app is the primary deliverable because it demonstrates backend + data +
AI skills directly, and Splunk Free was added as a smaller secondary piece specifically
because SIEM literacy is a common screening signal for SOC-analyst-track roles.
