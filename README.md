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
