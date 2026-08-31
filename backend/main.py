from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.routers import threats

app = FastAPI(title="SupplyChainIQ")

app.include_router(threats.router)

@app.get("/")
def root():
    return {"status": "SupplyChainIQ backend running"}
