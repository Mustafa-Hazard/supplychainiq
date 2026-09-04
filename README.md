```markdown
# SupplyChainIQ

SupplyChainIQ is an automated threat intelligence dashboard designed to monitor vulnerabilities and threat feeds affecting logistics, warehouse IoT, ERP, and critical shipping infrastructure.

The platform continuously ingests real threat telemetry from AlienVault OTX and CISA's Known Exploited Vulnerabilities (KEV) catalog, scores threats by supply chain relevance and severity, detects multi-week trends, and produces automated executive briefings via a resilient multi-tier AI fallback pipeline.

---

## Current Status

- [x] FastAPI REST backend architecture with SQLite persistence
- [x] Automated multi-source data ingestion pipeline (AlienVault OTX + CISA KEV)
- [x] Domain-specific keyword tagging engine (ERP, Warehouse IoT, Fleet/GPS)
- [x] Composite priority scoring model (Severity × Supply Chain Relevance)
- [x] Resilient 3-tier executive summary generation (`Gemini` → `Groq` → deterministic static template)
- [x] Historical vulnerability trend aggregation endpoint (`/trends`)
- [x] React 19 + TypeScript + Tailwind CSS analytics dashboard
- [x] Interactive data visualization using Recharts
- [x] Multi-container Docker & Docker Compose setup (`backend` + `frontend`)
- [ ] Splunk HTTP Event Collector forwarding (optional secondary integration)

---

## Architecture

```text
[ AlienVault OTX ]       [ CISA KEV Catalog ]
        │                         │
        └────────────┬────────────┘
                     ▼
         [ Ingest Pipeline Service ]
         ├── Domain Keyword Tagging
         └── Priority Scoring (0-10)
                     ▼
           [ SQLite Database ]
                     ▼
          [ FastAPI Application ]
   ┌─────────────────┼─────────────────┐
   ▼                 ▼                 ▼
GET /threats    GET /trends       GET /summary
                                       │
                      ┌────────────────┴────────────────┐
                      ▼                                 ▼
              Tier 1: Google Gemini            Tier 2: Groq Llama
                      │                                 │
                      └────────────────┬────────────────┘
                                       ▼ (on failure)
                             Tier 3: Static Template
                                       │
                                       ▼
                 [ React 19 / TypeScript Dashboard ]
                 ├── Live Metrics & Severity Distribution
                 ├── 220+ Week Historical Vulnerability Trends
                 └── Filterable Threat Inventory

```

---

## Tech Stack

* **Backend:** Python 3.11, FastAPI, SQLAlchemy, SQLite, Uvicorn
* **Frontend:** React 19, TypeScript, Vite, Tailwind CSS, Recharts
* **AI / LLM Orchestration:** Google Gemini API (`gemini-2.5-flash`), Groq API, multi-tier fallback architecture
* **Threat Intelligence Sources:** AlienVault OTX API, CISA Known Exploited Vulnerabilities (KEV) Catalog
* **Containerization:** Docker, Docker Compose, Nginx Alpine

---

## Getting Started

### Option 1: Running with Docker Compose (Recommended)

1. Ensure Docker and Docker Compose are installed.
2. Configure your environment variables in `backend/.env`:
```bash
cd backend && cp .env.example .env
# Add your OTX_API_KEY, GEMINI_API_KEY, and GROQ_API_KEY

```


3. Build and launch all services from the project root:
```bash
docker compose up --build

```


4. Access the services:
* **Frontend Dashboard:** http://localhost:5173
* **Backend API Docs:** http://localhost:8000/docs



---

### Option 2: Running Locally

#### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and supply your API keys

```

Run initial data ingestion:

```bash
python -m app.services.ingest

```

Start the API server:

```bash
uvicorn main:app --reload --port 8000

```

#### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev

```

The frontend will start on http://localhost:5173.

---

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/threats` | Returns full list of ingested threats, priority scores, and tags |
| `GET` | `/trends` | Aggregates weekly historical vulnerability volume across OTX and CISA KEV |
| `GET` | `/summary` | Produces an executive threat briefing via the 3-tier fallback chain |
| `GET` | `/` | Backend health check status |

---

## Engineering Challenges & Lessons Learned

1. **Cold-Start SQLite Initialization (`create_all` race condition):**
Early iterations encountered 500 errors when querying `/threats` against a fresh database because models were not registered prior to creation. Registering the models and invoking `Base.metadata.create_all(bind=engine)` directly inside `main.py` ensured schema creation is guaranteed on startup.
2. **Scoped CORS vs. Browser Preflight:**
Frontend queries in development hung in a `(pending)` state without browser console errors. Explicitly configuring FastAPI's `CORSMiddleware` scoped to the Vite origins resolved browser preflight rejections.
3. **Multi-Source Ingestion Resilience:**
External intelligence APIs can return HTML error pages (e.g., Cloudflare 502 Bad Gateway) instead of valid JSON. In modern `requests`, `requests.exceptions.JSONDecodeError` inherits from `requests.exceptions.RequestException`. Catching this alongside network failures in isolated blocks ensures a failure in one provider (like OTX) doesn't abort the entire ingestion run for healthy sources (like CISA KEV).
4. **Sparse Historical Feeds (OTX vs. CISA KEV):**
The AlienVault OTX `/pulses/subscribed` endpoint is non-historical; it only delivers pulses going forward from active subscriptions. CISA KEV, by contrast, is a cumulative catalog dating back to 2021. The trend visualization explicitly accounts for this split (e.g., 5 OTX rows vs. 1695 KEV rows across 226 weeks) to prevent misinterpreting feed mechanics as data loss.
5. **Recharts X-Axis Tick Collision:**
Plotting 220+ historical weeks created unreadable, overlapping timestamps on standard charts. Adding custom tick formatters, dynamic step intervals, and angled tick anchors preserved visual clarity across screen widths.

```

```
