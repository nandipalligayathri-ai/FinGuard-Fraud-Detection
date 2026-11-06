from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .config import settings
from .routers import auth, transactions, alerts, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Risk Analysis & Rule-Based Review API",
    description="Synthetic transaction analysis. Alerts are review signals, not confirmed fraud.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware, allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(alerts.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Financial Risk API is running", "docs": "/docs"}
