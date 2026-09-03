from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.routers import threats, summary, trends

app = FastAPI(title="SupplyChainIQ")

app.include_router(threats.router)
app.include_router(summary.router)
app.include_router(trends.router)

@app.get("/")
def root():
    return {"status": "SupplyChainIQ backend running"}
