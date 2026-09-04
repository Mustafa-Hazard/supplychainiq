from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routers import threats, summary, trends
from app.database import Base, engine
from app.models import threat  # noqa: F401 - ensures model is registered before create_all

app = FastAPI(title="SupplyChainIQ")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(threats.router)
app.include_router(summary.router)
app.include_router(trends.router)

@app.get("/")
def root():
    return {"status": "SupplyChainIQ backend running"}
